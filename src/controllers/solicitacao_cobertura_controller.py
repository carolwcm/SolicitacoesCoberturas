# src/controllers/solicitacao_cobertura_controller.py

from typing import List, Dict, Any
from fastapi import HTTPException, status
from ..providers.interfaces.solicitacao_cobertura_provider_interface import SolicitacaoCoberturaProviderInterface

async def criar_solicitacao(
    data: Dict[str, Any], 
    provider: SolicitacaoCoberturaProviderInterface
) -> Dict[str, Any]:
    """Cria uma solicitação de cobertura a partir dos dados do AGHU."""
    # Validações básicas de entrada
    if not data.get("prontuario"):
        raise HTTPException(status_code=400, detail="O prontuário é obrigatório.")
    if not data.get("nome_paciente"):
        raise HTTPException(status_code=400, detail="O nome do paciente é obrigatório.")
    if not data.get("itens") or len(data["itens"]) == 0:
        raise HTTPException(status_code=400, detail="A solicitação deve conter pelo menos um item.")
        
    return await provider.criar_solicitacao(data)

async def listar_solicitacoes(
    status_filter: str, 
    provider: SolicitacaoCoberturaProviderInterface
) -> List[Dict[str, Any]]:
    """Lista as solicitações do sistema, opcionalmente filtradas por status."""
    return await provider.listar_solicitacoes(status_filter)

async def obter_solicitacao(
    solicitacao_id: int, 
    provider: SolicitacaoCoberturaProviderInterface
) -> Dict[str, Any]:
    """Busca uma solicitação específica."""
    return await provider.obter_solicitacao_por_id(solicitacao_id)

async def auditar_solicitacao(
    solicitacao_id: int,
    auditor: str,
    status_geral: str,
    justificativa: str,
    itens_atualizados: List[Dict[str, Any]],
    provider: SolicitacaoCoberturaProviderInterface
) -> Dict[str, Any]:
    """Realiza a auditoria da CCIRAS na solicitação."""
    if status_geral.upper() not in ["AUTORIZADO", "NEGADO", "EM ANÁLISE", "LIBERADO", "LIBERADO PELA CCIRAS"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Status geral inválido na auditoria."
        )

    # Validações dos itens auditados
    for item in itens_atualizados:
        if "id" not in item:
            raise HTTPException(status_code=400, detail="ID do item é obrigatório para atualização.")
        if item.get("status_item").upper() not in ["AUTORIZADO", "NEGADO", "PENDENTE", "LIBERADO", "EM ANÁLISE"]:
            raise HTTPException(status_code=400, detail="Status de item inválido.")
        if item.get("status_item").upper() in ["AUTORIZADO", "LIBERADO"]:
            qtd_aut = item.get("quantidade_autorizada")
            if qtd_aut is None or qtd_aut < 0:
                raise HTTPException(status_code=400, detail="Quantidade autorizada inválida para item aprovado.")

    return await provider.atualizar_auditoria(
        solicitacao_id=solicitacao_id,
        auditor=auditor,
        status_geral=status_geral,
        justificativa=justificativa,
        itens_atualizados=itens_atualizados,
        provider=provider
    )

async def entregar_solicitacao(
    solicitacao_id: int,
    farmaceutico: str,
    status_geral: str,
    justificativa: str,
    itens_atualizados: List[Dict[str, Any]],
    provider: SolicitacaoCoberturaProviderInterface
) -> Dict[str, Any]:
    """Registra que a farmácia entregou/liberou os itens autorizados."""
    # Validações dos itens liberados
    for item in itens_atualizados:
        if "id" not in item:
            raise HTTPException(status_code=400, detail="ID do item é obrigatório para liberação.")
        qtd_lib = item.get("quantidade_liberada")
        if qtd_lib is None or qtd_lib < 0:
            raise HTTPException(status_code=400, detail="Quantidade liberada inválida.")

    return await provider.registrar_entrega(
        solicitacao_id=solicitacao_id,
        farmaceutico=farmaceutico,
        status_geral=status_geral,
        justificativa=justificativa,
        itens_atualizados=itens_atualizados
    )
