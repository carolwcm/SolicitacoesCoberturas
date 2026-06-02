# src/providers/implementations/solicitacao_cobertura_sqlite_provider.py

from typing import List, Dict, Any
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from datetime import datetime

from ..interfaces.solicitacao_cobertura_provider_interface import SolicitacaoCoberturaProviderInterface
from ...models.solicitacao import SolicitacaoCobertura, ItemSolicitacao

class SolicitacaoCoberturaSqliteProvider(SolicitacaoCoberturaProviderInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _solicitacao_to_dict(self, sol: SolicitacaoCobertura) -> Dict[str, Any]:
        """Converte uma instância do modelo SolicitacaoCobertura para dicionário."""
        return {
            "id": sol.id,
            "prontuario": sol.prontuario,
            "nome_paciente": sol.nome_paciente,
            "leito": sol.leito,
            "solicitante": sol.solicitante,
            "status": sol.status,
            "auditor_username": sol.auditor_username,
            "data_auditoria": sol.data_auditoria.isoformat() if sol.data_auditoria else None,
            "justificativa": sol.justificativa,
            "farmaceutico_username": sol.farmaceutico_username,
            "data_entrega": sol.data_entrega.isoformat() if sol.data_entrega else None,
            "created_at": sol.created_at.isoformat() if sol.created_at else None,
            "updated_at": sol.updated_at.isoformat() if sol.updated_at else None,
            "itens": [
                {
                    "id": item.id,
                    "codigo_material": item.codigo_material,
                    "nome_material": item.nome_material,
                    "quantidade_solicitada": item.quantidade_solicitada,
                    "quantidade_autorizada": item.quantidade_autorizada,
                    "status_item": item.status_item
                } for item in sol.itens
            ]
        }

    async def criar_solicitacao(self, data: Dict[str, Any]) -> Dict[str, Any]:
        solicitacao = SolicitacaoCobertura(
            prontuario=data["prontuario"],
            nome_paciente=data["nome_paciente"],
            leito=data.get("leito"),
            solicitante=data["solicitante"],
            status="PENDENTE"
        )
        self.session.add(solicitacao)
        await self.session.flush() # Para gerar o id da solicitação
        
        for item_data in data["itens"]:
            item = ItemSolicitacao(
                solicitacao_id=solicitacao.id,
                codigo_material=item_data["codigo_material"],
                nome_material=item_data["nome_material"],
                quantidade_solicitada=item_data["quantidade_solicitada"],
                status_item="PENDENTE"
            )
            self.session.add(item)
            
        await self.session.commit()
        # Recarrega a solicitação com seus itens
        stmt = select(SolicitacaoCobertura).where(SolicitacaoCobertura.id == solicitacao.id)
        result = await self.session.execute(stmt)
        sol = result.scalar_one()
        return self._solicitacao_to_dict(sol)

    async def listar_solicitacoes(self, status_filter: str = None) -> List[Dict[str, Any]]:
        stmt = select(SolicitacaoCobertura).order_by(SolicitacaoCobertura.created_at.desc())
        if status_filter:
            stmt = stmt.where(SolicitacaoCobertura.status == status_filter.upper())
            
        result = await self.session.execute(stmt)
        solicitacoes = result.scalars().all()
        return [self._solicitacao_to_dict(sol) for sol in solicitacoes]

    async def obter_solicitacao_por_id(self, solicitacao_id: int) -> Dict[str, Any]:
        stmt = select(SolicitacaoCobertura).where(SolicitacaoCobertura.id == solicitacao_id)
        result = await self.session.execute(stmt)
        sol = result.scalar_one_or_none()
        
        if not sol:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Solicitação com ID {solicitacao_id} não encontrada."
            )
        return self._solicitacao_to_dict(sol)

    async def atualizar_auditoria(
        self, 
        solicitacao_id: int, 
        auditor: str, 
        status_geral: str, 
        justificativa: str, 
        itens_atualizados: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        stmt = select(SolicitacaoCobertura).where(SolicitacaoCobertura.id == solicitacao_id)
        result = await self.session.execute(stmt)
        sol = result.scalar_one_or_none()
        
        if not sol:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Solicitação com ID {solicitacao_id} não encontrada."
            )

        # Atualiza a solicitação geral
        sol.status = status_geral.upper()
        sol.auditor_username = auditor
        sol.data_auditoria = datetime.now()
        sol.justificativa = justificativa
        
        # Mapeia itens existentes por código do material para atualizar
        itens_map = {item.id: item for item in sol.itens}
        
        for item_up in itens_atualizados:
            item_id = item_up.get("id")
            if item_id in itens_map:
                item = itens_map[item_id]
                item.quantidade_autorizada = item_up.get("quantidade_autorizada")
                item.status_item = item_up.get("status_item", "PENDENTE").upper()

        await self.session.commit()
        return self._solicitacao_to_dict(sol)

    async def registrar_entrega(self, solicitacao_id: int, farmaceutico: str) -> Dict[str, Any]:
        stmt = select(SolicitacaoCobertura).where(SolicitacaoCobertura.id == solicitacao_id)
        result = await self.session.execute(stmt)
        sol = result.scalar_one_or_none()
        
        if not sol:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Solicitação com ID {solicitacao_id} não encontrada."
            )

        if sol.status != "AUTORIZADO":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Somente solicitações no status AUTORIZADO podem ser entregues."
            )

        sol.status = "ENTREGUE"
        sol.farmaceutico_username = farmaceutico
        sol.data_entrega = datetime.now()

        await self.session.commit()
        return self._solicitacao_to_dict(sol)
