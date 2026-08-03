"""THE single model-configuration location (Bounded Change Protocol v3).

Every role reads its model id from here; no other file may hardcode one. The one
deliberate exception, recorded in HANDOFF.md: the digest classifier keeps its
existing default inside src/classify.py because that file is outside the protocol's
allowed-change manifest and the operator's assignment for it is "unchanged".

Operator-confirmed assignments:
    orchestrator/chairman      -> claude-opus-5
    heavy-reasoning sub-agents -> claude-opus-5   (research analyst — operator directive
                                                    2026-07-29: the researcher needs the most
                                                    advanced capabilities available)
    utility sub-agents         -> claude-opus-4-8  (integrity helper, editor, graph classifier)
    digest classifier          -> unchanged (claude-haiku-4-5-20251001, in src/classify.py)

Runtime-fallback rule: if a requested id is unavailable in the runtime, do NOT
silently substitute — run on FALLBACK_MODEL and record REQUESTED vs ACTUAL per role
in HANDOFF.md via record_fallback(). The discrepancy must be visible, never hidden.
"""

from __future__ import annotations

import datetime
import os

CHAIRMAN_MODEL = "claude-opus-5"
HEAVY_MODEL = "claude-opus-5"
UTILITY_MODEL = "claude-opus-4-8"

# Digest classifier: operator assignment is "unchanged". The id lives HERE and is
# read by src/classify.py, so no model id is defined in more than one place.
DIGEST_CLASSIFIER_MODEL = "claude-haiku-4-5-20251001"

# Where an unavailable requested model lands (the strongest generally-available id).
FALLBACK_MODEL = "claude-opus-4-8"

_HANDOFF = "HANDOFF.md"
_MARKER = "## Model runtime fallbacks"


def record_fallback(role: str, requested: str, actual: str,
                    handoff_path: str = _HANDOFF) -> None:
    """Append a visible requested-vs-actual record to HANDOFF.md (idempotent per
    role+pair per day). Never raises — recording must not break the pipeline."""
    try:
        ts = datetime.date.today().isoformat()
        line = (f"- {ts} · role `{role}`: REQUESTED `{requested}` -> "
                f"ACTUAL runtime `{actual}`\n")
        existing = ""
        if os.path.exists(handoff_path):
            with open(handoff_path, encoding="utf-8") as fh:
                existing = fh.read()
        if line in existing:
            return
        with open(handoff_path, "a", encoding="utf-8") as fh:
            if _MARKER not in existing:
                fh.write(f"\n{_MARKER}\n\nThe pipeline ran, but a requested model id "
                         "was unavailable in the runtime; the discrepancy is recorded "
                         "here rather than hidden.\n\n")
            fh.write(line)
    except OSError:
        pass
