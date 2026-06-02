from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

from .resources.database import DatabaseManager, Base
from .models.refresh_token import RefreshToken
from .models.solicitacao import SolicitacaoCobertura, ItemSolicitacao

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")

    # Initialize AGHU DB Manager and store in app.state
    aghu_dsn = os.getenv("POSTGRES_DSN")
    if aghu_dsn:
        app.state.aghu_db = DatabaseManager(aghu_dsn)
        print("AGHU PostgreSQL connection pool initialized.")
    else:
        print("WARNING: POSTGRES_DSN not found. Skipping AGHU DB initialization.")

    # Initialize App DB Manager (SQLite) and store in app.state
    app_dsn = os.getenv("SQLITE_DSN")
    if not app_dsn:
        raise ValueError("SQLITE_DSN not found in environment variables.")
    app.state.app_db = DatabaseManager(app_dsn)
    print("App SQLite connection pool initialized.")

    # Create tables for App DB (if they don't exist) - for development only, Alembic handles this in production
    async with app.state.app_db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("App SQLite tables checked/created.")

    # Background task for periodic AGHU import (every 30 minutes)
    import asyncio
    from .helpers.aghu_import_service import import_solicitacoes_from_aghu
    
    async def periodic_import():
        await asyncio.sleep(5) # Delay inicial suave
        while True:
            try:
                print("Starting periodic AGHU import background task...")
                async with app.state.app_db.async_session_maker() as session:
                    # Se tiver banco do AGHU (Postgres) configurado, passa a sessão
                    aghu_session = None
                    if hasattr(app.state, 'aghu_db') and app.state.aghu_db:
                        try:
                            aghu_session = app.state.aghu_db.async_session_maker()
                        except Exception:
                            pass
                    
                    try:
                        await import_solicitacoes_from_aghu(session, aghu_session)
                    finally:
                        if aghu_session:
                            await aghu_session.close()
            except Exception as e:
                print(f"Error in AGHU periodic import: {e}")
            await asyncio.sleep(1800) # 30 minutos (30 * 60)

    # Inicia a tarefa em background
    app.state.import_task = asyncio.create_task(periodic_import())
    print("AGHU periodic import background task scheduled (every 30m).")

    yield

    # Shutdown
    print("Shutting down...")
    # Cancela a tarefa em background no shutdown
    if hasattr(app.state, 'import_task') and app.state.import_task:
        app.state.import_task.cancel()
        print("AGHU periodic import background task cancelled.")
    if hasattr(app.state, 'aghu_db') and app.state.aghu_db:
        await app.state.aghu_db.close_connection()
        print("AGHU PostgreSQL connection pool closed.")
    if hasattr(app.state, 'app_db') and app.state.app_db:
        await app.state.app_db.close_connection()
        print("App SQLite connection pool closed.")

app = FastAPI(
    title="Esqueleto de Aplicação Web Full-Stack",
    description="Aplicação Backend monolítica (API REST) em Python/FastAPI, com foco em acesso e agregação de dados heterogêneos.",
    version="1.0.0",
    lifespan=lifespan,
)

# Serve o frontend Vue 3 empacotado
app.mount("/assets", StaticFiles(directory="src/static/dist/assets"), name="assets")
# Outros arquivos estáticos na raiz do dist (como favicon.ico)
app.mount("/static", StaticFiles(directory="src/static/dist"), name="static")

# Placeholder para incluir os roteadores da API
from .routers import paciente, auth, admin, aih, bpa, material, solicitacao_cobertura
app.include_router(paciente.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(aih.router)
app.include_router(bpa.router)
app.include_router(material.router)
app.include_router(solicitacao_cobertura.router)

@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    """
    Serve o arquivo index.html para todas as rotas que não são da API ou arquivos estáticos.
    Isso é necessário para que o roteamento do Vue (SPA) funcione.
    """
    # Se a rota começa com 'api', deixa o roteador do FastAPI lidar
    if full_path.startswith("api"):
        raise HTTPException(status_code=404, detail="API route not found")
    
    index_path = os.path.join("src", "static", "dist", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "Frontend build not found"}

# Exemplo:
# from .routers import aih, bpa, material
# app.include_router(aih.router)
# app.include_router(bpa.router)
# app.include_router(material.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
