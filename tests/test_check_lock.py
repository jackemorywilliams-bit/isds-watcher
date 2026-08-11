"""scripts/check_lock.py — the locked validation set is what it was when locked.

The important test here is the planted tamper: `items.json` edited after its
hash was written down. Git history is the project's evidence that labels
preceded scores, and that evidence is worth nothing if either file can be
adjusted afterwards.
"""

import hashlib
import importlib
import json
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
check_lock = importlib.import_module("check_lock")


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


ITEMS = json.dumps([{"id": "cat1-01", "category": 1, "tier": "P",
                     "source_url": "https://icsid.example/1",
                     "document_title": "Award", "document_date": "2026-01-01",
                     "pinpoint": "para 143", "text": "x" * 40,
                     "access_status": "full"}], indent=2)
LABELS = json.dumps([{"id": "cat1-01", "L_theme": 1,
                      "L_theme_reason": "IP and judicial rings present.",
                      "L_band": "HIGH", "L_band_clause": "two rings -> HIGH"}],
                    indent=2)


def _lock_md(items_sha, labels_sha=None):
    rows = ["# Lock", "",
            "| File | SHA-256 | Commit |",
            "|---|---|---|",
            f"| `items.json` | `{items_sha}` | `abc1234` |"]
    if labels_sha:
        rows.append(f"| `labels.json` | `{labels_sha}` | `def5678` |")
    return "\n".join(rows) + "\n"


def _locked_set(tmp_path, *, items=ITEMS, labels=LABELS, lock=None):
    d = tmp_path / "locked_set"
    d.mkdir()
    if items is not None:
        (d / "items.json").write_text(items, encoding="utf-8")
    if labels is not None:
        (d / "labels.json").write_text(labels, encoding="utf-8")
    if lock is None:
        lock = _lock_md(_sha(items or ""), _sha(labels or ""))
    if lock is not False:
        (d / "LOCK.md").write_text(lock, encoding="utf-8")
    return d


def _run(directory):
    return check_lock.main(["check_lock", "--dir", str(directory)])


# =============================================================================
# The designed empty state
# =============================================================================
def test_the_real_repository_locked_set_is_empty_and_that_is_not_an_error():
    """The current state of the project: no items, deliberately."""
    assert _run(os.path.join(REPO, "analytics", "locked_set")) == 0


def test_an_empty_directory_with_no_lock_file_passes_with_a_note(tmp_path):
    d = tmp_path / "locked_set"
    d.mkdir()
    notes, problems = check_lock.check(d)
    assert problems == []
    assert any("deliberately empty" in n for n in notes)
    assert _run(d) == 0


def test_a_directory_that_does_not_exist_at_all_passes(tmp_path):
    assert _run(tmp_path / "not_created") == 0


# =============================================================================
# The lock, working
# =============================================================================
def test_an_untampered_locked_set_passes(tmp_path):
    assert _run(_locked_set(tmp_path)) == 0


def test_the_key_value_lock_format_is_read_as_well_as_the_table(tmp_path):
    lock = (f"- `items.json`: `{_sha(ITEMS)}` (commit `abc1234`)\n"
            f"- `labels.json`: `{_sha(LABELS)}` (commit `def5678`)\n")
    assert _run(_locked_set(tmp_path, lock=lock)) == 0


def test_items_locked_before_labels_exist_is_the_expected_intermediate_state(
        tmp_path):
    """Step 2 of the schema's commit order: items locked, labels not yet written."""
    d = _locked_set(tmp_path, labels=None, lock=_lock_md(_sha(ITEMS)))
    notes, problems = check_lock.check(d)
    assert problems == []
    assert any("labels.json: not present and not locked" in n for n in notes)


# =============================================================================
# The planted tamper
# =============================================================================
def test_a_tampered_items_file_fails_closed(tmp_path):
    d = _locked_set(tmp_path)
    assert _run(d) == 0
    tampered = json.loads(ITEMS)
    tampered[0]["text"] = "an edit made after the set was locked" + "y" * 20
    (d / "items.json").write_text(json.dumps(tampered, indent=2), encoding="utf-8")
    assert _run(d) == 1
    _, problems = check_lock.check(d)
    assert any("items.json CHANGED after it was locked" in p for p in problems)


def test_a_tampered_labels_file_fails_closed(tmp_path):
    d = _locked_set(tmp_path)
    relabelled = json.loads(LABELS)
    relabelled[0]["L_band"] = "LOW"
    (d / "labels.json").write_text(json.dumps(relabelled, indent=2),
                                   encoding="utf-8")
    assert _run(d) == 1


def test_a_whitespace_only_reformat_still_fails(tmp_path):
    """The lock is over BYTES. Two files that parse the same are still two
    different commits, and a reformat that passed would let a real edit hide
    inside one."""
    d = _locked_set(tmp_path)
    (d / "items.json").write_text(json.dumps(json.loads(ITEMS)), encoding="utf-8")
    assert _run(d) == 1


def test_a_deleted_locked_file_fails(tmp_path):
    d = _locked_set(tmp_path)
    (d / "labels.json").unlink()
    assert _run(d) == 1
    _, problems = check_lock.check(d)
    assert any("the file is gone" in p for p in problems)


def test_an_unlocked_file_in_a_locked_set_fails(tmp_path):
    """A file added to the set without being locked."""
    d = _locked_set(tmp_path, lock=_lock_md(_sha(ITEMS)))
    # labels.json exists but the lock names only items.json.
    assert _run(d) == 1
    _, problems = check_lock.check(d)
    assert any("added to the set without being locked" in p for p in problems)


def test_items_present_with_no_lock_file_at_all_fails(tmp_path):
    d = _locked_set(tmp_path, lock=False)
    assert _run(d) == 1
    _, problems = check_lock.check(d)
    assert any("unlocked validation set" in p for p in problems)


def test_a_lock_file_that_locks_nothing_fails(tmp_path):
    d = _locked_set(tmp_path, lock="# Lock\n\nTo be completed.\n")
    assert _run(d) == 1
    _, problems = check_lock.check(d)
    assert any("locks nothing" in p for p in problems)


def test_a_rewritten_lock_entry_is_caught_rather_than_taken_at_face_value(tmp_path):
    """Step 4 APPENDS labels.json's entry; it never rewrites an earlier one.

    Two different hashes for the same file means the lock record itself was
    edited — which is the one way a tamper could otherwise pass, by moving the
    hash to match the new contents.
    """
    old = _sha("a previous version of the items file")
    lock = (_lock_md(old, _sha(LABELS)).rstrip("\n") + "\n"
            + f"| `items.json` | `{_sha(ITEMS)}` | `9999999` |\n")
    d = _locked_set(tmp_path, lock=lock)
    assert _run(d) == 1
    _, problems = check_lock.check(d)
    assert any("two different hashes" in p for p in problems)


def test_the_guard_does_not_populate_or_modify_the_set(tmp_path):
    d = _locked_set(tmp_path)
    before = {p.name: p.read_bytes() for p in sorted(d.iterdir())}
    _run(d)
    after = {p.name: p.read_bytes() for p in sorted(d.iterdir())}
    assert before == after
