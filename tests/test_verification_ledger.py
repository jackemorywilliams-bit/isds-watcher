"""Adversarial tests for the append-only verification ledger (Protocol Part 1).

Every test here encodes an invariant that MUST be able to fail: each builds the
violating fixture (the forbidden write, the mutated claim, the stale snapshot, the
fuzzy lookup) and asserts the ledger refuses to treat it as verified.
"""

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import verify  # noqa: E402


@pytest.fixture()
def ledger(tmp_path):
    return str(tmp_path / "verification_ledger.jsonl")


CLAIM = ("The tribunal dismissed all claims for failure to withdraw the "
         "concurrent Chinese court proceedings.")
URL = "https://www.italaw.com/cases/5973"


def test_machine_cannot_mark_operator_verified(ledger):
    cid = verify.create_claim(CLAIM, URL, path=ledger)
    # Violating fixture: an automated caller tries to append a verification event.
    with pytest.raises(PermissionError):
        verify.append_event({"event": "verification_changed", "claim_id": cid,
                             "prior_status": "unverified",
                             "new_status": "operator_verified",
                             "actor": "pipeline-bot"}, ledger)
    assert verify.current_status(cid, verify.replay(ledger)) == "unverified"


def test_reachable_url_is_not_verified(ledger):
    cid = verify.create_claim(CLAIM, URL, path=ledger)
    # Violating fixture: a successful reachability probe must not read as truth.
    verify.record_metadata(cid, "reachability", {"http_status": 200, "ok": True},
                           path=ledger)
    assert verify.current_status(cid, verify.replay(ledger)) == "unverified"


def test_same_url_different_claims_do_not_collide(ledger):
    a = verify.create_claim("Claim one about the award.", URL, path=ledger)
    b = verify.create_claim("Claim two about the award.", URL, path=ledger)
    assert a != b


def test_claim_text_mutation_invalidates_verification(ledger):
    cid = verify.create_claim(CLAIM, URL, path=ledger)
    verify.mark(cid, "operator_verified", path=ledger)
    mutated = verify.claim_id(CLAIM.replace("dismissed", "upheld"), URL)
    assert mutated != cid
    assert verify.current_status(mutated, verify.replay(ledger)) == "unverified"


def test_changed_source_locator_invalidates_verification(ledger):
    cid = verify.create_claim(CLAIM, URL, path=ledger)
    verify.mark(cid, "operator_verified", path=ledger)
    moved = verify.claim_id(CLAIM, "https://example.com/mirror/5973")
    assert moved != cid
    assert verify.current_status(moved, verify.replay(ledger)) == "unverified"


def test_changed_source_snapshot_requires_reverification(ledger):
    cid = verify.create_claim(CLAIM, URL, source_snapshot="sha-one", path=ledger)
    verify.mark(cid, "operator_verified", path=ledger)
    st = verify.replay(ledger)[cid]
    assert verify.verified_against_current_snapshot(st)
    # Violating fixture: the artifact at the locator changes after verification.
    verify.record_metadata(cid, "snapshot_observed", {"sha256": "sha-two"}, path=ledger)
    st = verify.replay(ledger)[cid]
    assert st["status"] == "operator_verified"          # history stays valid
    assert not verify.verified_against_current_snapshot(st)  # but not against NEW artifact


def test_fuzzy_match_cannot_satisfy_lookup(ledger):
    cid = verify.create_claim(CLAIM, URL, path=ledger)
    verify.mark(cid, "operator_verified", path=ledger)
    claims = verify.replay(ledger)
    # Violating fixture: near-identical text (one word off) and a truncated id.
    near = verify.claim_id(CLAIM.replace("all claims", "the claims"), URL)
    assert verify.current_status(near, claims) == "unverified"
    assert verify.current_status(cid[:16], claims) == "unverified"


def test_verification_history_recoverable_from_log(ledger):
    cid = verify.create_claim(CLAIM, URL, path=ledger)
    verify.mark(cid, "operator_verified", path=ledger)
    verify.mark(cid, "operator_rejected", note="quote did not check out", path=ledger)
    verify.mark(cid, "operator_verified", note="rechecked against award text", path=ledger)
    st = verify.replay(ledger)[cid]
    transitions = [(e["prior_status"], e["new_status"]) for e in st["events"]
                   if e["event"] == "verification_changed"]
    assert transitions == [("unverified", "operator_verified"),
                           ("operator_verified", "operator_rejected"),
                           ("operator_rejected", "operator_verified")]
    assert st["status"] == "operator_verified"


def test_ledger_is_append_only_jsonl(ledger):
    cid = verify.create_claim(CLAIM, URL, path=ledger)
    verify.mark(cid, "operator_verified", path=ledger)
    lines = open(ledger, encoding="utf-8").read().strip().splitlines()
    assert len(lines) == 2 and all(json.loads(ln) for ln in lines)


def test_canonicalization_rules():
    a = verify.claim_id("  The   tribunal\nheld X. ", "HTTPS://Example.COM/p/?utm_source=x#frag")
    b = verify.claim_id("The tribunal held X.", "https://example.com/p")
    assert a == b
    # Content-bearing query params are preserved (different resource, different id).
    c = verify.claim_id("The tribunal held X.", "https://example.com/p?id=2")
    assert c != b


def test_malformed_lines_reported_not_dropped(ledger):
    verify.create_claim(CLAIM, URL, path=ledger)
    with open(ledger, "a", encoding="utf-8") as fh:
        fh.write("{not valid json\n")
    claims = verify.replay(ledger)
    assert "_malformed" in claims and len(claims["_malformed"]["lines"]) == 1


# ---- prefix resolution on operator marks (fail-closed) ----

def test_mark_resolves_unique_prefix(tmp_path):
    path = str(tmp_path / "ledger.jsonl")
    cid = verify.create_claim("Prefix test claim.", "https://example.org/a", path=path)
    ev = verify.mark(cid[:16], "operator_verified", note="via prefix", path=path)
    assert ev["claim_id"] == cid
    assert verify.replay(path)[cid]["status"] == "operator_verified"


def test_mark_unknown_id_fails_closed(tmp_path):
    path = str(tmp_path / "ledger.jsonl")
    verify.create_claim("Prefix test claim.", "https://example.org/a", path=path)
    with pytest.raises(ValueError, match="unknown claim id"):
        verify.mark("deadbeef00000000", "operator_verified", path=path)


def test_mark_empty_or_ambiguous_prefix_fails_closed(tmp_path):
    path = str(tmp_path / "ledger.jsonl")
    verify.create_claim("Claim one.", "https://example.org/1", path=path)
    verify.create_claim("Claim two.", "https://example.org/2", path=path)
    with pytest.raises(ValueError):
        verify.mark("", "operator_verified", path=path)
