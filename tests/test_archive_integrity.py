"""Guardrail tests: the live archive must stay consistent, and the validator
must actually catch the failure modes we hit in development."""
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))

from validate_archive import validate_archive  # noqa: E402


def test_live_archive_is_clean():
    problems = validate_archive(os.path.join(REPO, "digests"))
    assert problems == [], "Archive integrity problems:\n  " + "\n  ".join(problems)


def test_validator_flags_subfloor_and_placeholder(tmp_path):
    folder = tmp_path / "2099-01-01_ISDS-Thematic-Watch"
    arts = folder / "articles"
    arts.mkdir(parents=True)
    # One legitimate watch-list lead, one sub-floor item, one placeholder title.
    (arts / "01_real.md").write_text(
        "# 1. Real Case v. State\n- **Relevance:** 30 (WATCH)\n", encoding="utf-8")
    (arts / "02_subfloor.md").write_text(
        "# 2. Noise Item\n- **Relevance:** 8 (LOW)\n", encoding="utf-8")
    (arts / "03_placeholder.md").write_text(
        "# 3. View case details\n- **Relevance:** 27 (WATCH)\n", encoding="utf-8")
    # meta claims wrong counts on purpose.
    (folder / "meta.json").write_text(json.dumps(
        {"date": "2099-01-01", "screened": 50, "matches": 1,
         "watch_list_leads": 9, "accepted": 3}), encoding="utf-8")

    problems = validate_archive(str(tmp_path))
    blob = "\n".join(problems)
    assert "< floor" in blob              # sub-floor item caught
    assert "placeholder title" in blob    # "View case details" caught
    assert "meta matches=" in blob        # bad matches count caught
    assert "watch_list_leads=" in blob    # bad leads count caught
