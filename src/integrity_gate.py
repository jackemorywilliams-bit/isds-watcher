"""Deterministic integrity gate — the council's integrity-officer stage.

Replaces the LLM "security officer" for ASSERTION decisions. The model proposes;
the ledger disposes. EXACT claim_id lookup against the append-only verification
ledger (scripts/verify.py) decides what may be asserted:

    operator_verified (primary source, for holdings)  -> ASSERTED finding
    unverified / machine-reachable-only               -> "Unverified leads" only
    paywalled/blocked + unverified                    -> "For professor / library access" only

No fuzzy, similarity, URL-only, or semantic match may satisfy assertion. A
secondary-source claim — even full-access, even operator-verified — may inform a
lead but may not independently establish a primary-source HOLDING.

Also enforces the analyst output contract: the analyst emits JSON
candidate_claims[]; malformed output FAILS the stage with a structured error
artifact — it is never converted into a successful empty result.
"""

from __future__ import annotations

import datetime
import json
import os
import re
import sys

_SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)

import verify  # noqa: E402  scripts/verify.py — ledger + canonical ids

ERROR_DIR = os.path.join("analytics", "errors")

CLAIM_TYPES = {"holding", "procedural", "factual", "interpretive", "lead"}
ASSERTION_STATUSES = {"candidate", "lead"}
ACCESS_STATUSES = {"full", "partial", "paywalled", "blocked", "unavailable"}
AUTHORITIES = {"primary", "official_secondary", "academic_secondary", "media", "unknown"}

_REQUIRED_FIELDS = ("claim_text", "source_url", "access_status", "source_authority",
                    "claim_type", "assertion_status")


class MalformedAnalystOutput(Exception):
    """Analyst stage contract violation. Carries the structured error artifact path."""

    def __init__(self, message: str, artifact_path: str | None = None):
        super().__init__(message)
        self.artifact_path = artifact_path


class GateFailure(Exception):
    """An asserted finding lacks operator verification; names the claim_ids."""

    def __init__(self, claim_ids: list[str]):
        super().__init__("integrity gate FAILED — asserted finding(s) not "
                         "operator_verified: " + ", ".join(claim_ids))
        self.claim_ids = claim_ids


# --- Analyst output contract --------------------------------------------------------

def _write_error_artifact(kind: str, detail: dict, root: str = ".") -> str:
    d = os.path.join(root, ERROR_DIR)
    os.makedirs(d, exist_ok=True)
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = os.path.join(d, f"{ts}-{kind}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"kind": kind, "ts": ts, **detail}, fh, indent=2, ensure_ascii=False)
    return path


def parse_candidate_claims(analyst_text: str, *, root: str = ".") -> list[dict]:
    """Extract and validate the analyst's ``candidate_claims`` JSON block.

    Contract (1f): malformed output MUST fail the stage with a structured error
    artifact and MUST NOT become a successful empty result. The model does not
    decide verification status; any verification-ish field it emits is stripped.
    """
    m = re.search(r"```json\s*(\{.*?\"candidate_claims\".*?\})\s*```",
                  analyst_text or "", re.DOTALL)
    if not m:
        path = _write_error_artifact("analyst-malformed", {
            "error": "no candidate_claims JSON block found",
            "analyst_text_head": (analyst_text or "")[:2000]}, root)
        raise MalformedAnalystOutput("analyst emitted no candidate_claims block", path)
    try:
        payload = json.loads(m.group(1))
        raw = payload["candidate_claims"]
        assert isinstance(raw, list)
    except Exception as exc:  # noqa: BLE001 - any parse/shape failure is contractual
        path = _write_error_artifact("analyst-malformed", {
            "error": f"candidate_claims block unparseable: {exc}",
            "block": m.group(1)[:4000]}, root)
        raise MalformedAnalystOutput(f"candidate_claims unparseable: {exc}", path) from exc

    problems: list[str] = []
    claims: list[dict] = []
    for i, c in enumerate(raw):
        if not isinstance(c, dict):
            problems.append(f"[{i}] not an object")
            continue
        missing = [f for f in _REQUIRED_FIELDS if not c.get(f)]
        if "source_url" in missing:
            problems.append(f"[{i}] missing source_url — claim rejected")
            continue
        if missing:
            problems.append(f"[{i}] missing fields: {missing}")
            continue
        if c["claim_type"] not in CLAIM_TYPES or \
           c["assertion_status"] not in ASSERTION_STATUSES or \
           c["access_status"] not in ACCESS_STATUSES or \
           c["source_authority"] not in AUTHORITIES:
            problems.append(f"[{i}] enum out of range")
            continue
        cid = verify.claim_id(c["claim_text"], c["source_url"])
        claims.append({
            "claim_id": cid,  # id is DERIVED here; the model's own id claim is ignored
            "claim_text": c["claim_text"],
            "source_url": c["source_url"],
            "access_status": c["access_status"],
            "source_authority": c["source_authority"],
            "claim_type": c["claim_type"],
            "assertion_status": c["assertion_status"],
            "supporting_quote": c.get("supporting_quote"),
            "supporting_locator": c.get("supporting_locator"),
        })
    if problems and not claims:
        path = _write_error_artifact("analyst-malformed", {
            "error": "all candidate claims invalid", "problems": problems}, root)
        raise MalformedAnalystOutput("all candidate claims invalid", path)
    if problems:
        _write_error_artifact("analyst-partial", {"problems": problems}, root)
    return claims


# --- The gate -----------------------------------------------------------------------

def _assertable(claim: dict, status: str) -> bool:
    """operator_verified is necessary for assertion; for a HOLDING it must also rest
    on a primary source — a verified secondary can only ever inform a lead."""
    if status != "operator_verified":
        return False
    if claim["claim_type"] == "holding" and claim["source_authority"] != "primary":
        return False
    return True


def classify(candidates: list[dict], ledger_path: str = verify.LEDGER_PATH) -> dict:
    """Sort candidates into asserted / leads / library sections by exact-id ledger
    lookup. Rejected claims are dropped from all sections (reported separately)."""
    claims_state = verify.replay(ledger_path)
    asserted, leads, library, rejected = [], [], [], []
    for c in candidates:
        status = verify.current_status(c["claim_id"], claims_state)
        if status == "operator_rejected":
            rejected.append(c)
        elif _assertable(c, status):
            asserted.append(c)
        elif c["access_status"] in ("paywalled", "blocked"):
            library.append(c)
        else:
            leads.append(c)
    header = (f"{len(asserted)} asserted (all operator-verified) · "
              f"{len(leads)} unverified leads · "
              f"{len(library)} routed for library access")
    return {"asserted": asserted, "leads": leads, "library": library,
            "rejected": rejected, "header": header}


def gate_brief(asserted: list[dict], ledger_path: str = verify.LEDGER_PATH) -> None:
    """FAIL the brief build (never the digest) if any finding presented as asserted
    lacks operator verification — naming the claim_id(s)."""
    claims_state = verify.replay(ledger_path)
    bad = [c["claim_id"] for c in asserted
           if not _assertable(c, verify.current_status(c["claim_id"], claims_state))]
    if bad:
        raise GateFailure(bad)
