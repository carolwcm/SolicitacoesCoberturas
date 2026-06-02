# src/models/solicitacao.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..resources.database import Base

class SolicitacaoCobertura(Base):
    __tablename__ = "solicitacoes_cobertura"

    id = Column(Integer, primary_key=True, index=True)
    prontuario = Column(Integer, index=True, nullable=False)
    nome_paciente = Column(String, nullable=False)
    leito = Column(String, nullable=True)
    solicitante = Column(String, nullable=False) # Quem solicitou no AGHU
    status = Column(String, default="PENDENTE", index=True) # PENDENTE, AUTORIZADO, NEGADO, ENTREGUE
    
    # Dados de Auditoria (CCIRAS)
    auditor_username = Column(String, nullable=True)
    data_auditoria = Column(DateTime, nullable=True)
    justificativa = Column(String, nullable=True)
    
    # Dados de Entrega (Farmácia)
    farmaceutico_username = Column(String, nullable=True)
    data_entrega = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relacionamento com os itens da solicitação
    itens = relationship("ItemSolicitacao", back_populates="solicitacao", cascade="all, delete-orphan", lazy="selectin")


class ItemSolicitacao(Base):
    __tablename__ = "itens_solicitacao"

    id = Column(Integer, primary_key=True, index=True)
    solicitacao_id = Column(Integer, ForeignKey("solicitacoes_cobertura.id", ondelete="CASCADE"), nullable=False)
    codigo_material = Column(Integer, nullable=False)
    nome_material = Column(String, nullable=False)
    quantidade_solicitada = Column(Integer, nullable=False)
    quantidade_autorizada = Column(Integer, nullable=True) # Definida pela CCIRAS
    status_item = Column(String, default="PENDENTE") # PENDENTE, AUTORIZADO, NEGADO

    solicitacao = relationship("SolicitacaoCobertura", back_populates="itens")
