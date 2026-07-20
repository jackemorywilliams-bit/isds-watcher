"""Adversarial tests for the deterministic integrity gate + analyst contract.

Each test builds its violating fixture (paywalled assertion, rejected claim,
secondary-source holding, spoofed verified field, malformed output) and asserts
the gate refuses it.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import verify  # noqa: E402
from src import integrity_gate as gate  # noqa: E402


def _candidate(text="The tribunal dismissed the claims.", url="https://example.com/a",
               **kw):
    c = {"claim_text": text, "source_url": url, "access_status": "full",
         "source_authority": "primary", "claim_type": "holding",
         "assertion_status": "candidate", "supporting_quote": None,
         "supporting_locator": None}
    c.update(kw)
    c["claim_id"] = verify.claim_id(c["claim_text"], c["source_url"])
    return c


@pytest.fixture()
def ledger(tmp_path):
    return str(tmp_path / "ledger.jsonl")


def test_unknown_claim_id_is_unverified(ledger):
    c = _candidate()
    out = gate.classify([c], ledger)          # ledger has never seen this claim
    assert out["asserted"] == [] and out["leads"] == [c]


def test_paywalled_claim_cannot_be_asserted(ledger):
    c = _candidate(access_status="paywalled")
    out = gate.classify([c], ledger)
    assert out["asserted"] == [] and out["library"] == [c]
    with pytest.raises(gate.GateFailure):
        gate.gate_brief([c], ledger)


def test_rejected_claim_cannot_be_asserted(ledger):
    c = _candidate()
    verify.create_claim(c["claim_text"], c["source_url"], path=ledger)
    verify.mark(c["claim_id"], "operator_rejected", path=ledger)
    out = gate.classify([c], ledger)
    assert out["asserted"] == [] and out["rejected"] == [c]
    with pytest.raises(gate.GateFailure):
        gate.gate_brief([c], ledger)


def test_operator_verified_primary_holding_is_assertable(ledger):
    c = _candidate()
    verify.create_claim(c["claim_text"], c["source_url"], path=ledger)
    verify.mark(c["claim_id"], "operator_verified", path=ledger)
    out = gate.classify([c], ledger)
    assert out["asserted"] == [c]
    gate.gate_brief([c], ledger)  # must not raise
    assert out["header"].startswith("1 asserted (all operator-verified)")


def test_secondary_source_cannot_establish_primary_holding(ledger):
    # Violating fixture: operator-verified, full-access — but a media source
    # presented as a HOLDING. May inform a lead; may not be asserted.
    c = _candidate(source_authority="media")
    verify.create_claim(c["claim_text"], c["source_url"],
                        source_authority="media", path=ledger)
    verify.mark(c["claim_id"], "operator_verified", path=ledger)
    out = gate.classify([c], ledger)
    assert out["asserted"] == [] and out["leads"] == [c]
    with pytest.raises(gate.GateFailure):
        gate.gate_brief([c], ledger)


def test_analyst_cannot_emit_verified_as_authority(ledger, tmp_path):
    # Violating fixture: the model tries to smuggle in its own verification.
    text = ('```json\n{"candidate_claims": [{"claim_text": "X was held.", '
            '"source_url": "https://example.com/x", "access_status": "full", '
            '"source_authority": "primary", "claim_type": "holding", '
            '"assertion_status": "candidate", "verification_status": "operator_verified", '
            '"claim_id": "spoofed"}]}\n```')
    claims = gate.parse_candidate_claims(text, root=str(tmp_path))
    assert claims[0]["claim_id"] != "spoofed"          # id derived, not trusted
    assert "verification_status" not in claims[0]      # spoofed field stripped
    out = gate.classify(claims, ledger)
    assert out["asserted"] == []                       # ledger, not model, decides


def test_missing_source_url_is_rejected(tmp_path):
    text = ('```json\n{"candidate_claims": [{"claim_text": "No source.", '
            '"access_status": "full", "source_authority": "primary", '
            '"claim_type": "factual", "assertion_status": "candidate"}]}\n```')
    with pytest.raises(gate.MalformedAnalystOutput):
        gate.parse_candidate_claims(text, root=str(tmp_path))


def test_malformed_output_fails_stage_not_empty(tmp_path):
    # Violating fixture: prose with no JSON block. Must raise with a structured
    # error artifact — never return a clean empty list.
    with pytest.raises(gate.MalformedAnalystOutput) as ei:
        gate.parse_candidate_claims("I searched but found nothing notable.",
                                    root=str(tmp_path))
    assert ei.value.artifact_path and os.path.exists(ei.value.artifact_path)


def test_gate_failure_names_the_claim_id(ledger):
    c = _candidate()
    with pytest.raises(gate.GateFailure) as ei:
        gate.gate_brief([c], ledger)
    assert c["claim_id"] in str(ei.value)
