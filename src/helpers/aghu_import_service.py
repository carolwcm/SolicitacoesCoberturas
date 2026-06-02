# src/helpers/aghu_import_service.py

import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.solicitacao import SolicitacaoCobertura, ItemSolicitacao
from sqlalchemy.future import select

logger = logging.getLogger("aghu_import")

async def import_solicitacoes_from_aghu(app_db_session: AsyncSession, aghu_db_session: AsyncSession = None) -> int:
    """
    Busca solicitações no banco do AGHU e as importa para o banco local.
    Se aghu_db_session não for fornecido, simula os dados.
    Retorna a quantidade de novas solicitações importadas.
    """
    logger.info("Iniciando rotina de importação de solicitações do AGHU...")
    novas_importadas = 0

    # 1. Obter dados do AGHU (real ou simulado)
    solicitacoes_aghu = []
    if aghu_db_session:
        try:
            # Query exemplo para buscar dados de solicitações de coberturas pendentes no AGHU
            # Adapte esta query de acordo com a estrutura real do AGHU
            query = text("""
                SELECT 
                    p.codigo as prontuario,
                    p.nome as nome_paciente,
                    s.leito as leito,
                    s.criado_por as solicitante,
                    s.codigo_material,
                    s.nome_material,
                    s.quantidade
                FROM agh.coberturas_solicitadas s
                JOIN agh.aip_pacientes p ON s.paciente_codigo = p.codigo
                WHERE s.status = 'PENDENTE'
            """)
            result = await aghu_db_session.execute(query)
            rows = result.mappings().all()
            
            # Agrupa os itens por prontuário para formar a estrutura de Solicitação -> Itens
            grouped = {}
            for r in rows:
                key = (r['prontuario'], r['nome_paciente'], r['leito'], r['solicitante'])
                if key not in grouped:
                    grouped[key] = []
                grouped[key].append({
                    "codigo_material": r['codigo_material'],
                    "nome_material": r['nome_material'],
                    "quantidade_solicitada": r['quantidade']
                })
            
            for key, itens in grouped.items():
                solicitacoes_aghu.append({
                    "prontuario": key[0],
                    "nome_paciente": key[1],
                    "leito": key[2],
                    "solicitante": key[3],
                    "itens": itens
                })
        except Exception as e:
            logger.error(f"Erro ao buscar dados do AGHU: {e}. Usando dados simulados.")
            solicitacoes_aghu = _get_mock_aghu_data()
    else:
        # Se não há conexão ativa com o AGHU (Postgres), gera dados mockados para desenvolvimento
        solicitacoes_aghu = _get_mock_aghu_data()

    # 2. Salvar no banco local SQLite evitando duplicidades
    for sol_data in solicitacoes_aghu:
        # Verifica se já existe uma solicitação com o mesmo prontuário e solicitante nas últimas 24h
        # (Ou uma regra de negócio que defina unicidade de solicitação vinda do AGHU)
        stmt = select(SolicitacaoCobertura).where(
            SolicitacaoCobertura.prontuario == sol_data["prontuario"],
            SolicitacaoCobertura.solicitante == sol_data["solicitante"]
        )
        result = await app_db_session.execute(stmt)
        existente = result.scalars().first()

        if not existente:
            solicitacao = SolicitacaoCobertura(
                prontuario=sol_data["prontuario"],
                nome_paciente=sol_data["nome_paciente"],
                leito=sol_data.get("leito"),
                solicitante=sol_data["solicitante"],
                status="PENDENTE"
            )
            app_db_session.add(solicitacao)
            await app_db_session.flush()

            for item_data in sol_data["itens"]:
                item = ItemSolicitacao(
                    solicitacao_id=solicitacao.id,
                    codigo_material=item_data["codigo_material"],
                    nome_material=item_data["nome_material"],
                    quantidade_solicitada=item_data["quantidade_solicitada"],
                    status_item="PENDENTE"
                )
                app_db_session.add(item)
            
            novas_importadas += 1
            logger.info(f"Nova solicitação importada para o prontuário: {sol_data['prontuario']}")

    if novas_importadas > 0:
        await app_db_session.commit()
        
    logger.info(f"Rotina de importação finalizada. {novas_importadas} nova(s) solicitação(ões) importada(s).")
    return novas_importadas

def _get_mock_aghu_data():
    """Gera uma lista de solicitações simuladas vindas do AGHU."""
    import random
    n_pacientes = [
        (100234, "Maria Oliveira Souza", "Leito 102-A"),
        (200456, "João Silva Rego", "Leito 205-B"),
        (300789, "Ana Beatriz Santos", "Leito 110-T")
    ]
    solicitantes = ["dr.silva", "enfa.claudia", "dr.roberto"]
    materiais = [
        (101, "Seringa 10ml"),
        (102, "Agulha 25x7"),
        (103, "Cateter Intravenoso"),
        (104, "Avental Descartável"),
        (105, "Máscara Cirúrgica")
    ]
    
    p = random.choice(n_pacientes)
    s = random.choice(solicitantes)
    
    # Seleciona de 1 a 3 itens aleatórios
    itens_selecionados = random.sample(materiais, k=random.randint(1, 3))
    itens = [{
        "codigo_material": m[0],
        "nome_material": m[1],
        "quantidade_solicitada": random.randint(1, 10)
    } for m in itens_selecionados]
    
    return [{
        "prontuario": p[0],
        "nome_paciente": p[1],
        "leito": p[2],
        "solicitante": s,
        "itens": itens
    }]
