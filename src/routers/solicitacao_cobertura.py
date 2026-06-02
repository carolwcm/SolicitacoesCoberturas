# src/routers/solicitacao_cobertura.py

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from ..auth.auth import auth_handler
from ..dependencies import get_solicitacao_cobertura_provider
from ..resources.database import get_app_db_session, get_aghu_db_session
from ..providers.interfaces.solicitacao_cobertura_provider_interface import SolicitacaoCoberturaProviderInterface
from ..controllers import solicitacao_cobertura_controller
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/api/solicitacoes",
    tags=["Solicitações de Cobertura"],
    dependencies=[Depends(auth_handler.decode_token)]
)

# Pydantic Schemas
class ItemSolicitacaoInput(BaseModel):
    codigo_material: int
    nome_material: str
    quantidade_solicitada: int

class SolicitacaoInput(BaseModel):
    prontuario: int
    nome_paciente: str
    leito: Optional[str] = None
    solicitante: str
    itens: List[ItemSolicitacaoInput]

class ItemAuditoriaInput(BaseModel):
    id: int
    quantidade_autorizada: Optional[int] = None
    status_item: str # AUTORIZADO, NEGADO, PENDENTE

class AuditoriaInput(BaseModel):
    status_geral: str # AUTORIZADO, NEGADO
    justificativa: str
    itens: List[ItemAuditoriaInput]

# Verificadores de Acesso (AD Groups)
CCIRAS_GROUP = "SOL-COB-CCIRAS"
FARMACIA_GROUP = "SOL-COB-FARMACIA"
ADMIN_GROUP = "GLO-SEC-HCPE-SETISD" # Grupo admin existente

async def verify_cciras_group(current_user: dict = Depends(auth_handler.decode_token)):
    user_groups = current_user.get("groups", [])
    if CCIRAS_GROUP not in user_groups and ADMIN_GROUP not in user_groups:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Acesso negado. Exclusivo para membros da CCIRAS."
        )
    return current_user

async def verify_farmacia_group(current_user: dict = Depends(auth_handler.decode_token)):
    user_groups = current_user.get("groups", [])
    if FARMACIA_GROUP not in user_groups and ADMIN_GROUP not in user_groups:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Acesso negado. Exclusivo para o setor de Farmácia."
        )
    return current_user

# Endpoints
@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def criar_solicitacao(
    payload: SolicitacaoInput,
    provider: SolicitacaoCoberturaProviderInterface = Depends(get_solicitacao_cobertura_provider)
):
    """Cria uma nova solicitação vinda do AGHU."""
    return await solicitacao_cobertura_controller.criar_solicitacao(payload.model_dump(), provider)

@router.get("", response_model=List[dict])
async def listar_solicitacoes(
    status: Optional[str] = None,
    provider: SolicitacaoCoberturaProviderInterface = Depends(get_solicitacao_cobertura_provider)
):
    """Lista as solicitações do sistema, filtrando opcionalmente por status (ex: PENDENTE, AUTORIZADO, ENTREGUE)."""
    return await solicitacao_cobertura_controller.listar_solicitacoes(status, provider)

@router.get("/{id}", response_model=dict)
async def obter_solicitacao(
    id: int,
    provider: SolicitacaoCoberturaProviderInterface = Depends(get_solicitacao_cobertura_provider)
):
    """Obtém os detalhes de uma solicitação específica."""
    return await solicitacao_cobertura_controller.obter_solicitacao(id, provider)

@router.put("/{id}/auditar", response_model=dict)
async def auditar_solicitacao(
    id: int,
    payload: AuditoriaInput,
    current_user: dict = Depends(verify_cciras_group),
    provider: SolicitacaoCoberturaProviderInterface = Depends(get_solicitacao_cobertura_provider)
):
    """CCIRAS: Autoriza ou nega a solicitação e seus itens."""
    auditor = current_user.get("username", "auditor_desconhecido")
    return await solicitacao_cobertura_controller.auditar_solicitacao(
        solicitacao_id=id,
        auditor=auditor,
        status_geral=payload.status_geral,
        justificativa=payload.justificativa,
        itens_atualizados=[item.model_dump() for item in payload.itens],
        provider=provider
    )

@router.put("/{id}/entregar", response_model=dict)
async def entregar_solicitacao(
    id: int,
    current_user: dict = Depends(verify_farmacia_group),
    provider: SolicitacaoCoberturaProviderInterface = Depends(get_solicitacao_cobertura_provider)
):
    """Farmácia: Registra a entrega dos itens liberados."""
    farmaceutico = current_user.get("username", "farmaceutico_desconhecido")
    return await solicitacao_cobertura_controller.entregar_solicitacao(
        solicitacao_id=id,
        farmaceutico=farmaceutico,
        provider=provider
    )

@router.post("/importar", response_model=dict)
async def importar_solicitacoes(
    current_user: dict = Depends(auth_handler.decode_token),
    app_db: AsyncSession = Depends(get_app_db_session)
):
    """Importa solicitações pendentes do AGHU manualmente."""
    from ..helpers.aghu_import_service import import_solicitacoes_from_aghu
    
    # Executa a importação
    novas = await import_solicitacoes_from_aghu(app_db)
    return {
        "status": "success",
        "message": f"Sincronização concluída. {novas} novas solicitações importadas.",
        "importadas": novas
    }

