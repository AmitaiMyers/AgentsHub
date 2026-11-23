"""A2A JSON-RPC binding and Agent Card."""
from typing import Any

from agentshub.operations import OPERATIONS
from tests.conftest import employer, job_offer_payload, seeker


def rpc(method: str, params: dict[str, Any], request_id: int = 1) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "method": method, "params": params}


def skill_message(skill: str, skill_input: dict[str, Any]) -> dict[str, Any]:
    return {"message": {"messageId": "m-1", "role": "ROLE_USER",
                        "parts": [{"data": {"skill": skill, "input": skill_input}}]}}


def test_agent_card_lists_every_operation(client):
    card = client.get("/.well-known/agent-card.json").json()
    assert card["supportedInterfaces"] == [{"url": "http://testserver/a2a", "protocolBinding": "JSONRPC",
                                            "protocolVersion": "1.0"}]
    assert {skill["id"] for skill in card["skills"]} == set(OPERATIONS)


def test_send_message_runs_a_skill_and_get_task_returns_it(client):
    acme = employer(client)
    sent = client.post("/a2a", headers=acme.agent_headers,
                       json=rpc("SendMessage", skill_message("post_intent", {"intent_type": "job_offer",
                                                                             "payload": job_offer_payload()})))
    task = sent.json()["result"]["task"]
    assert task["status"]["state"] == "TASK_STATE_COMPLETED"
    intent = task["artifacts"][0]["parts"][0]["data"]
    assert intent["intent_type"] == "job_offer"

    fetched = client.post("/a2a", headers=acme.agent_headers, json=rpc("GetTask", {"id": task["id"]}, 2)).json()
    assert fetched["result"]["id"] == task["id"]

    other = seeker(client)
    hidden = client.post("/a2a", headers=other.agent_headers, json=rpc("GetTask", {"id": task["id"]}, 3)).json()
    assert hidden["error"]["code"] == -32001


def test_rule_violations_become_rejected_tasks(client):
    dana = seeker(client)
    sent = client.post("/a2a", headers=dana.agent_headers,
                       json=rpc("SendMessage", skill_message("post_intent", {"intent_type": "job_offer",
                                                                             "payload": job_offer_payload()})))
    status = sent.json()["result"]["task"]["status"]
    assert status["state"] == "TASK_STATE_REJECTED"
    assert "Only organization principals" in status["message"]["parts"][0]["text"]

    unknown = client.post("/a2a", headers=dana.agent_headers, json=rpc("SendMessage", skill_message("hack", {})))
    assert unknown.json()["result"]["task"]["status"]["state"] == "TASK_STATE_REJECTED"


def test_protocol_errors_are_json_rpc_errors(client):
    dana = seeker(client)
    no_message = client.post("/a2a", headers=dana.agent_headers, json=rpc("SendMessage", {})).json()
    assert no_message["error"]["code"] == -32602
    unknown_method = client.post("/a2a", headers=dana.agent_headers, json=rpc("ListTasks", {})).json()
    assert unknown_method["error"]["code"] == -32601
    assert client.post("/a2a", json=rpc("GetTask", {"id": "x"})).status_code == 401
