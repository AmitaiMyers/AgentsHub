"""ASGI entry point: `uvicorn agentshub.asgi:app`. Settings come from AGENTSHUB_* environment variables."""
from agentshub.main import create_app

app = create_app()
