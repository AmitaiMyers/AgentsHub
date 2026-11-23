"""Shared fixtures: a fresh app and database per test, plus helpers to build principals and intents."""
import re
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from agentshub.config import Settings
from agentshub.main import create_app
from agentshub.models import OutboxEmail

ADMIN_TOKEN = "admin-secret-for-tests"


def make_settings(tmp_path: Path, base_url: str = "http://testserver") -> Settings:
    return Settings(database_url=f"sqlite:///{tmp_path / 'test.db'}", base_url=base_url, admin_token=ADMIN_TOKEN,
                    show_dev_outbox=True, allowed_hosts=("127.0.0.1:*", "localhost:*", "testserver"))


@pytest.fixture
def client(tmp_path: Path) -> Iterator[TestClient]:
    with TestClient(create_app(make_settings(tmp_path))) as test_client:
        yield test_client


@dataclass
class Party:
    principal_id: str
    principal_token: str
    api_key: str
    email: str

    @property
    def agent_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"}

    @property
    def principal_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.principal_token}"}


def latest_link(client: TestClient, email: str, path: str) -> str:
    """Return the most recent outbox link to `path` sent to `email` (path + query)."""
    with client.app.state.database.transaction() as db:
        bodies = [row.body for row in db.scalars(select(OutboxEmail).where(OutboxEmail.to_email == email)
                                                  .order_by(OutboxEmail.created_at.desc()))]
    base_url = client.app.state.settings.base_url
    for body in bodies:
        match = re.search(rf"{re.escape(base_url)}({re.escape(path)}\S*)", body)
        if match:
            return match.group(1)
    raise AssertionError(f"No e-mail to {email} links to {path}")


def verification_token(client: TestClient, email: str) -> str:
    return latest_link(client, email, "/verify-email").split("token=", 1)[1]


def register(client: TestClient, *, kind: str, name: str, email: str, org_domain: str | None = None,
             verify_email: bool = True, verify_domain: bool = False) -> Party:
    body: dict[str, Any] = {"kind": kind, "display_name": name, "contact_email": email}
    if org_domain is not None:
        body["org_domain"] = org_domain
    response = client.post("/v1/principals", json=body)
    assert response.status_code == 201, response.text
    registered = response.json()
    token = registered["principal_token"]
    principal_headers = {"Authorization": f"Bearer {token}"}
    if verify_email:
        verified = client.post("/v1/principals/verify-email", json={"token": verification_token(client, email)})
        assert verified.status_code == 200, verified.text
    if verify_domain:
        domain = client.post("/v1/principals/verify-domain", headers=principal_headers)
        assert domain.status_code == 200, domain.text
    agent = client.post("/v1/agents", json={"name": f"{name} agent"}, headers=principal_headers)
    assert agent.status_code == 201, agent.text
    return Party(registered["principal"]["id"], token, agent.json()["api_key"], email)


def employer(client: TestClient, name: str = "Acme AI", domain: str = "acme.ai") -> Party:
    return register(client, kind="organization", name=name, email=f"talent@{domain}", org_domain=domain,
                    verify_domain=True)


def seeker(client: TestClient, name: str = "Dana Cohen", email: str = "dana@example.com") -> Party:
    return register(client, kind="person", name=name, email=email)


def job_offer_payload(**overrides: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "title": "Senior ML Engineer", "company_name": "Acme AI", "seniority": "senior",
        "skills_required": ["Python", "PyTorch"], "skills_preferred": ["Kubernetes", "CUDA"],
        "remote_policy": "remote", "locations": [], "salary_min": 150000, "salary_max": 190000,
        "currency": "USD", "visa_sponsorship": False, "description": "Train and ship models.",
    }
    payload.update(overrides)
    return payload


def job_seek_payload(**overrides: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "headline": "ML engineer, 7 years", "seniority": "senior", "skills": ["python", "pytorch", "kubernetes"],
        "interests": ["CUDA"], "years_experience": 7, "remote_preferences": ["remote"], "locations": [],
        "salary_floor": 160000, "currency": "USD", "needs_visa_sponsorship": False,
        "summary": "Built recommendation systems.", "deal_breakers": ["on-call every week"],
    }
    payload.update(overrides)
    return payload


def post_intent(client: TestClient, party: Party, intent_type: str, payload: dict[str, Any]) -> str:
    response = client.post("/v1/intents", json={"intent_type": intent_type, "payload": payload},
                           headers=party.agent_headers)
    assert response.status_code == 201, response.text
    return response.json()["id"]


def open_session(client: TestClient, offer_party: Party, offer_id: str, seek_party: Party, seek_id: str) -> str:
    first = client.post("/v1/interests", json={"from_intent_id": seek_id, "to_intent_id": offer_id},
                        headers=seek_party.agent_headers)
    assert first.json() == {"status": "waiting_for_counterpart", "session_id": None}, first.text
    second = client.post("/v1/interests", json={"from_intent_id": offer_id, "to_intent_id": seek_id},
                         headers=offer_party.agent_headers)
    assert second.json()["status"] == "session_opened", second.text
    return second.json()["session_id"]
