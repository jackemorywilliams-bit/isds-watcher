#!/usr/bin/env python3
"""Append-only verification ledger + operator CLI (Bounded Change Protocol, Part 1).

The ledger (analytics/verification_ledger.jsonl) is an EVENT LOG, never mutated in
place. Events are appended; current state is derived by replaying the stream. Only the
operator — through this CLI — may append ``verification_changed`` events; automated
code may append only ``claim_created`` and machine-metadata events (reachability,
snapshot observations, audit notes). A reachable URL is never evidence a claim is true.

Events
------
claim_created        — a candidate claim enters the record (automated OK).
machine_metadata     — reachability / snapshot_observed / audit facts (automated OK).
verification_changed — operator-only status transition, appended via ``verify mark``.

claim_id = SHA256(canonical_claim_text + "\\n" + canonical_source_locator). Exact-id
lookup only: no fuzzy, similarity, or URL-only match may satisfy verification.

CLI
---
    python scripts/verify.py list [--status unverified]
    python scripts/verify.py mark <claim_id> --verified|--rejected [--quote-ok]
                                  [--scope-ok] [--note "..."]
    python scripts/verify.py status
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

LEDGER_PATH = os.path.join("analytics", "verification_ledger.jsonl")

OPERATOR_STATUSES = {"operator_verified", "operator_rejected"}
DEFAULT_STATUS = "unverified"

# Query parameters that identify tracking, not content — dropped at canonicalization.
_TRACKING_PARAMS = re.compile(r"^(utm_|fbclid$|gclid$|mc_cid$|mc_eid$|ref$)")


# --- Canonicalization + identity ---------------------------------------------------

def canonical_claim_text(text: str) -> str:
    """Unicode NFC, whitespace collapsed to single spaces, trimmed. Case and
    punctuation preserved — a different sentence is a different claim."""
    text = unicodedata.normalize("NFC", text or "")
    return re.sub(r"\s+", " ", text).strip()


def canonical_source_locator(locator: str) -> str:
    """Lowercase scheme+host, fragment removed, trailing slash normalized, tracking
    params dropped (other query params preserved). Redirects are NOT followed —
    identity is the locator as cited, not wherever it forwards to today."""
    locator = (locator or "").strip()
    if "://" not in locator:
        return locator  # pdf / local_file / database_record locators pass through
    parts = urlsplit(locator)
    query = urlencode([(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
                       if not _TRACKING_PARAMS.match(k.lower())])
    path = parts.path or "/"
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, query, ""))


def claim_id(claim_text: str, source_locator: str) -> str:
    payload = canonical_claim_text(claim_text) + "\n" + canonical_source_locator(source_locator)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# --- Append-only event log ----------------------------------------------------------

_MACHINE_EVENTS = {"claim_created", "machine_metadata"}


def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def append_event(event: dict, path: str = LEDGER_PATH, *, _operator_cli: bool = False) -> None:
    """Append one event line. ENFORCED: ``verification_changed`` may only be appended
    through the operator CLI path (``mark``); any automated caller raises. This is the
    state machine's in-code gate — no automated path can mint a verification."""
    kind = event.get("event")
    if kind == "verification_changed" and not _operator_cli:
        raise PermissionError(
            "verification_changed events may only be appended by the operator CLI "
            "(scripts/verify.py mark); automated code may not change verification status")
    if kind not in _MACHINE_EVENTS and kind != "verification_changed":
        raise ValueError(f"unknown event type: {kind!r}")
    event.setdefault("ts", _now())
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, sort_keys=True, ensure_ascii=False) + "\n")


def create_claim(claim_text: str, source_locator: str, *,
                 source_locator_type: str = "url", source_snapshot: str | None = None,
                 supporting_locator: str | None = None, access_status: str = "full",
                 source_authority: str = "unknown", path: str = LEDGER_PATH) -> str:
    """Record a candidate claim (automated path). Returns its claim_id. Idempotent in
    effect: re-creating an existing claim appends another claim_created event but the
    id — and any verification history — is unchanged."""
    cid = claim_id(claim_text, source_locator)
    append_event({
        "event": "claim_created", "claim_id": cid,
        "claim_text": canonical_claim_text(claim_text),
        "source_locator": canonical_source_locator(source_locator),
        "source_locator_type": source_locator_type,
        "source_snapshot": source_snapshot,
        "supporting_locator": supporting_locator,
        "access_status": access_status,
        "source_authority": source_authority,
    }, path)
    return cid


def record_metadata(cid: str, kind: str, detail: dict, path: str = LEDGER_PATH) -> None:
    """Machine facts about a claim (reachability probe, snapshot_observed, audit note).
    Never affects verification status."""
    append_event({"event": "machine_metadata", "claim_id": cid,
                  "kind": kind, **detail}, path)


# --- Replay: derive state from the stream -------------------------------------------

def replay(path: str = LEDGER_PATH) -> dict[str, dict]:
    """Replay the log into {claim_id: state}. State carries the full event history —
    every transition is always recoverable. Malformed lines are collected under
    ``_malformed`` (never silently dropped), not fatal."""
    claims: dict[str, dict] = {}
    malformed: list[str] = []
    if not os.path.exists(path):
        return claims
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
                cid = ev["claim_id"]
                kind = ev["event"]
            except Exception:  # noqa: BLE001 - malformed is reported, not dropped
                malformed.append(line)
                continue
            st = claims.setdefault(cid, {
                "claim_id": cid, "claim": None, "status": DEFAULT_STATUS,
                "verified_snapshot": None, "latest_snapshot": None, "events": [],
            })
            st["events"].append(ev)
            if kind == "claim_created":
                if st["claim"] is None:
                    st["claim"] = ev
                st["latest_snapshot"] = ev.get("source_snapshot") or st["latest_snapshot"]
            elif kind == "machine_metadata":
                if ev.get("kind") == "snapshot_observed" and ev.get("sha256"):
                    st["latest_snapshot"] = ev["sha256"]
            elif kind == "verification_changed":
                new = ev.get("new_status")
                if new in OPERATOR_STATUSES or new == DEFAULT_STATUS:
                    st["status"] = new
                    st["verified_snapshot"] = ev.get("source_snapshot",
                                                     st["latest_snapshot"])
    if malformed:
        claims["_malformed"] = {"claim_id": "_malformed", "lines": malformed}  # type: ignore[assignment]
    return claims


def current_status(cid: str, claims: dict[str, dict]) -> str:
    """EXACT-id lookup only. An unknown id is unverified — no fuzzy fallback."""
    st = claims.get(cid)
    return st["status"] if st else DEFAULT_STATUS


def verified_against_current_snapshot(st: dict) -> bool:
    """Snapshot invalidation: a verification holds FOR THE SNAPSHOT it was made
    against. If a later observation of the same locator hashes differently, the claim
    is no longer verified against the current artifact (history stays intact)."""
    if st.get("status") != "operator_verified":
        return False
    vs, ls = st.get("verified_snapshot"), st.get("latest_snapshot")
    if vs and ls and vs != ls:
        return False
    return True


# --- Operator CLI -------------------------------------------------------------------

def _git_actor() -> str:
    try:
        out = subprocess.run(["git", "config", "user.name"],
                             capture_output=True, text=True, check=False)
        return out.stdout.strip() or "unknown-operator"
    except OSError:
        return "unknown-operator"


def mark(cid: str, new_status: str, *, note: str = "", quote_ok: bool = False,
         scope_ok: bool = False, path: str = LEDGER_PATH) -> dict:
    """Operator transition. Records prior status; reversible between the two operator
    states. This is the ONLY function that appends verification_changed."""
    if new_status not in OPERATOR_STATUSES:
        raise ValueError(f"operator may set {sorted(OPERATOR_STATUSES)}, not {new_status!r}")
    claims = replay(path)
    st = claims.get(cid)
    prior = st["status"] if st else DEFAULT_STATUS
    ev = {
        "event": "verification_changed", "claim_id": cid,
        "prior_status": prior, "new_status": new_status,
        "actor": _git_actor(), "command": " ".join(sys.argv),
        "note": note, "quote_ok": quote_ok, "scope_ok": scope_ok,
        "source_snapshot": (st or {}).get("latest_snapshot"),
    }
    append_event(ev, path, _operator_cli=True)
    return ev


def _cmd_list(args) -> int:
    claims = replay(args.ledger)
    groups: dict[tuple[str, str], list[dict]] = {}
    for cid, st in sorted(claims.items()):
        if cid == "_malformed" or st.get("claim") is None:
            continue
        if args.status and st["status"] != args.status:
            continue
        c = st["claim"]
        groups.setdefault((c.get("access_status", "?"), c.get("source_authority", "?")),
                          []).append(st)
    for (access, authority), rows in sorted(groups.items()):
        flag = ("  << forward to professor, do not self-verify"
                if access in ("paywalled", "blocked") else "")
        print(f"\n[{access} / {authority}]{flag}")
        for st in rows:
            c = st["claim"]
            print(f"  {st['claim_id'][:16]}  {st['status']:<18} {c['claim_text'][:90]}")
            print(f"                    {c['source_locator']}")
    if "_malformed" in claims:
        print(f"\nWARNING: {len(claims['_malformed']['lines'])} malformed ledger line(s).")
    return 0


def _cmd_mark(args) -> int:
    new = "operator_verified" if args.verified else "operator_rejected"
    ev = mark(args.claim_id, new, note=args.note or "",
              quote_ok=args.quote_ok, scope_ok=args.scope_ok, path=args.ledger)
    print(f"{args.claim_id[:16]}: {ev['prior_status']} -> {ev['new_status']} "
          f"(actor: {ev['actor']})")
    return 0


def _cmd_status(args) -> int:
    claims = replay(args.ledger)
    counts: dict[str, int] = {}
    total = 0
    for cid, st in claims.items():
        if cid == "_malformed" or st.get("claim") is None:
            continue
        total += 1
        counts[st["status"]] = counts.get(st["status"], 0) + 1
    print(f"claims: {total}")
    for s in sorted(counts):
        print(f"  {s}: {counts[s]}")
    verified = counts.get("operator_verified", 0)
    pct = (100.0 * verified / total) if total else 0.0
    print(f"operator_verified: {pct:.0f}% of ledgered claims")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Operator verification ledger CLI.")
    ap.add_argument("--ledger", default=LEDGER_PATH)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("list"); p.add_argument("--status"); p.set_defaults(fn=_cmd_list)
    p = sub.add_parser("mark")
    p.add_argument("claim_id")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--verified", action="store_true")
    g.add_argument("--rejected", action="store_true")
    p.add_argument("--quote-ok", action="store_true")
    p.add_argument("--scope-ok", action="store_true")
    p.add_argument("--note")
    p.set_defaults(fn=_cmd_mark)
    p = sub.add_parser("status"); p.set_defaults(fn=_cmd_status)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
