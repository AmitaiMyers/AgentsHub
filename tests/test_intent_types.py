from datetime import date

import pytest
from pydantic import ValidationError

from agentshub.errors import ValidationFailed
from agentshub.intent_types import (
    INTENT_TYPES,
    Stage,
    check_pair,
    find_prohibited_keys,
    own_preference_overlap,
    parse_payload,
    validate_terms,
    visible_fields,
)
from tests.conftest import job_offer_payload, job_seek_payload

OFFER, SEEK = INTENT_TYPES["job_offer"], INTENT_TYPES["job_seek"]


def pair(offer_overrides=None, seek_overrides=None):
    offer = parse_payload(OFFER, job_offer_payload(**(offer_overrides or {})))
    seek = parse_payload(SEEK, job_seek_payload(**(seek_overrides or {})))
    return offer, seek


def test_every_field_declares_a_disclosure_stage():
    for spec in INTENT_TYPES.values():
        visible = visible_fields(spec, {name: None for name in spec.payload_model.model_fields}, Stage.HANDOFF)
        assert set(visible) == set(spec.payload_model.model_fields)


def test_company_name_hidden_until_mutual_interest():
    payload = job_offer_payload()
    assert "company_name" not in visible_fields(OFFER, payload, Stage.PUBLIC)
    assert visible_fields(OFFER, payload, Stage.MUTUAL)["company_name"] == "Acme AI"


def test_offer_rejects_inverted_salary_range():
    with pytest.raises(ValidationError, match="salary_min must not exceed salary_max"):
        parse_payload(OFFER, job_offer_payload(salary_min=200000, salary_max=100000))


def test_onsite_offer_requires_locations():
    with pytest.raises(ValidationError, match="locations are required"):
        parse_payload(OFFER, job_offer_payload(remote_policy="onsite", locations=[]))


def test_unknown_payload_fields_are_rejected():
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        parse_payload(SEEK, job_seek_payload(favourite_colour="blue"))


def test_prohibited_keys_found_at_any_depth():
    assert find_prohibited_keys({"attributes": {"Date of Birth": "1990"}, "x": [{"gender": "f"}]}) == \
        ["Date of Birth", "gender"]
    assert find_prohibited_keys(job_seek_payload()) == []


def test_compatible_pair_lists_every_rule():
    offer, seek = pair()
    result = check_pair(OFFER, offer, SEEK, seek)
    assert result.compatible
    assert "seeker has every required skill" in result.rules_passed
    assert check_pair(SEEK, seek, OFFER, offer).compatible


@pytest.mark.parametrize(("offer_overrides", "seek_overrides", "failed_rule"), [
    ({}, {"seniority": "mid"}, "same seniority"),
    ({"salary_max": 155000}, {}, "salary range reaches the seeker's floor"),
    ({}, {"needs_visa_sponsorship": True}, "visa sponsorship available if needed"),
    ({"skills_required": ["Rust"]}, {}, "seeker has every required skill"),
    ({"remote_policy": "onsite", "locations": ["Berlin"]}, {}, "work arrangement accepted by the seeker"),
    ({"remote_policy": "hybrid", "locations": ["Berlin"]},
     {"remote_preferences": ["hybrid"], "locations": ["Paris"]}, "shared location for non-remote work"),
    ({}, {"currency": "EUR"}, "same salary currency"),
])
def test_incompatible_pairs_report_the_failing_rule(offer_overrides, seek_overrides, failed_rule):
    offer, seek = pair(offer_overrides, seek_overrides)
    result = check_pair(OFFER, offer, SEEK, seek)
    assert not result.compatible
    assert result.first_failed_rule == failed_rule


def test_preference_overlap_uses_only_the_requesters_preferences():
    offer, seek = pair()
    assert own_preference_overlap(OFFER, offer, seek) == 1   # the offer prefers Kubernetes; the seeker has it
    assert own_preference_overlap(SEEK, seek, offer) == 1    # the seeker wants CUDA; the role lists it
    offer_without_cuda, _ = pair({"skills_preferred": ["Go"]})
    assert own_preference_overlap(SEEK, seek, offer_without_cuda) == 0


def test_terms_must_sit_inside_the_zone_of_agreement():
    offer, seek = pair()
    good = {"base_salary": 170000, "currency": "USD", "start_date": "2027-01-04", "remote_policy": "remote"}
    assert validate_terms(SEEK, seek, offer, good)["start_date"] == date(2027, 1, 4).isoformat()
    with pytest.raises(ValidationFailed, match="zone of agreement 160000-190000"):
        validate_terms(OFFER, offer, seek, {**good, "base_salary": 150000})
    with pytest.raises(ValidationFailed, match="remote_policy must match"):
        validate_terms(OFFER, offer, seek, {**good, "remote_policy": "onsite"})
