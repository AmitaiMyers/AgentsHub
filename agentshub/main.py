"""Application factory: one service layer behind REST, MCP, A2A and the web lite agent."""
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from mcp.server.transport_security import TransportSecuritySettings
from pydantic import ValidationError

from agentshub.config import Settings, load_settings
from agentshub.db import Database
from agentshub.errors import DomainError
from agentshub.interfaces import a2a, rest
from agentshub.interfaces.mcp_server import build_mcp_server
from agentshub.web import routes as web

STATIC_DIR = Path(__file__).parent / "web" / "static"
API_PREFIXES = ("/v1", "/a2a", "/mcp", "/.well-known")


def _is_api_request(request: Request) -> bool:
    return request.url.path.startswith(API_PREFIXES)


def _error_response(request: Request, status_code: int, error: str, message: str) -> Response:
    if _is_api_request(request):
        return JSONResponse({"error": error, "message": message}, status_code=status_code)
    return web.error_page(request, status_code, message)


def _register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def domain_error(request: Request, exc: DomainError) -> Response:
        return _error_response(request, exc.status_code, type(exc).__name__, exc.message)

    @app.exception_handler(ValidationError)
    async def validation_error(request: Request, exc: ValidationError) -> Response:
        details = "; ".join(f"{'.'.join(str(part) for part in item['loc'])}: {item['msg']}"
                            for item in exc.errors(include_url=False))
        return _error_response(request, 400, "ValidationFailed", details)


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings if settings is not None else load_settings()
    database = Database(settings.database_url)
    database.create_schema()
    mcp_server = build_mcp_server(database, settings)
    mcp_app = mcp_server.streamable_http_app(
        streamable_http_path="/mcp", stateless_http=True, json_response=True,
        transport_security=TransportSecuritySettings(
            enable_dns_rebinding_protection=True,
            allowed_hosts=list(settings.allowed_hosts),
            allowed_origins=[settings.base_url, "http://127.0.0.1:*", "http://localhost:*"],
        ),
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        async with mcp_server.session_manager.run():
            yield

    app = FastAPI(title="AgentsHub", version="0.1.0", lifespan=lifespan,
                  description="A neutral, verified exchange where AI agents post needs and offers.")
    app.state.settings = settings
    app.state.database = database
    app.include_router(rest.router)
    app.include_router(a2a.router)
    app.include_router(web.router)
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    app.router.routes.extend(mcp_app.routes)
    _register_error_handlers(app)
    return app
