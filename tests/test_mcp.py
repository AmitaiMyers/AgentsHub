"""MCP over real Streamable HTTP, using the official MCP client."""
import asyncio
import socket
import threading
import time
from collections.abc import Iterator
from pathlib import Path

import httpx2
import pytest
import uvicorn
from fastapi.testclient import TestClient
from mcp import Client
from mcp.client.streamable_http import streamable_http_client

from agentshub.main import create_app
from agentshub.operations import OPERATIONS
from tests.conftest import employer, job_offer_payload, make_settings


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@pytest.fixture
def live_server(tmp_path: Path) -> Iterator[tuple[str, TestClient]]:
    port = _free_port()
    base_url = f"http://127.0.0.1:{port}"
    app = create_app(make_settings(tmp_path, base_url=base_url))
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning"))
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    deadline = time.monotonic() + 10
    while not server.started:
        assert time.monotonic() < deadline, "server did not start"
        time.sleep(0.05)
    rest_client = TestClient(app, base_url="http://testserver")
    yield base_url, rest_client
    server.should_exit = True
    thread.join(timeout=10)


def _mcp_client(base_url: str, api_key: str | None) -> Client:
    headers = {"Authorization": f"Bearer {api_key}"} if api_key is not None else {}
    return Client(streamable_http_client(f"{base_url}/mcp", http_client=httpx2.AsyncClient(headers=headers)))


def test_mcp_tools_mirror_operations_and_post_an_intent(live_server):
    base_url, rest_client = live_server
    acme = employer(rest_client)

    async def scenario() -> tuple[set[str], dict, dict]:
        async with _mcp_client(base_url, acme.api_key) as client:
            tools = {tool.name for tool in (await client.list_tools()).tools}
            posted = await client.call_tool("post_intent", {"intent_type": "job_offer", "payload": job_offer_payload()})
            listed = await client.call_tool("list_my_intents", {})
            return tools, posted.structured_content, listed.structured_content

    tools, posted, listed = asyncio.run(scenario())
    assert tools == set(OPERATIONS)
    assert posted["intent_type"] == "job_offer"
    assert [item["id"] for item in listed["items"]] == [posted["id"]]


def test_mcp_tool_errors_carry_the_domain_message(live_server):
    base_url, rest_client = live_server
    acme = employer(rest_client)

    async def scenario():
        async with _mcp_client(base_url, acme.api_key) as client:
            bad = await client.call_tool("post_intent", {"intent_type": "job_offer",
                                                         "payload": job_offer_payload(age=40)})
        async with _mcp_client(base_url, None) as anonymous:
            unauthenticated = await anonymous.call_tool("whoami", {})
        return bad, unauthenticated

    bad, unauthenticated = asyncio.run(scenario())
    assert bad.is_error and "Protected-trait" in bad.content[0].text
    assert unauthenticated.is_error and "Authorization" in unauthenticated.content[0].text
