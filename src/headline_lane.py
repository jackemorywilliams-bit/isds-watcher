"""Workstream G — the constrained lane: a renderer with no slot for a conclusion.

WHY A GRAMMAR AND NOT A PROMPT. The archive's worst entries are not entries that
got a fact wrong. They are entries that said something *about* a document nobody
read. `analytics/instrument-map-2026-08-08.md` §7 records the Gazprom
annotation, which reached a negative thematic conclusion about a body the
pipeline never retrieved. The instinct is to fix that by instructing a model
more carefully. That has been tried, in this repo, several times, and the
failure mode of an instruction is that it holds until the day it does not and
nobody can tell which day that was.

So this renderer has no free-text slot at all. It emits a fixed template with
values substituted into named positions, and the positions are: the source
name, the date, the item's own verbatim title, an optional posture clause that
must be a verbatim run of words FROM that title, one enum word for the
deterministic ISDS nexus, and one fixed limitation sentence chosen from a closed
set of three. There is nowhere in that list to put "this is a routine
enforcement matter" or "no ISDS issue arises", because there is nowhere to put
a sentence at all. `scripts/check_headline_lane.py` re-derives every rendered
entry from its slots and requires byte identity, so a hand-edit or a stray
model-written line is a build failure and not a thing someone has to notice.

THE POSTURE CLAUSE, which is the only interesting slot. It exists because
"Source — date — headline" alone reads as a bare link dump, and a reader needs
the procedural shape of the item. It is safe only because both its parts must
appear IN THE TITLE, consecutively and in order: `_verbatim_run` requires
``subject + " " + verb_phrase`` to be a substring of the title, which blocks the
recombination attack a per-part check would allow — a title reading "State
challenges tribunal's finding" cannot be rendered as "tribunal challenges
State", because that word sequence is not in the title.

THE LIMITATION CLAUSE IS KEYED ON WHAT WE ACTUALLY HOLD, and this is a
deliberate, recorded deviation from the single fixed sentence R2.1 specifies.
That sentence says the body "is paywalled and was not retrieved". For a
headline-only source that is true. For a library comparator whose body we DID
retrieve it is false — and printing a false statement about our own access, in
the very sentence whose job is to be honest about our access, would be this
project's characteristic failure committed inside its own remedy. There are
therefore three fixed sentences, one per access state, chosen by code from the
evidence location; the set is closed and the guard enforces membership.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional

from .rings import (PUBLIC_LABEL_HEADLINE_ONLY_LEAD,
                    PUBLIC_LABEL_LIBRARY_COMPARATOR, EvidenceLocation,
                    InvariantViolation, Lane, Nexus, public_lane_label)

# Source names are module-derived identifiers of ours (`icsid`, `pca_press`,
# `iareporter_headlines`, ...). Anchored, so a source name is a name and never a
# sentence someone put in the source field.
_SOURCE_RE = re.compile(r"\A[a-z0-9_]+\Z")
_DATE_RE = re.compile(r"\A\d{4}-\d{2}-\d{2}\Z")

# The nexus values this lane may state. ABSENT is excluded on purpose: "there is
# no investor-State nexus here" is a thematic conclusion about the item, and
# this lane does not make those. An item whose deterministic nexus is ABSENT
# renders as "indeterminate" — see `nexus_word`.
NEXUS_WORDS = ("established", "asserted", "indeterminate")

# The three fixed limitation sentences. A closed set: the renderer picks by
# evidence location and the guard checks membership, so a fourth sentence cannot
# be introduced by editing a rendered file.
LIMITATION_PAYWALLED = (
    "The body is paywalled and was not retrieved; nothing above is a finding "
    "about its contents, and no thematic assessment has been made.")
LIMITATION_UNRETRIEVED = (
    "The body could not be retrieved; nothing above is a finding about its "
    "contents, and no thematic assessment has been made.")
LIMITATION_RETRIEVED = (
    "The body was retrieved and recorded; nothing above is a thematic "
    "assessment of it, and no finding about the research question has been "
    "made.")

LIMITATIONS = (LIMITATION_PAYWALLED, LIMITATION_UNRETRIEVED, LIMITATION_RETRIEVED)

_LIMITATION_FOR_LOCATION = {
    EvidenceLocation.TITLE: LIMITATION_PAYWALLED,
    EvidenceLocation.UNAVAILABLE_BODY: LIMITATION_UNRETRIEVED,
    EvidenceLocation.ACCESSIBLE_BODY: LIMITATION_RETRIEVED,
    EvidenceLocation.SUMMARY: LIMITATION_RETRIEVED,
}

# Words and phrases that would turn a record into an assertion. Checked by the
# guard against everything EXCEPT the quoted title — a headline may legitimately
# read "Tribunal held that...", and quoting it verbatim inside quotation marks
# attributes it to the source. Lifting the same words into the posture clause
# would be us saying it, so the posture clause is checked too.
FORBIDDEN_TOKENS = (
    "held", "found that", "concludes", "reasoning", "no isds",
    "does not engage", "straightforward", "routine", "intersection",
)

_FIXED_LEAD = " — "
_FIXED_NEWLINE = "\n"
_FIXED_QUOTE = "“"
_FIXED_UNQUOTE = "”"
_FIXED_POSTURE_LEAD = "Posture: "
_FIXED_STOP = "."
_FIXED_NEXUS_LEAD = "ISDS nexus: "

# Every literal the grammar may emit. The guard rejects a rendered entry whose
# fixed segments are not all drawn from this set, which is what makes "no
# character that is not from an allowed slot or a fixed string" checkable rather
# than aspirational.
FIXED_LITERALS = frozenset({
    _FIXED_LEAD, _FIXED_NEWLINE, _FIXED_QUOTE, _FIXED_UNQUOTE,
    _FIXED_POSTURE_LEAD, _FIXED_STOP, _FIXED_NEXUS_LEAD, " ", *LIMITATIONS,
})

SLOT_NAMES = ("source", "date", "title", "posture_subject", "posture_verb",
              "nexus", "limitation")


def nexus_word(nexus: Nexus) -> str:
    """The enum word this lane states for a deterministic nexus value.

    ABSENT maps to "indeterminate". That is not a fudge: `derive_nexus` returns
    ABSENT only from an accessible body, and this lane's entries assert nothing
    about contents, so reporting "absent" here would be the lane making the one
    kind of claim it exists not to make. The precise value is untouched in
    `verdict.isds_nexus` and in telemetry.
    """
    if not isinstance(nexus, Nexus):
        raise InvariantViolation(f"nexus must be a Nexus, got {nexus!r}")
    if nexus is Nexus.ABSENT:
        return Nexus.INDETERMINATE.value
    return nexus.value


def limitation_for(location: EvidenceLocation) -> str:
    if not isinstance(location, EvidenceLocation):
        raise InvariantViolation(
            f"location must be an EvidenceLocation, got {location!r}")
    return _LIMITATION_FOR_LOCATION[location]


def _normalize_ws(s: str) -> str:
    """Collapse runs of whitespace. Titles arrive from feeds with newlines and
    doubled spaces in them; a "verbatim substring" test that treated those as
    significant would reject genuine runs of words over invisible characters."""
    return re.sub(r"\s+", " ", s or "").strip()


def _verbatim_run(title: str, subject: str, verb_phrase: str) -> bool:
    """Whether ``subject verb_phrase`` is a consecutive run of words in ``title``."""
    if not subject or not verb_phrase:
        return False
    return _normalize_ws(f"{subject} {verb_phrase}") in _normalize_ws(title)


@dataclass(frozen=True)
class HeadlineLaneEntry:
    """One rendered constrained-lane record: its slots, and the text they make.

    Frozen, and ``text`` is derived in ``__post_init__`` rather than accepted:
    there is no constructor in which the text and the slots can disagree, which
    is the property the guard then re-checks on anything read back from disk.
    """

    source: str
    date: str
    title: str
    nexus: str
    limitation: str
    posture_subject: str = ""
    posture_verb: str = ""
    public_label: str = PUBLIC_LABEL_HEADLINE_ONLY_LEAD
    lane_reason: str = ""
    text: str = field(init=False)

    def __post_init__(self) -> None:
        if not _SOURCE_RE.match(self.source or ""):
            raise InvariantViolation(
                f"source {self.source!r} is not a source identifier")
        if not _DATE_RE.match(self.date or ""):
            raise InvariantViolation(f"date {self.date!r} is not YYYY-MM-DD")
        if not (self.title or "").strip():
            raise InvariantViolation("an entry with no title states nothing")
        if self.nexus not in NEXUS_WORDS:
            raise InvariantViolation(
                f"nexus {self.nexus!r} is not one of {NEXUS_WORDS}")
        if self.limitation not in LIMITATIONS:
            raise InvariantViolation(
                "the limitation clause is fixed and this is not one of the three")
        if self.public_label not in (PUBLIC_LABEL_HEADLINE_ONLY_LEAD,
                                     PUBLIC_LABEL_LIBRARY_COMPARATOR):
            raise InvariantViolation(
                f"public_label {self.public_label!r} is not a lane label")
        if bool(self.posture_subject) != bool(self.posture_verb):
            raise InvariantViolation(
                "a posture clause needs both a subject and a verb phrase")
        if self.posture_subject and not _verbatim_run(
                self.title, self.posture_subject, self.posture_verb):
            raise InvariantViolation(
                f"posture clause {self.posture_subject!r} + "
                f"{self.posture_verb!r} is not a consecutive verbatim run of the "
                "title; the clause may only re-say words the headline already "
                "says, in the order it says them")
        object.__setattr__(self, "text",
                           "".join(t for _, t in self.segments()))

    def slots(self) -> dict:
        return {name: getattr(self, name) for name in SLOT_NAMES}

    def segments(self) -> tuple[tuple[str, str], ...]:
        """The rendering, decomposed into ``(kind, text)`` pairs.

        ``kind`` is ``"fixed"`` or a slot name. This is the single definition of
        the grammar — the renderer joins it and the guard walks it — so there is
        no second copy of the template for the two to drift apart on.
        """
        segs: list[tuple[str, str]] = [
            ("source", self.source),
            ("fixed", _FIXED_LEAD),
            ("date", self.date),
            ("fixed", _FIXED_NEWLINE),
            ("fixed", _FIXED_QUOTE),
            ("title", _normalize_ws(self.title)),
            ("fixed", _FIXED_UNQUOTE),
            ("fixed", _FIXED_NEWLINE),
        ]
        if self.posture_subject:
            segs += [
                ("fixed", _FIXED_POSTURE_LEAD),
                ("posture_subject", self.posture_subject),
                ("fixed", " "),
                ("posture_verb", self.posture_verb),
                ("fixed", _FIXED_STOP),
                ("fixed", _FIXED_NEWLINE),
            ]
        segs += [
            ("fixed", _FIXED_NEXUS_LEAD),
            ("nexus", self.nexus),
            ("fixed", _FIXED_STOP),
            ("fixed", _FIXED_NEWLINE),
            ("limitation", self.limitation),
        ]
        return tuple(segs)

    def to_record(self) -> dict:
        """The serialisable form the guard reads: slots, label, and the text."""
        rec = self.slots()
        rec["public_label"] = self.public_label
        rec["lane_reason"] = self.lane_reason
        rec["text"] = self.text
        return rec


def from_record(rec: dict) -> HeadlineLaneEntry:
    """Rebuild an entry from its slots. Raises InvariantViolation on bad slots."""
    return HeadlineLaneEntry(
        source=str(rec.get("source", "")),
        date=str(rec.get("date", "")),
        title=str(rec.get("title", "")),
        nexus=str(rec.get("nexus", "")),
        limitation=str(rec.get("limitation", "")),
        posture_subject=str(rec.get("posture_subject", "")),
        posture_verb=str(rec.get("posture_verb", "")),
        public_label=str(rec.get("public_label", PUBLIC_LABEL_HEADLINE_ONLY_LEAD)),
        lane_reason=str(rec.get("lane_reason", "")),
    )


def render_from_verdict(verdict, item, *, date: str,
                        posture_subject: str = "",
                        posture_verb: str = "") -> HeadlineLaneEntry:
    """Render the constrained entry for a library-lane verdict.

    Refuses any lane but the library lane. The other four lanes mean something
    was concluded — a match, an adjacent lead, an earned rejection, an unfinished
    classification — and this grammar has no way to say any of them; rendering
    one here would silently present a conclusion as a bare record.
    """
    if verdict.lane is not Lane.HEADLINE_ONLY_LIBRARY_LEAD:
        raise InvariantViolation(
            f"the constrained lane renders {Lane.HEADLINE_ONLY_LIBRARY_LEAD.value} "
            f"only; got {verdict.lane.value}")
    return HeadlineLaneEntry(
        source=getattr(item, "source", "") or "",
        date=date,
        title=getattr(item, "title", "") or "",
        nexus=nexus_word(verdict.isds_nexus),
        limitation=limitation_for(verdict.evidence_location),
        posture_subject=posture_subject,
        posture_verb=posture_verb,
        public_label=public_lane_label(verdict.lane, verdict.evidence_location),
        lane_reason=verdict.lane_reason,
    )


def forbidden_tokens_in(entry: HeadlineLaneEntry) -> tuple[str, ...]:
    """Forbidden tokens outside the quoted title, plus any in the posture clause.

    Two scopes, for the reason set out in the module docstring: the title is the
    SOURCE's words, quoted and attributed, and a headline containing "held" is
    not us holding anything. The posture clause is our sentence even though its
    words come from the title, so it is scanned as ours.
    """
    ours = " ".join(t for kind, t in entry.segments() if kind != "title").lower()
    posture = f"{entry.posture_subject} {entry.posture_verb}".lower()
    return tuple(sorted({tok for tok in FORBIDDEN_TOKENS
                         if tok in ours or tok in posture}))
