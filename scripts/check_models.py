#!/usr/bin/env python3
"""Cross-check what every council seat is said to run on.

WHY THIS EXISTS. Three artifacts each assert a seat's model and nothing compared
them:

  * `.claude/agents/<seat>.md` frontmatter — the only one with a MECHANISM. What it
    says is what actually gets invoked; the rest are descriptions of it.
  * `views/isds-workflow-3d/workflow.json` — the flowchart card's `meta` line, which
    is what a reader sees.
  * `agents/<seat>.md` in the vault — the seat's note.

On 2026-07-29 the operator moved seats off Fable; `939deaa` updated the registry's
roster table and not the card mirror, so five cards read "Claude Fable 5" for days
against definitions that said otherwise. Separately, `systems-designer` and
`site-experience` carried cards asserting "Claude Opus 5" while their definitions
declared no `model:` key at all — the card was accidentally true, because the
invoking session happened to be Opus 5, and would have gone silently false the moment
it was not. Both were caught by a person reading carefully. This makes them fail
instead.

WHAT IT CHECKS.

  1. A card that names a model must belong to a seat whose definition declares a
     `model:` key. An assertion with no mechanism behind it is the defect above.
  2. Every model named on a card must normalise to a model id that actually appears
     in `src/models.py`. This is what catches "Claude Fable 5": it normalises to
     `claude-fable-5`, which the code does not contain.
  3. A seat's vault note, where it states a model, must name the same one as its
     card. Two records of one fact that disagree mean at least one is wrong.

WHAT IT CANNOT DO. It cannot tell you a seat is running on the model it *should* —
only that the project's three statements agree and that the named model is one the
code knows. Choosing the model is the operator's; this checks the bookkeeping.

A NOTE ON `model: opus`. The frontmatter selects a TIER, not a version. The concrete
version lives in `src/models.py` and on the card. That is the project's existing
convention, not something this script invents, and it means a card naming a version
is describing a choice the frontmatter does not itself pin.

CLI:
    python scripts/check_models.py

Exit 0 clean, 1 on any disagreement, 2 if an input cannot be read.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFS_DIR = REPO / ".claude" / "agents"
VAULT_DIR = REPO / "agents"
MODELS_PY = REPO / "src" / "models.py"
FLOWCHART = REPO / "views" / "isds-workflow-3d" / "workflow.json"

# "Model: Claude Opus 4.8" on a card -> "claude-opus-4-8" in the code.
_CARD_MODEL_RE = re.compile(r"Model:\s*(.+?)\s*$", re.IGNORECASE)
_FRONTMATTER_MODEL_RE = re.compile(r"^model:\s*(\S+)\s*$", re.MULTILINE)
_VAULT_MODEL_RE = re.compile(r"^\*\*Model\.\*\*\s+`([^`]+)`", re.MULTILINE)
_MODEL_ID_RE = re.compile(r"[\"']((?:claude|gpt|gemini)-[a-z0-9.\-]+)[\"']", re.IGNORECASE)
# The only thing a card is allowed to omit from a code id: a dated build stamp.
_DATE_SUFFIX_RE = re.compile(r"^-\d{8}$")

# Cards name a seat by flowchart node id, which is not always the definition's name.
NODE_TO_SEAT = {
    "chairman": "council-chairman",
    "analyst": "research-analyst",
    "editor": "research-editor",
    "minutes": "council-chairman",       # the chairman writes the minutes
    "daily-researcher": "research-analyst",
}


def normalise(name: str) -> str:
    """"Claude Opus 4.8" -> "claude-opus-4-8". Dots and spaces both become hyphens
    because the code writes versions with hyphens and prose writes them with dots."""
    return re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")


def names_a_known_model(norm: str, known: set[str]) -> bool:
    """Whether ``norm`` identifies one of ``known``.

    A card may name the family where the code pins a DATED BUILD: the classifier card
    reads "Claude Haiku 4.5" against ``claude-haiku-4-5-20251001``, and that is a
    truthful description, not drift. So a prefix counts only when what it omits is a
    date. Any hyphen boundary would be too loose — "claude-opus-4" is a hyphen-
    boundary prefix of "claude-opus-4-8", and a card naming the wrong minor version
    must fail, not pass. "claude-fable-5" still matches nothing at all."""
    return any(k == norm or _DATE_SUFFIX_RE.match(k[len(norm):])
               for k in known if k.startswith(norm))


def known_model_ids() -> set[str]:
    """Every model id literal in ``src/models.py`` — the set a card may name."""
    text = MODELS_PY.read_text(encoding="utf-8")
    return {m.group(1).lower() for m in _MODEL_ID_RE.finditer(text)}


def card_models() -> dict[str, str]:
    """``{node_id: model as written on the card}`` for cards that name one."""
    data = json.loads(FLOWCHART.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for node in data.get("nodes", []):
        for value in node.values():
            if isinstance(value, str):
                m = _CARD_MODEL_RE.match(value.strip())
                if m:
                    out[node["id"]] = m.group(1)
                    break
    return out


def declared_model(seat: str) -> str | None:
    """The `model:` key in a seat's definition frontmatter, or None."""
    path = DEFS_DIR / f"{seat}.md"
    if not path.exists():
        return None
    m = _FRONTMATTER_MODEL_RE.search(path.read_text(encoding="utf-8"))
    return m.group(1) if m else None


def vault_model(seat: str) -> str | None:
    """The model a seat's vault note states, or None if it states none."""
    path = VAULT_DIR / f"{seat}.md"
    if not path.exists():
        return None
    m = _VAULT_MODEL_RE.search(path.read_text(encoding="utf-8"))
    return m.group(1) if m else None


def check() -> list[str]:
    """Every disagreement, as a list of human-readable problems."""
    problems: list[str] = []
    known = known_model_ids()
    if not known:
        return [f"{MODELS_PY.relative_to(REPO)}: no model ids found — cannot check "
                "cards against the code"]

    for node, card in sorted(card_models().items()):
        seat = NODE_TO_SEAT.get(node, node)
        norm = normalise(card)

        # 2. The named model must be one the code knows.
        if not names_a_known_model(norm, known):
            problems.append(
                f"views/isds-workflow-3d/workflow.json [{node}] names \"{card}\", "
                f"which normalises to \"{norm}\" and appears nowhere in "
                f"src/models.py — no model by that name is configured")

        # 1. A card asserting a model needs a definition that declares one.
        if not (DEFS_DIR / f"{seat}.md").exists():
            continue  # a card for something that is not a subagent seat
        if declared_model(seat) is None:
            problems.append(
                f".claude/agents/{seat}.md declares no `model:` key, but its card "
                f"[{node}] asserts \"{card}\" — the assertion has no mechanism "
                "behind it and is true only while the invoking session happens to "
                "match")

        # 3. The vault note must not contradict the card.
        vault = vault_model(seat)
        if vault and normalise(vault) != norm:
            problems.append(
                f"agents/{seat}.md states `{vault}` but its card [{node}] says "
                f"\"{card}\" — two records of one fact, disagreeing")

    return problems


def main(argv: list[str]) -> int:
    try:
        problems = check()
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot run the model check: {exc}", file=sys.stderr)
        return 2

    cards = card_models()
    print(f"Checked {len(cards)} flowchart cards against "
          f".claude/agents/, agents/ and src/models.py.")
    for p in problems:
        print(f"  FAIL {p}")
    if problems:
        print("\nA seat's model is asserted in three places. They must agree, and the "
              "definition's\n`model:` key is the only one of the three that does "
              "anything.", file=sys.stderr)
        return 1
    print("  ok — every card names a configured model, backed by a declared "
          "`model:` key, and no\n       vault note contradicts its card.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
