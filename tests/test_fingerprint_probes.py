"""Standing regression harness for the lexical-fingerprint probe suite.

Companion to analytics/fingerprint-gap-report.md. It pins the CURRENT
fingerprint's known-good behaviours so a future edit cannot silently regress
them, and it records the four measured false negatives (E2, E4, E5, C2) as
``xfail`` so the operator-approved reweight, when it lands, flips them to xpass
instead of requiring a test rewrite.

Scoring is the repo's own deterministic path (``keyword_score`` against the
canonical ``fingerprint.yaml``); nothing here reimplements the scorer.

Bands (from fingerprint.yaml ``scoring``):  HIGH >= 70,  MEDIUM >= 40,  LOW < 40.
Digest threshold = 40.
"""
import datetime
import json
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src import classify  # noqa: E402
from src.classify import keyword_score, load_fingerprint  # noqa: E402
from src.sources.base import CandidateItem  # noqa: E402

PROBES_PATH = os.path.join(ROOT, "analytics", "fingerprint_probes.json")
NOW = datetime.datetime.now(datetime.timezone.utc)

# The probes whose CURRENT score contradicts their theme-implied expected_band.
# Measured 2026-07 (see analytics/fingerprint-gap-report.md sec.3). Marked xfail
# so the suite stays green until the operator applies the sec.5 reweight, at
# which point E2/E4/E5 flip to xpass. C2 is the loose-vocabulary residual the
# phrase fix does not reach (see report sec.5c) and is expected to keep failing
# until the ISDS-nexus gate / semantic path lands.
KNOWN_FALSE_NEGATIVES = {"E2_einarsson_admin_fet", "E4_einarsson_negative_space",
                         "E5_einarsson_lexical_brittle", "C2_china_marketing_loose"}
XFAIL_REASON = "pending operator-approved reweight"


def _band(score: int) -> str:
    if score >= 70:
        return "HIGH"
    if score >= 40:
        return "MEDIUM"
    return "LOW"


def _score(text: str) -> int:
    # Ensure the canonical fingerprint is loaded (guard against another test
    # having swapped classify._FINGERPRINT_CACHE).
    classify._FINGERPRINT_CACHE = None
    load_fingerprint()
    ci = CandidateItem("probe", "id", "u", "", NOW, "", text, {})
    return keyword_score(ci)["relevance_score"]


def _load_probes():
    with open(PROBES_PATH, encoding="utf-8") as fh:
        return json.load(fh)["probes"]


PROBES = _load_probes()
_IDS = [p["id"] for p in PROBES]


def _meets(expected: str, score: int) -> bool:
    if expected == "LOW":
        return score < 40
    if expected == "MEDIUM":
        return score >= 40
    if expected == "HIGH":
        return score >= 70
    raise ValueError(expected)


# --------------------------------------------------------------------------- #
# Suite integrity
# --------------------------------------------------------------------------- #
def test_probe_suite_shape():
    """The suite exists at the documented size and category spread."""
    assert 12 <= len(PROBES) <= 16
    cats = [p["category"] for p in PROBES]
    assert cats.count("einarsson") >= 4
    assert cats.count("china_regime") >= 2
    assert cats.count("near_miss_negative") >= 3
    assert cats.count("seed_control") >= 2
    for p in PROBES:
        assert p["expected_band"] in {"HIGH", "MEDIUM", "LOW"}
        assert 90 <= len(p["text"].split()) <= 260, (p["id"], len(p["text"].split()))


def test_ring_weight_sums_are_100():
    """Invariant the whole scoring calibration rests on: each ring sums to 100."""
    classify._FINGERPRINT_CACHE = None
    fp = load_fingerprint()
    for ring, rd in fp["rings"].items():
        total = sum(int(k.get("weight", 0)) for k in rd.get("keywords", []))
        assert total == 100, f"{ring} sums to {total}, not 100"


# --------------------------------------------------------------------------- #
# Known-good behaviours of the CURRENT fingerprint (must never regress)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("probe", [p for p in PROBES if p["category"] == "seed_control"],
                         ids=[p["id"] for p in PROBES if p["category"] == "seed_control"])
def test_seed_controls_stay_high(probe):
    """The three-seed calibration must keep scoring the seed shapes HIGH."""
    score = _score(probe["text"])
    assert score >= 70, f"{probe['id']} fell to {score} ({_band(score)}); seed regressed"


@pytest.mark.parametrize("probe", [p for p in PROBES if p["category"] == "near_miss_negative"],
                         ids=[p["id"] for p in PROBES if p["category"] == "near_miss_negative"])
def test_negatives_stay_low(probe):
    """Near-miss negatives must stay below the digest threshold (no false positives)."""
    score = _score(probe["text"])
    assert score < 40, f"{probe['id']} rose to {score} ({_band(score)}); false positive"


# --------------------------------------------------------------------------- #
# Full-suite band expectations. Currently-failing on-theme probes are xfail.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("probe", PROBES, ids=_IDS)
def test_probe_meets_expected_band(probe, request):
    if probe["id"] in KNOWN_FALSE_NEGATIVES:
        request.applymarker(pytest.mark.xfail(reason=XFAIL_REASON, strict=False))
    score = _score(probe["text"])
    assert _meets(probe["expected_band"], score), (
        f"{probe['id']}: score {score} ({_band(score)}) "
        f"does not meet expected band {probe['expected_band']}"
    )
