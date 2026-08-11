"""Workstream G — the constrained lane, its guard, and the lane-naming fix.

The guard tests plant violations rather than describing them: an entry whose
text has been edited away from its slots, an entry with a conclusion in it, an
entry whose posture clause recombines the headline's words, and the label/access
mismatch the fixture simulation actually produced.
"""

import datetime
import importlib
import json
import os
import sys

import pytest

from src import headline_lane as hl
from src import rings
from src.rings import (PUBLIC_LABEL_HEADLINE_ONLY_LEAD,
                       PUBLIC_LABEL_LIBRARY_COMPARATOR, ClassifyState,
                       EvidenceLocation, EvidenceValidity, InvariantViolation,
                       Lane, Nexus, Strength)
from src.sources.base import CandidateItem

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
guard = importlib.import_module("check_headline_lane")

UTC = datetime.timezone.utc
FIXED = datetime.datetime(2026, 8, 1, 12, 0, tzinfo=UTC)

TITLE = "UK High Court declines State's request to amend set-aside claim"


def _entry(**kw):
    base = dict(source="iareporter_headlines", date="2026-08-01", title=TITLE,
                nexus="indeterminate", limitation=hl.LIMITATION_PAYWALLED,
                public_label=PUBLIC_LABEL_HEADLINE_ONLY_LEAD,
                lane_reason=rings.REASON_INCONCLUSIVE_LOCATION)
    base.update(kw)
    return hl.HeadlineLaneEntry(**base)


def _item(source, title, body="", summary="", enriched=False):
    return CandidateItem(source, f"http://x/{title[:12]}", f"http://x/{title[:12]}",
                         title, FIXED, summary, body,
                         {"enriched": True} if enriched else {})


# =============================================================================
# The grammar
# =============================================================================
def test_the_render_is_the_slots_and_nothing_else():
    e = _entry()
    assert e.text == "".join(t for _, t in e.segments())
    assert TITLE in e.text
    assert hl.LIMITATION_PAYWALLED in e.text
    assert "iareporter_headlines" in e.text
    assert "2026-08-01" in e.text


def test_the_limitation_clause_is_mandatory_and_from_a_closed_set():
    assert len(hl.LIMITATIONS) == 3
    with pytest.raises(InvariantViolation, match="limitation clause is fixed"):
        _entry(limitation="The body was not read, probably.")
    for lim in hl.LIMITATIONS:
        assert lim.endswith(".")
        assert "no thematic assessment" in lim or "no finding about the" in lim


def test_there_is_no_slot_for_a_conclusion():
    """The structural claim, checked structurally rather than asserted."""
    slot_names = set(hl.SLOT_NAMES)
    assert slot_names == {"source", "date", "title", "posture_subject",
                          "posture_verb", "nexus", "limitation"}
    # Every slot is either an enum, a pattern-checked identifier, or words
    # lifted verbatim from the title. None of them is free prose.
    assert "summary" not in slot_names and "assessment" not in slot_names
    assert "note" not in slot_names and "comment" not in slot_names


def test_a_posture_clause_must_be_a_consecutive_verbatim_run_of_the_title():
    ok = _entry(posture_subject="UK High Court", posture_verb="declines State's request")
    assert "Posture: UK High Court declines State's request." in ok.text

    # Both parts are in the title; the ORDER is not. Recombination is refused.
    with pytest.raises(InvariantViolation, match="consecutive verbatim run"):
        _entry(posture_subject="State's request", posture_verb="UK High Court")
    # A word that is not in the title at all.
    with pytest.raises(InvariantViolation, match="consecutive verbatim run"):
        _entry(posture_subject="UK High Court", posture_verb="dismissed the claim")
    # Half a clause is not a clause.
    with pytest.raises(InvariantViolation, match="needs both"):
        _entry(posture_subject="UK High Court")


def test_the_source_and_date_slots_are_pattern_checked():
    with pytest.raises(InvariantViolation, match="not a source identifier"):
        _entry(source="IA Reporter (paywalled), read at headline level")
    with pytest.raises(InvariantViolation, match="not YYYY-MM-DD"):
        _entry(date="1 August 2026")


def test_the_nexus_slot_is_an_enum_and_absent_is_never_stated():
    for word in hl.NEXUS_WORDS:
        assert _entry(nexus=word).text.count(f"ISDS nexus: {word}.") == 1
    with pytest.raises(InvariantViolation, match="is not one of"):
        _entry(nexus="absent")
    # A deterministic ABSENT nexus renders as indeterminate: "there is no
    # investor-State nexus here" is a conclusion, and this lane makes none.
    assert hl.nexus_word(Nexus.ABSENT) == "indeterminate"
    assert hl.nexus_word(Nexus.ESTABLISHED) == "established"


def test_rendering_is_deterministic_and_byte_stable():
    a, b = _entry(), _entry()
    assert a.text == b.text
    assert a.text.encode("utf-8") == b.text.encode("utf-8")


# =============================================================================
# The lane-naming fix
# =============================================================================
def test_an_accessible_body_library_item_is_not_called_headline_only():
    """The fixture-simulation mismatch, as a test.

    The simulation produced lane HEADLINE_ONLY_LIBRARY_LEAD at evidence location
    accessible_body — a fully-read domestic comparator publicly described as
    "headline-only". The internal lane value is unchanged; the public label is
    a function of where the evidence lives.
    """
    assert rings.public_lane_label(
        Lane.HEADLINE_ONLY_LIBRARY_LEAD, EvidenceLocation.ACCESSIBLE_BODY) \
        == PUBLIC_LABEL_LIBRARY_COMPARATOR
    assert rings.public_lane_label(
        Lane.HEADLINE_ONLY_LIBRARY_LEAD, EvidenceLocation.SUMMARY) \
        == PUBLIC_LABEL_LIBRARY_COMPARATOR
    assert rings.public_lane_label(
        Lane.HEADLINE_ONLY_LIBRARY_LEAD, EvidenceLocation.TITLE) \
        == PUBLIC_LABEL_HEADLINE_ONLY_LEAD
    assert rings.public_lane_label(
        Lane.HEADLINE_ONLY_LIBRARY_LEAD, EvidenceLocation.UNAVAILABLE_BODY) \
        == PUBLIC_LABEL_HEADLINE_ONLY_LEAD


def test_the_internal_lane_value_and_reason_are_preserved_exactly():
    """Compatibility: the public label is added, nothing is renamed."""
    assert Lane.HEADLINE_ONLY_LIBRARY_LEAD.value == "HEADLINE_ONLY_LIBRARY_LEAD"
    # The case in point: a domestic comparator whose body we DID retrieve. One
    # non-IP ring present, so it lands in the library lane at accessible_body.
    v = rings.RingVerdict(
        findings=(rings.lexical_finding(rings.RING_IP, 0),
                  rings.lexical_finding(rings.RING_JRM, rings.PRESENT_FLOOR),
                  rings.lexical_finding(rings.RING_JA, 0)),
        isds_nexus=Nexus.ESTABLISHED,
        evidence_location=EvidenceLocation.ACCESSIBLE_BODY,
        evidence_validity=EvidenceValidity.VERIFIED,
        classification_state=ClassifyState.OK_FIRST_PASS,
        path=rings.DerivationPath.DETERMINISTIC)
    assert v.lane is Lane.HEADLINE_ONLY_LIBRARY_LEAD
    assert v.evidence_location is EvidenceLocation.ACCESSIBLE_BODY
    assert v.lane_reason == rings.REASON_SINGLE_NO_IP_RING
    assert v.public_label == PUBLIC_LABEL_LIBRARY_COMPARATOR
    assert v.to_telemetry()["lane"] == "HEADLINE_ONLY_LIBRARY_LEAD"
    assert v.to_telemetry()["lane_reason"] == rings.REASON_SINGLE_NO_IP_RING
    assert v.to_telemetry()["public_label"] == PUBLIC_LABEL_LIBRARY_COMPARATOR


def test_the_public_label_is_total_over_every_lane_and_location():
    for lane in Lane:
        for location in EvidenceLocation:
            label = rings.public_lane_label(lane, location)
            assert label in rings.ALL_PUBLIC_LABELS
            if lane is not Lane.HEADLINE_ONLY_LIBRARY_LEAD:
                assert label not in (PUBLIC_LABEL_HEADLINE_ONLY_LEAD,
                                     PUBLIC_LABEL_LIBRARY_COMPARATOR)


def test_a_read_body_gets_the_retrieved_limitation_not_the_paywalled_one():
    """Saying "paywalled and was not retrieved" about a body we read would be
    this project's characteristic failure committed inside its own remedy."""
    assert hl.limitation_for(EvidenceLocation.ACCESSIBLE_BODY) \
        == hl.LIMITATION_RETRIEVED
    assert hl.limitation_for(EvidenceLocation.SUMMARY) == hl.LIMITATION_RETRIEVED
    assert hl.limitation_for(EvidenceLocation.TITLE) == hl.LIMITATION_PAYWALLED
    assert hl.limitation_for(EvidenceLocation.UNAVAILABLE_BODY) \
        == hl.LIMITATION_UNRETRIEVED


def test_rendering_from_a_verdict_refuses_every_lane_but_the_library_one():
    item = _item("iareporter_headlines", TITLE)
    match_verdict = rings.RingVerdict(
        findings=(rings.lexical_finding(rings.RING_IP, 20),
                  rings.lexical_finding(rings.RING_JRM, 20),
                  rings.lexical_finding(rings.RING_JA, 0)),
        isds_nexus=Nexus.ESTABLISHED,
        evidence_location=EvidenceLocation.ACCESSIBLE_BODY,
        evidence_validity=EvidenceValidity.VERIFIED,
        classification_state=ClassifyState.OK_FIRST_PASS,
        path=rings.DerivationPath.DETERMINISTIC)
    assert match_verdict.lane is Lane.MATCH
    with pytest.raises(InvariantViolation, match="renders"):
        hl.render_from_verdict(match_verdict, item, date="2026-08-01")


def test_a_headline_only_verdict_renders_end_to_end():
    item = _item("iareporter_headlines", TITLE)
    v = rings.shadow_verdict(
        item, lexical_result={"per_ring_subtotal": {}},
        classified=type("S", (), {"matched_rings": [], "relevance_score": None,
                                  "metadata": {}})(),
        classification_outcome="ok", attempts=1, headline_only=True)
    assert v.lane is Lane.HEADLINE_ONLY_LIBRARY_LEAD
    entry = hl.render_from_verdict(
        v, item, date="2026-08-01",
        posture_subject="UK High Court", posture_verb="declines State's request")
    assert entry.public_label == PUBLIC_LABEL_HEADLINE_ONLY_LEAD
    assert entry.limitation == hl.LIMITATION_PAYWALLED
    assert entry.lane_reason == v.lane_reason
    assert guard.check_entry(entry.to_record(), "fresh") == []


# =============================================================================
# The guard
# =============================================================================
def _write(tmp_path, entries):
    path = tmp_path / "headline_lane.jsonl"
    path.write_text("\n".join(json.dumps(e) for e in entries) + "\n",
                    encoding="utf-8")
    return path


def _run(path):
    return guard.main(["check_headline_lane", "--path", str(path)])


def test_the_guard_passes_a_freshly_rendered_entry(tmp_path):
    assert _run(_write(tmp_path, [_entry().to_record()])) == 0


def test_the_guard_is_silent_when_nothing_has_been_written(tmp_path):
    assert _run(tmp_path / "nothing.jsonl") == 0


def test_the_guard_fails_on_text_that_is_not_what_its_slots_render(tmp_path):
    """The planted violation that matters most: a hand-edited record."""
    rec = _entry().to_record()
    rec["text"] = rec["text"].replace(
        hl.LIMITATION_PAYWALLED,
        hl.LIMITATION_PAYWALLED + " The matter appears routine.")
    assert _run(_write(tmp_path, [rec])) == 1
    problems = guard.check_entry(rec, "planted")
    assert any("not what its own slots render" in p for p in problems)


def test_the_guard_fails_on_a_deletion_as_well_as_an_insertion(tmp_path):
    rec = _entry().to_record()
    rec["text"] = rec["text"].replace(hl.LIMITATION_PAYWALLED, "")
    assert _run(_write(tmp_path, [rec])) == 1


def test_the_guard_fails_on_a_conclusion_smuggled_into_the_text(tmp_path):
    for smuggled in ("The tribunal held that the claim fails.",
                     "This does not engage the research question.",
                     "A straightforward enforcement matter.",
                     "No ISDS issue arises.",
                     "The reasoning is set out below.",
                     "The court concludes against the investor.",
                     "It found that the claim was inadmissible.",
                     "A routine set-aside.",
                     "Outside the thematic intersection."):
        rec = _entry().to_record()
        rec["text"] = rec["text"] + "\n" + smuggled
        problems = guard.check_entry(rec, "planted")
        assert problems, f"{smuggled!r} passed the guard"


def test_the_guard_permits_a_forbidden_word_inside_the_quoted_title(tmp_path):
    """A headline is the source's sentence, quoted and attributed."""
    rec = _entry(title="Tribunal held that shipyard investor lacked standing",
                 ).to_record()
    assert guard.check_entry(rec, "quoted") == []
    assert _run(_write(tmp_path, [rec])) == 0


def test_the_guard_refuses_the_same_word_lifted_into_the_posture_clause(tmp_path):
    """...and the posture clause is OUR sentence, so it is scanned as ours."""
    title = "Tribunal held that shipyard investor lacked standing"
    rec = _entry(title=title, posture_subject="Tribunal",
                 posture_verb="held that shipyard investor lacked standing"
                 ).to_record()
    problems = guard.check_entry(rec, "lifted")
    assert any("forbidden token" in p for p in problems)
    assert _run(_write(tmp_path, [rec])) == 1


def test_the_guard_fails_a_label_that_contradicts_the_access_it_states(tmp_path):
    """The lane-naming defect, as a build failure."""
    rec = _entry(limitation=hl.LIMITATION_RETRIEVED,
                 public_label=PUBLIC_LABEL_HEADLINE_ONLY_LEAD).to_record()
    problems = guard.check_entry(rec, "mismatch")
    assert any("contradicts the limitation clause" in p for p in problems)
    assert _run(_write(tmp_path, [rec])) == 1

    # And the other direction: a paywalled body called a library comparator.
    rec = _entry(limitation=hl.LIMITATION_PAYWALLED,
                 public_label=PUBLIC_LABEL_LIBRARY_COMPARATOR).to_record()
    assert _run(_write(tmp_path, [rec])) == 1


def test_the_guard_fails_a_recombined_posture_clause_read_back_from_disk(tmp_path):
    rec = _entry().to_record()
    rec["posture_subject"] = "State's request"
    rec["posture_verb"] = "UK High Court"
    assert _run(_write(tmp_path, [rec])) == 1


def test_the_guard_fails_an_entry_that_does_not_record_its_slots(tmp_path):
    rec = _entry().to_record()
    del rec["limitation"]
    assert _run(_write(tmp_path, [rec])) == 1


def test_the_guard_reads_a_json_list_as_well_as_jsonl(tmp_path):
    path = tmp_path / "lane.json"
    path.write_text(json.dumps([_entry().to_record()]), encoding="utf-8")
    assert _run(path) == 0
