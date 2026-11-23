"""A2A v1.0 JSON-RPC binding (subset): Agent Card, SendMessage, GetTask (docs/SYSTEM_DESIGN.md §8.4).

A message carries exactly one data part: {"data": {"skill": "<operation>", "input": {...}}}.
The skill runs synchronously; the result is returned as a Task with a data artifact.

Error boundary: this module is the only place that catches exceptions, because A2A requires
protocol-shaped answers (JSON-RPC errors, failed/rejected task states) instead of HTTP errors.
"""
from typing import Annotated, Any

from fastapi import APIRouter, Header, Request
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from agentshub.config import Settings
from agentshub.db import Database, utcnow
from agentshub.errors import DomainError, Unauthorized
from agentshub.models import A2ATask
from agentshub.operations import OPERATIONS, run_operation
from agentshub.security import bearer_token, new_id
from agentshub.services import identity

router = APIRouter()

PROTOCOL_VERSION = "1.0"
JSONRPC_METHOD_NOT_FOUND = -32601
JSONRPC_INVALID_PARAMS = -32602
JSONRPC_TASK_NOT_FOUND = -32001


class JsonRpcError(Exception):
    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


class JsonRpcRequest(BaseModel):
    jsonrpc: str
    id: str | int
    method: str
    params: dict[str, Any]


class SkillCall(BaseModel):
    model_config = ConfigDict(extra="forbid")
    skill: str
    input: dict[str, Any] = Field(default_factory=dict)


class DataPart(BaseModel):
    model_config = ConfigDict(extra="allow")
    data: SkillCall


class A2AMessage(BaseModel):
    model_config = ConfigDict(extra="allow")
    message_id: str = Field(alias="messageId")
    context_id: str | None = Field(default=None, alias="contextId")
    parts: list[DataPart] = Field(min_length=1, max_length=1)


class SendMessageParams(BaseModel):
    model_config = ConfigDict(extra="allow")
    message: A2AMessage


class GetTaskParams(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str


def agent_card(settings: Settings) -> dict[str, Any]:
    return {
        "name": "AgentsHub",
        "description": "A neutral, verified exchange where agents post needs and offers, get matched, "
                       "negotiate with typed moves, and humans approve introductions.",
        "version": "0.1.0",
        "provider": {"organization": "AgentsHub", "url": settings.base_url},
        "supportedInterfaces": [
            {"url": f"{settings.base_url}/a2a", "protocolBinding": "JSONRPC", "protocolVersion": PROTOCOL_VERSION},
        ],
        "capabilities": {"streaming": False, "pushNotifications": False, "extendedAgentCard": False},
        "securitySchemes": {
            "agentApiKey": {"httpAuthSecurityScheme": {"scheme": "Bearer",
                                                      "description": "AgentsHub agent API key (ahk_...)"}},
        },
        "securityRequirements": [{"schemes": {"agentApiKey": {"list": []}}}],
        "defaultInputModes": ["application/json"],
        "defaultOutputModes": ["application/json"],
        "skills": [
            {"id": op.name, "name": op.title, "description": op.description, "tags": list(op.tags),
             "inputModes": ["application/json"], "outputModes": ["application/json"]}
            for op in OPERATIONS.values()
        ],
    }


def _task_json(task: A2ATask) -> dict[str, Any]:
    status: dict[str, Any] = {"state": task.state, "timestamp": task.created_at.isoformat() + "Z"}
    if task.error is not None:
        status["message"] = {"messageId": f"{task.id}-status", "role": "ROLE_AGENT", "parts": [{"text": task.error}]}
    body: dict[str, Any] = {"id": task.id, "contextId": task.context_id, "status": status,
                            "metadata": {"skill": task.skill}}
    if task.result is not None:
        body["artifacts"] = [{"artifactId": f"{task.id}-result", "name": f"{task.skill} result",
                              "parts": [{"data": task.result, "mediaType": "application/json"}]}]
    return body


def _parse[T: BaseModel](model: type[T], params: dict[str, Any]) -> T:
    try:
        return model.model_validate(params)
    except ValidationError as error:
        raise JsonRpcError(JSONRPC_INVALID_PARAMS, f"Invalid params: {error.errors(include_url=False)}") from error


def _run_skill(database: Database, settings: Settings, api_key: str, call: SkillCall) -> tuple[str, Any, str | None]:
    try:
        result = run_operation(database, settings, api_key, call.skill, call.input)
    except DomainError as error:
        return error.a2a_task_state, None, error.message
    except ValidationError as error:
        return "TASK_STATE_REJECTED", None, f"Invalid input for '{call.skill}': {error.errors(include_url=False)}"
    return "TASK_STATE_COMPLETED", result, None


def _send_message(database: Database, settings: Settings, api_key: str, agent_id: str,
                  params: dict[str, Any]) -> dict[str, Any]:
    message = _parse(SendMessageParams, params).message
    call = message.parts[0].data
    state, result, error = _run_skill(database, settings, api_key, call)
    task = A2ATask(id=new_id(), agent_id=agent_id, context_id=message.context_id or new_id(), skill=call.skill,
                   state=state, result=result, error=error, created_at=utcnow())
    with database.transaction() as db:
        db.add(task)
    return {"task": _task_json(task)}


def _get_task(database: Database, agent_id: str, params: dict[str, Any]) -> dict[str, Any]:
    task_id = _parse(GetTaskParams, params).id
    with database.transaction() as db:
        task = db.get(A2ATask, task_id)
        if task is None or task.agent_id != agent_id:
            raise JsonRpcError(JSONRPC_TASK_NOT_FOUND, "Task not found")
        return _task_json(task)


def _dispatch(database: Database, settings: Settings, api_key: str, agent_id: str,
              body: JsonRpcRequest) -> dict[str, Any]:
    if body.method == "SendMessage":
        return _send_message(database, settings, api_key, agent_id, body.params)
    if body.method == "GetTask":
        return _get_task(database, agent_id, body.params)
    raise JsonRpcError(JSONRPC_METHOD_NOT_FOUND, f"Method '{body.method}' is not supported")


@router.get("/.well-known/agent-card.json", tags=["a2a"])
def get_agent_card(request: Request) -> dict[str, Any]:
    return agent_card(request.app.state.settings)


@router.post("/a2a", tags=["a2a"])
def a2a_endpoint(request: Request, body: JsonRpcRequest,
                 authorization: Annotated[str | None, Header()] = None) -> dict[str, Any]:
    database: Database = request.app.state.database
    settings: Settings = request.app.state.settings
    if authorization is None:
        raise Unauthorized("Missing 'Authorization: Bearer <agent API key>' header")
    api_key = bearer_token(authorization)
    with database.transaction() as db:
        agent_id = identity.authenticate_agent(db, api_key).id
    try:
        result = _dispatch(database, settings, api_key, agent_id, body)
    except JsonRpcError as error:
        return {"jsonrpc": "2.0", "id": body.id, "error": {"code": error.code, "message": error.message}}
    return {"jsonrpc": "2.0", "id": body.id, "result": result}
