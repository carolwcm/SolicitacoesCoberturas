# src/providers/interfaces/solicitacao_cobertura_provider_interface.py

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class SolicitacaoCoberturaProviderInterface(ABC):
    """Interface (contrato) para provedores de dados de solicitações de cobertura."""

    @abstractmethod
    async def criar_solicitacao(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria uma nova solicitação vinda do AGHU."""
        pass

    @abstractmethod
    async def listar_solicitacoes(self, status: str = None) -> List[Dict[str, Any]]:
        """Retorna uma lista de solicitações filtradas por status."""
        pass

    @abstractmethod
    async def obter_solicitacao_por_id(self, solicitacao_id: int) -> Dict[str, Any]:
        """Retorna uma única solicitação pelo seu ID."""
        pass

    @abstractmethod
    async def atualizar_auditoria(
        self, 
        solicitacao_id: int, 
        auditor: str, 
        status: str, 
        justificativa: str, 
        itens_atualizados: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Atualiza a auditoria da CCIRAS para a solicitação."""
        pass

    @abstractmethod
    async def registrar_entrega(
        self, 
        solicitacao_id: int, 
        farmaceutico: str,
        status_geral: str,
        justificativa: str,
        itens_atualizados: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Registra a entrega/liberação dos itens pela farmácia."""
        pass
