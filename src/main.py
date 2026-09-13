"""ISDS thematic watcher — orchestrator.

Run: python -m src.main [--dry-run] [--since 7d] [--no-email] [--provider gemini|claude]

The whole run is defensive: a failing source or item is logged and skipped,
never fatal. With no network the sources return []; with no API key the
classifier uses its keyword fallback — so --dry-run works fully offline.
"""

from __future__ import annotations

import argparse
import copy
import logging
import re
import sys
from dataclasses import asdict
from datetime import datetime, timedelta, timezone

from . import (classify_v2, config, council_log, locked_set, tail_audit, render,
               research_brief, research_state, rings, source_health,
               source_recovery, state, telemetry, triage)
from . import classify as classify_mod
from .classify import (TERMINAL_OUTCOMES, ClassifyOutcome, classify_item,
                       keyword_score, outcome_of, prompt_version)
from .email_send import send_digest
from .enrich import NO_BODY_FETCH, enrich, notable_quote as enrich_notable
from .sources import all_sources, base
from .sources.base import CandidateItem, parse_date

logger = logging.getLogger("isds.main")

# Sources we treat as DISABLED in the source-health table when they yield nothing:
# best-effort feeds whose robots policy disallows our crawl, so a zero from them
# reads as "suppressed", not "quiet". Empty since the Google News source was
# retired (2026-07-29); kept for the next robots-blocked feed.
ROBOTS_BLOCKED_SOURCES = set()

# The outcome VALUES after which an item is finished with. Compared as strings
# because ClassifyOutcome members hash by identity, not by their value, so a
# plain `"ok" in TERMINAL_OUTCOMES` would silently be False.
TERMINAL_VALUES = frozenset(o.value for o in TERMINAL_OUTCOMES)


# Printed in the run summary when the provider canary failed. The weekly
# workflow's provider gate greps this exact literal from the watcher's stdout
# (after the state commit) and fails the run so the failure alert fires;
# tests/test_pipeline.py keeps the two in sync.
PROVIDER_DOWN_MARKER = "!! PROVIDER DOWN"


def deferred_candidates(deferred: dict, already: set[tuple[str, str]],
                        listings: "dict[str, dict[str, str]] | None" = None) -> list:
    """Rebuild CandidateItems for queued items the current fetch did not return.

    A deferred item is not in the seen state, so if its source still lists it the
    normal fetch brings it back with fresh text and there is nothing to rebuild —
    that is the common case and the better one. This covers the item that has
    since scrolled off the feed: without it, "retry next run" would quietly mean
    "retry only if the source is slow to move on", which is not a retry policy so
    much as luck. What we can rebuild is what the queue keeps: identity, title,
    summary, published. The body is gone and enrichment may or may not get it
    back, which is exactly the honest position to retry from.

    ``listings`` maps a source name to ``{source_id: title}`` for every item that
    source LISTED this run, and it is present ONLY for sources whose listing we
    actually read. It exists for one population, and the population is why
    (2026-09-13):

    THE ELEVEN. Eleven `iareporter_headlines` items sit in the queue with no
    title and no summary, because the abandoned ledger keeps only identity and a
    URL. Their source is in ``enrich.NO_BODY_FETCH`` — it is paywalled and we do
    not fetch its article bodies, correctly and permanently — so enrichment can
    never give such an item any text. The ONLY words that will ever exist for it
    are the words the source itself put in its listing. Two rules follow, and
    they are different facts about a source that must not be collapsed:

      1. THE SOURCE STILL LISTS IT. Take the headline from the live listing. It
         is the source's own text, read from the source's own page in this run,
         and with it the item is readable and is classified like any other
         headline. What is NOT done: no article body is fetched from the
         paywalled source, and no title is mined out of the URL slug. A slug is
         our reconstruction of what a headline might have said, and the council
         has ruled that fabrication.

         BE CLEAR ABOUT WHEN THIS FIRES, because the paragraph above this one
         says the normal fetch usually gets there first: a queued item is unseen,
         so a source that still lists it returns it with its headline and the
         item never reaches this function at all — it is in ``already``. This
         branch is the backstop for the case where the two disagree, and it is
         here so that the rescue is a property of the rebuild rather than of the
         caller's bookkeeping. Rule 2 and the third case below are what change
         behaviour on the queue as it stands today.

      2. WE READ THE LISTING AND IT IS GONE. The item has scrolled off, nothing
         will ever give it text, and it is rebuilt with none — which is now a
         terminal `ClassifyOutcome.UNREADABLE` rather than a silent zero.

    AND THE THIRD CASE IS WHY ``listings`` CARRIES ABSENCE. If we could not read
    the source's listing at all this run, we know NOTHING about whether it still
    lists the URL, and "the source dropped it" and "we could not reach the
    source" are not the same fact — the same distinction the source-health table
    makes between a quiet feed and a refused one. Retiring the item on that
    would turn one bad morning at iareporter into eleven items permanently
    retired unread, which is the defect this whole change exists to end, arriving
    through the door marked "fix". So a titleless NO_BODY_FETCH item whose source
    we did not read is NOT rebuilt: it stays in the queue, uncharged, for a run
    that can actually ask.
    """
    listings = listings or {}
    out = []
    for source, source_id, entry in state.deferred_entries(deferred):
        if (source, source_id) in already:
            continue
        title = entry.get("title", "") or ""
        metadata = {"from_deferred": True,
                    "deferred_attempts": int(entry.get("attempts", 0))}
        if not title.strip() and source in NO_BODY_FETCH:
            listed = listings.get(source)
            if listed is None:
                logger.info(
                    "main: %s / %s has no title and its source was not read this "
                    "run — left queued rather than retired unread",
                    source, source_id)
                continue
            live_title = (listed.get(source_id) or "").strip()
            if live_title:
                title = live_title
                # Says where the words came from. They are the source's own, read
                # from its listing in this run — never derived from the URL.
                metadata["title_from_live_listing"] = True
                logger.info("main: recovered the headline for %s / %s from the "
                            "live listing", source, source_id)
        published = parse_date(entry.get("published")) or datetime.now(timezone.utc)
        out.append(CandidateItem(
            source=source,
            source_id=source_id,
            url=entry.get("url", "") or "",
            title=title,
            published=published,
            summary=entry.get("summary", "") or "",
            raw_text="",
            metadata=metadata,
        ))
    return out


def partition_reserved(items, reservations):
    """``(screenable, reserved)`` — the locked-set split, applied at intake.

    Council SUPPLEMENTARY RULING 2026-09-13 ¶5. An item that is in the locked
    validation set is excluded from production screening *at the moment of
    capture*: before enrichment, before triage, before classification, before any
    score for it exists anywhere. Screening one would give a locked-set item the
    instrument's own verdict and break the set's disjointness from production
    retroactively — an outcome no later edit can undo.

    Matched on ``url`` and, for the rebuilt-from-queue case where a URL was not
    kept, on ``source_id`` — which every source adapter sets to the URL anyway.
    """
    if not reservations:
        return list(items), []
    screenable, reserved = [], []
    for it in items:
        url = getattr(it, "url", "") or getattr(it, "source_id", "") or ""
        (reserved if locked_set.is_reserved(url, reservations) else screenable).append(it)
    return screenable, reserved


def _norm_line(s: str) -> str:
    """Fold curly quotes, collapse whitespace, strip wrapping quotes/case — for
    deciding whether a notable line merely restates the item's headline."""
    s = (s or "").translate({0x201c: '"', 0x201d: '"', 0x2018: "'", 0x2019: "'"})
    return re.sub(r"\s+", " ", s).strip().strip("\"'").lower()


def parse_since(spec: str) -> datetime:
    """Parse '7d', '14d', '48h', '30m' into a tz-aware UTC cutoff."""
    now = datetime.now(timezone.utc)
    m = re.fullmatch(r"\s*(\d+)\s*([dhmw])\s*", spec.lower())
    if not m:
        logger.warning("main: bad --since %r; defaulting to 7d", spec)
        return now - timedelta(days=7)
    n, unit = int(m.group(1)), m.group(2)
    delta = {"d": timedelta(days=n), "h": timedelta(hours=n),
             "m": timedelta(minutes=n), "w": timedelta(weeks=n)}[unit]
    return now - delta


# Outcomes whose SCORE must never be published, however high it is.
#
# Council rulings session of 2026-09-13, Ruling 4(d), ruled mechanically because
# row C had already made it mechanical. A tail item is classified without a body
# and, when a provider call is made for it and fails, it falls back to a keyword
# score. Until 2026-09-10 that was recorded as `keyword_only_by_design` and was
# indistinguishable from the genuine by-design case. It is not the same thing:
#
#   KEYWORD_ONLY_BY_DESIGN         no model was expected and NONE WAS CALLED
#                                  (`attempts == 0`; the offline dry-run case).
#                                  The keyword score is the intended result, so
#                                  it publishes exactly as it does today.
#   KEYWORD_AFTER_PROVIDER_ERROR   a call WAS made for this item and it failed.
#                                  The score is what an outage left behind, and
#                                  publishing it would put a number in front of
#                                  a reader that the instrument did not produce
#                                  by the route it claims to use.
#
# Suppression lives HERE, in the publication decision, and not in
# `src/classify.py`. Whether an outage's fallback score may be published is
# POLICY; what happened to the item is a FACT, and the classifier's job ends at
# the fact. Putting the policy in the classifier would also make the item
# non-terminal or unscored, and it is neither: it is finished, it has a number,
# and the number simply does not publish.
UNPUBLISHABLE_OUTCOMES = frozenset({ClassifyOutcome.KEYWORD_AFTER_PROVIDER_ERROR})


def publication_suppressed(ci) -> bool:
    """Whether this item's score may not be published, whatever it is."""
    return outcome_of(ci) in UNPUBLISHABLE_OUTCOMES


def would_surface(classified, threshold, min_items, floor,
                  fill_floor_suspended=None):
    """The items the score-and-fill rule alone would publish.

    Every item at or above ``threshold`` is included (a match; no upper cap).

    Below that sits the FILL: if fewer than ``min_items`` matched, the digest was
    topped up with the next-highest items down to ``floor``. That fill is
    SUSPENDED by default (``config.FILL_FLOOR_SUSPENDED``) while the classifier is
    under validation. It published sub-threshold items — items the instrument
    itself declined to call matches — and it did so most aggressively in the weeks
    it found least, which is exactly when its judgment is least worth borrowing
    against. Since no item has ever scored a true match, nearly everything the
    professor has been sent arrived through this path. With the fill suspended a
    thin week reports as a thin week, and an item that genuinely clears the
    threshold still clears it here.

    No item below ``floor`` is ever included under either setting.

    THIS IS NOT THE PUBLICATION DECISION. It is the counterfactual behind it:
    ``select_surfaced`` applies the validation gate on top, and the difference
    between the two lists is exactly what the gate is holding. Keeping the
    counterfactual computable is what lets a status-only cycle report the number
    of items it held instead of only reporting an absence.
    """
    if fill_floor_suspended is None:
        fill_floor_suspended = config.FILL_FLOOR_SUSPENDED
    ordered = sorted(classified, key=lambda c: c.relevance_score, reverse=True)
    surfaced = [c for c in ordered if c.relevance_score >= threshold]
    if not fill_floor_suspended and len(surfaced) < min_items:
        for c in ordered:
            if c in surfaced:
                continue
            if c.relevance_score >= floor:
                surfaced.append(c)
            if len(surfaced) >= min_items:
                break
    return surfaced


def select_surfaced(classified, threshold, min_items, floor,
                    fill_floor_suspended=None, status_only=None):
    """Choose which classified items are actually published this cycle.

    Three independent gates, in this order:

    1. ``status_only`` (``config.VALIDATION_STATUS_ONLY``, ON by default). While
       the classifier is under validation NOTHING publishes at item level — not
       fill candidates, and not items at or above the threshold. A score is the
       instrument's output, and what the instrument's output means is the open
       question; publishing on it is borrowing against an answer we do not have.
       Example 4 of ``prompts/classifier.txt`` teaches a 55 for a case with no IP
       ring and no jurisdictional ring, which is over the threshold and off the
       theme, so "only publish what clears 40" is not the safety property it
       reads as. This gate is checked FIRST and no argument to this function can
       be set such that the fill flag disables it.

    2. ``UNPUBLISHABLE_OUTCOMES`` (Ruling 4(d), 2026-09-13). An item whose score
       is a keyword fallback produced AFTER a failed provider call does not
       publish, at any score. A genuine ``keyword_only_by_design`` score — no
       provider configured, no call made, ``attempts == 0`` — publishes as
       today. The filter runs BEFORE the fill rather than after it, so a
       suppressed item does not silently occupy one of the fill's slots: the
       next eligible item takes it.

    3. the score-and-fill rule (``would_surface``).

    ``would_surface`` deliberately does NOT apply gate 2. It is the
    counterfactual — what the score-and-fill rule alone would have published —
    and the difference between the two lists is what the gates HELD. A
    suppressed item is a held item; ``src/main.py`` records the distinct reason
    per candidate in telemetry and prints the count in the run summary, so the
    holding is countable and its cause is not summarised away.

    Returning ``[]`` rather than filtering later is deliberate: every downstream
    surface — the email body, the archive folder, the article files, meta.json,
    the website — derives from this one list, so one gate here closes all of them
    at once and none of them can be reopened by a caller that forgot.
    """
    if status_only is None:
        status_only = config.VALIDATION_STATUS_ONLY
    if status_only:
        return []
    eligible = [c for c in classified if not publication_suppressed(c)]
    return would_surface(eligible, threshold, min_items, floor,
                         fill_floor_suspended)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="isds-watcher")
    p.add_argument("--dry-run", action="store_true", help="don't send email; still write digest")
    p.add_argument("--since", default="7d", help="window, e.g. 7d / 14d / 48h / 1w (default 7d)")
    p.add_argument("--no-email", action="store_true", help="skip sending email")
    p.add_argument("--provider", default=None, help="override MODEL_PROVIDER (gemini|claude)")
    p.add_argument("--limit-sources", default=None, help="CSV of source names to run (testing)")
    p.add_argument("--verbose", action="store_true", help="DEBUG logging")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    cfg = config.load_config()
    st = state.load_state()
    dq = state.load_deferred()
    bootstrap = state.is_empty(st)
    since = parse_since(args.since)
    generated_at = datetime.now(timezone.utc)
    date_str = generated_at.strftime("%Y-%m-%d")
    run_tel = telemetry.RunTelemetry(date_str)
    provider = args.provider or cfg.model_provider

    # 0. Provider canary. One trivial model call before anything is fetched or
    #    charged. 2026-09-07: the classifier had been dead for four straight
    #    weekly runs (anthropic 1.x dropped `temperature`; every call raised
    #    TypeError) and each run still reported success, deferred every enriched
    #    item, and after three such runs abandoned eight of them — the
    #    instrument's own bug counted against the items. A dead provider is now
    #    known before the first item, no attempt is charged for it, and the
    #    workflow's provider gate fails the run (after state is committed) so
    #    the failure alert fires the same day.
    classify_mod.PROVIDER_DOWN = None
    provider_down = ""
    canary_ok, canary_detail = classify_mod.provider_canary(provider)
    if canary_ok:
        logger.info("main: provider canary: %s", canary_detail)
    else:
        provider_down = canary_detail
        classify_mod.PROVIDER_DOWN = canary_detail
        logger.critical("main: PROVIDER DOWN (%s): %s — no model call will be made "
                        "this run and no candidate will be charged an attempt",
                        provider, canary_detail)

    only = set(s.strip() for s in args.limit_sources.split(",")) if args.limit_sources else None

    stats = {
        "total_candidates": 0, "classified": 0, "above_threshold": 0,
        "per_source": {}, "dropped_sources": [], "threshold": cfg.threshold,
        "provider": provider, "source_health": [],
        "retried_deferred": 0, "deferred": 0, "abandoned": 0,
        # Cost-bearing optional passes. Reported as counts so a run says what it
        # spent instead of leaving it to be reconstructed from the bill.
        "triage_ran": 0, "triage_skipped": 0, "v2_shadow_calls": 0,
        # triage_calls is ACCUMULATED with += at the triage loop, so unlike the
        # keys assigned once it must exist before the first candidate. It was
        # lost on 2026-09-13 when two branches that both edited this dict were
        # rebased onto one another and the conflict resolved toward the older
        # side, leaving the consumer without its counter: every run raised
        # KeyError and 52 tests failed on main. A key that is incremented
        # rather than assigned belongs here, beside the ones it is counted with.
        "triage_calls": 0, "triage_cost_usd": 0.0,
        # Locked-set reservations withheld from screening this run. Present from
        # the start and always a number: "we excluded none" and "we never looked"
        # are different facts and a reader must not have to tell them apart by
        # the absence of a key.
        "reserved_excluded": 0,
        # Non-empty when the provider canary failed: the detail, verbatim.
        "provider_down": provider_down,
    }

    # 1. Fetch + dedupe (per-source failure is non-fatal). Alongside the counts,
    #    capture an honest per-source SOURCE-HEALTH status so each digest shows
    #    which feeds were actually readable this run:
    #      RETURNED      — fetched and yielded N items
    #      FAILED        — fetch raised (network / parse error)
    #      HEADLINE-ONLY — paywalled feed read at headline level only (e.g. IAReporter)
    #      DISABLED      — robots-blocked / suppressed feed that yielded nothing
    #      NOT-READ (r)  — HTTP was attempted, nothing was read, nothing yielded
    #    A quiet or failed feed shows as such here — it is never hidden. NOT-READ
    #    states only what WE could read: a 403 to our runner may be our own IP
    #    class, so no status ever asserts a defect in the source itself.
    #
    #    LOCKED-SET RESERVATIONS (council SUPPLEMENTARY RULING 2026-09-13 ¶5) are
    #    applied inside this loop, on each source's fresh items, so that a
    #    reserved item is withheld at capture and the per-source SOURCE-HEALTH
    #    `count` still reports what the source ACTUALLY RETURNED. A reservation is
    #    a decision of ours about an item; it is not a fact about the feed, and it
    #    must never make a healthy source read as a quiet or failed one.
    reservations = locked_set.load_reservations()
    if reservations:
        logger.info("locked_set: %d reserved URL(s) will be withheld from screening",
                    locked_set.reserved_count(reservations))
    reserved_excluded = []
    new_candidates = []
    # source -> {source_id: title} for every item the source LISTED this run.
    # Read by `deferred_candidates`; a source ABSENT from this map is one whose
    # listing we could not read, which is a different fact from a listing that
    # does not contain a URL. See that function.
    listings: dict[str, dict[str, str]] = {}
    for src in all_sources(cfg):
        if only and src.name not in only:
            continue
        failed = False
        base.reset_fetch_log()
        try:
            items = src.fetch(since)
        except Exception as exc:  # noqa: BLE001
            logger.error("source %s failed: %s", src.name, exc)
            items = []
            failed = True
        # polite_get swallows refusals into None, so a blocked source used to
        # look exactly like a quiet one (italaw 403'd for four straight weeks
        # while every digest called it healthy). Read the outcomes instead.
        outcomes = base.get_fetch_log()
        refusals = [o for o in outcomes if o["outcome"] in ("refused", "no_contact",
                                                            "robots_disallowed")]
        reached = any(o["outcome"] == "ok" for o in outcomes)
        fresh = [it for it in items if not state.is_seen(st, src.name, it.source_id)]
        # The exclusion point. `items` (what the source returned) is untouched
        # below; only what proceeds to screening is reduced.
        fresh, held_back = partition_reserved(fresh, reservations)
        reserved_excluded.extend(held_back)
        stats["per_source"][src.name] = len(fresh)
        if not items:
            stats["dropped_sources"].append(src.name)
        if failed:
            status = "FAILED"
        elif src.name in ROBOTS_BLOCKED_SOURCES and not items:
            status = "DISABLED"
        elif refusals and not reached and not items:
            # We attempted HTTP, read nothing, and yielded nothing. Say only
            # what we could read — never that the source is at fault: a 403 to
            # our runner may be our own IP class (council standing rule,
            # 2026-08-03). Never a silently healthy zero.
            reason = refusals[0]["detail"] or refusals[0]["outcome"]
            status = f"NOT-READ ({reason})"
        elif src.name in config.HEADLINE_ONLY_SOURCES:
            status = "HEADLINE-ONLY"
        else:
            status = "RETURNED"
        if items:
            # What this source LISTED this run, whether or not each item was
            # fresh — read by `deferred_candidates` to recover the headline of a
            # queued NO_BODY_FETCH item that has none. Recorded only when the
            # source returned something: for `iareporter_headlines` an empty
            # return IS the homepage-unavailable path (`fetch_html` -> None ->
            # []), so an empty listing is a source we could not read, not a
            # source that lists nothing, and it must not be read as proof that a
            # URL is gone.
            listings[src.name] = {it.source_id: (it.title or "") for it in items}
        entry = {"name": src.name, "status": status, "count": len(items)}
        if refusals:
            # Keep the evidence: what refused us, and how.
            entry["refusals"] = [
                {"url": o["url"], "outcome": o["outcome"], "detail": o["detail"]}
                for o in refusals[:5]
            ]
            entry["refusal_count"] = len(refusals)
        stats["source_health"].append(entry)
        new_candidates.extend(fresh)

    # 1a0. Autonomous access-failure recovery. A documented-active source whose
    #      origin refused us (a confirmed NOT-READ, count 0) and which the
    #      recovery registry knows how to reach through the Internet Archive is
    #      recovered here rather than left dark: the guard reads the same content
    #      pages from the Archive, keyed to the real origin URL, and the source's
    #      status becomes RECOVERED. Because it now carries items, the zero-streak
    #      guard below no longer flags it and no SOURCE ACCESS FAILURE line
    #      reaches the email — the outage self-heals. Gated on NOT-READ (not a
    #      plain zero) so a genuinely quiet source is never fed stale archives,
    #      and skipped for --limit-sources runs. Never raises.
    if not only:
        for entry in stats["source_health"]:
            if (entry["count"] == 0
                    and str(entry.get("status", "")).startswith("NOT-READ")
                    and source_recovery.is_recoverable(entry["name"])):
                try:
                    recovered, report = source_recovery.recover_with_report(
                        entry["name"], since)
                except Exception as exc:  # noqa: BLE001 - recovery never kills a run
                    logger.error("source_recovery: %s failed (%s)", entry["name"], exc)
                    recovered, report = [], source_recovery.RecoveryReport()
                fresh_rec = [it for it in recovered
                             if not state.is_seen(st, entry["name"], it.source_id)]
                # A reserved item reached through the Archive is still reserved.
                fresh_rec, held_back = partition_reserved(fresh_rec, reservations)
                reserved_excluded.extend(held_back)
                if recovered:
                    entry["count"] = len(recovered)
                    entry["status"] = "RECOVERED (Internet Archive)"
                    # RECOVERED used to publish one number. The recovery's own
                    # telemetry — how much of the Archive's offer the per-run
                    # cap deferred, and how stale the snapshots read here are —
                    # rides under one nested key so meta.json readers that do
                    # not know about it are unaffected. Whether any of it is
                    # DISPLAYED is the site's call, not the pipeline's.
                    entry["recovery"] = asdict(report)
                    stats["per_source"][entry["name"]] = len(fresh_rec)
                    if entry["name"] in stats["dropped_sources"]:
                        stats["dropped_sources"].remove(entry["name"])
                    new_candidates.extend(fresh_rec)
                    logger.info("source_recovery: %s recovered %d page(s) "
                                "(%d new) via the Internet Archive",
                                entry["name"], len(recovered), len(fresh_rec))

    # 1a. Re-intake before new intake. Items a previous run could not classify
    #     were deferred rather than marked seen, so they are still "unseen" and a
    #     source that still lists them returns them here on its own; those are
    #     already in `new_candidates` and just carry their attempt count forward.
    #     Anything the source has since dropped is rebuilt from the queue and put
    #     FIRST, so a backlog is worked off ahead of the day's news rather than
    #     ranked against it and pushed below the enrichment cut forever.
    already = {(it.source, it.source_id) for it in new_candidates}
    returning = [it for it in deferred_candidates(dq, already, listings)
                 if not only or it.source in only]
    # An item queued by an earlier run, before its batch was locked, is reserved
    # now. The queue is left alone: it is not a publication surface, it holds no
    # score, and clearing it would erase the record that we once had the item.
    returning, held_back = partition_reserved(returning, reservations)
    reserved_excluded.extend(held_back)
    carried = sum(1 for it in new_candidates
                  if state.deferral_attempts(dq, it.source, it.source_id))
    new_candidates = returning + new_candidates
    stats["retried_deferred"] = len(returning) + carried
    stats["total_candidates"] = len(new_candidates)
    logger.info("main: %d new candidates across sources (%d retried from the "
                "deferred queue)", len(new_candidates), stats["retried_deferred"])

    # 1a-locked. The reservation, made visible and countable as ¶5 requires.
    #
    #   SEEN vs SKIPPED — the decision, and why. A reserved item is NOT marked
    #   seen. It is skipped afresh on every run, which costs nothing: the
    #   exclusion happens before enrichment and before classification, so no
    #   polite fetch and no model call is spent on it, and because it never
    #   reaches classification it can never enter the deferred queue either — the
    #   "churn the queue forever" failure mode does not exist on this path.
    #   Against that, marking seen would cost two things the ruling will not pay.
    #   First, VISIBILITY: `mark_seen` makes the item vanish from the fetch's
    #   fresh set, so this run's count would be 6 and every run after it 0, and
    #   the suppression the council ordered to be "visible and countable rather
    #   than silent" would go silent after one week. Second, REVERSIBILITY: the
    #   reservation list is DERIVED from items.json and can be corrected by
    #   correcting items.json, but a seen-state entry is a committed, permanent
    #   write that survives the correction. Skipping keeps the reservation as
    #   reversible as the thing it is derived from.
    #
    #   Each reserved item still gets a telemetry record — observed, never
    #   screened — so the exclusion is countable per item and not just in
    #   aggregate. No new telemetry stream: `surfacing.reason` already carries
    #   why an item did not appear, and "it was reserved" is one of those reasons.
    stats["reserved_excluded"] = len(reserved_excluded)
    for it in reserved_excluded:
        cid = run_tel.observe(it)
        run_tel.note_access(cid, it,
                            headline_only=it.source in config.HEADLINE_ONLY_SOURCES,
                            body_fetched=False, fetch_outcome="not_attempted")
        run_tel.note_dedup(cid, seen_before=False, marked_seen=False,
                           deferred=False, abandoned=False)
        run_tel.note_surfacing(cid, surfaced=False, reason="reserved_locked_set",
                               digest="", position=-1)
        logger.info("locked_set: RESERVED, not screened — %s / %s",
                    it.source, it.source_id)
    if reserved_excluded:
        logger.warning("locked_set: %d candidate(s) withheld from screening this "
                       "run because they are locked validation-set items",
                       len(reserved_excluded))

    # 1a. Silent-decay guard. Persist per-source consecutive-zero-run streaks
    #     (state/source_health.json); a documented-active source at 3+ zero runs
    #     has its status rewritten to "DEGRADED (N zero runs)", and an
    #     all-sources-but-one-zero run raises a COLLECTION ANOMALY warning. The
    #     warnings surface in meta.json, the digest README, and the digest
    #     header — a broken fetcher can no longer read as a quiet week.
    #     Skipped for --limit-sources runs (a partial test run must not advance
    #     the streaks of the sources it skipped or distort the anomaly check).
    if not only:
        stats["health_warnings"] = source_health.record_run(
            stats["source_health"], generated_at.strftime("%Y-%m-%d"))
    else:
        stats["health_warnings"] = []

    # 1b. First-run bootstrap (flood fix). On a genuinely empty seen-state, index
    #     every current item as already-seen and send only a baseline note — never
    #     classify or surface a historical backlog. Thematic monitoring begins next
    #     run. Respect --dry-run/--no-email (just index + save, no send).
    if bootstrap:
        for it in new_candidates:
            # Indexed, never classified — deliberately. "bootstrap" says so in
            # the state file, where "ok" would have claimed we had read them.
            cid = run_tel.observe(it)
            run_tel.note_access(cid, it,
                                headline_only=it.source in config.HEADLINE_ONLY_SOURCES,
                                body_fetched=False, fetch_outcome="not_attempted")
            run_tel.note_dedup(cid, seen_before=False, marked_seen=True,
                               deferred=False, abandoned=False)
            state.mark_seen(st, it.source, it.source_id, when=generated_at,
                            outcome="bootstrap", run=date_str)
        state.save_state(st)
        run_tel.flush()
        n = len(new_candidates)
        email_status = "skipped"
        if not (args.dry_run or args.no_email):
            subject = f"ISDS Thematic Watch — baseline established ({n} items indexed)"
            body = (f"<p>Baseline established; {n} existing items indexed. "
                    f"Thematic monitoring begins with the next run.</p>")
            email_status = "sent" if send_digest(body, subject, cfg) else "failed"
        logger.info("main: bootstrap run — indexed %d items as seen, no digest", n)
        print("\n=== ISDS Watcher run summary (baseline bootstrap) ===")
        print(f"new candidates indexed: {n}")
        print(f"locked-set reserved (excluded from screening): "
              f"{stats.get('reserved_excluded', 0)}")
        print(f"email:                  {email_status}")
        # A failed baseline send must fail the run too, so the failure alert fires
        # (consistent with the main path's "green == delivered" guarantee).
        return 1 if email_status == "failed" else 0

    # 2. Cheap keyword pre-score to rank candidates, then enrich the most
    #    promising ones (fetch their source page) so the LLM and the digest have
    #    real substance to work with. Bounds polite fetches to ENRICH_TOP_N.
    #    The keyword result is computed ONCE per candidate here and kept: the
    #    sort key used to recompute it on every comparison, and the detail behind
    #    the score (per-ring subtotals, which phrases hit, whether a negative
    #    signal fired) is what telemetry needs to explain a run later.
    lex = {}
    for it in new_candidates:
        cid = run_tel.observe(it)
        lex[id(it)] = (cid, keyword_score(it))

    # 2a. WORKSTREAM F — semantic triage, OFF by default (config.TRIAGE_ENABLED).
    #     A compact prompt over each candidate's title and summary, before any
    #     enrichment fetch, so the enrichment budget can be allocated by combined
    #     semantic/lexical rank instead of by the lexicon alone. Zero new HTTP
    #     fetches: the title and summary are already in hand.
    #
    #     Why it matters, from this repo's own probes: E5_einarsson_lexical_brittle
    #     is a paraphrase-heavy pharmaceutical-regulatory item whose expected band
    #     is HIGH and whose keyword_score is 0. Under lexical ranking it can never
    #     reach enrichment, so it can never reach classification. The model cannot
    #     miss what it is never shown.
    #
    #     Every failure is recorded as the named skip it was, and an item without
    #     a triage result keeps its lexical position (semantic_rank 0). When no
    #     item is triaged, every rank is 0 and the sort key collapses to the
    #     lexical order — so a total outage reproduces lexical ranking exactly.
    #     BOUNDED (council ruling of 2026-09-13, Ruling 4(a)). The pass is priced
    #     per candidate and the candidate count is the one quantity this pipeline
    #     does not control, so it is capped at config.TRIAGE_MAX_CALLS_PER_RUN.
    #     Above the cap the top 100 BY LEXICAL RANK are triaged and the remainder
    #     are recorded as the named skip they are. The cap is applied against a
    #     TOTAL order — (-relevance_score, source, source_id) — so which 100
    #     items are bought is a property of the candidate set rather than of
    #     fetch order, and a re-run over the same candidates buys the same 100.
    triage_results: dict = {}
    if config.TRIAGE_ENABLED:
        by_lexical_rank = sorted(
            new_candidates,
            key=lambda it: (-lex[id(it)][1]["relevance_score"],
                            getattr(it, "source", "") or "",
                            getattr(it, "source_id", "") or ""))
        within_cap = by_lexical_rank[:config.TRIAGE_MAX_CALLS_PER_RUN]
        over_cap = by_lexical_rank[config.TRIAGE_MAX_CALLS_PER_RUN:]
        for it in within_cap:
            result = triage.triage_item(it, provider=provider)
            triage_results[id(it)] = result
            stats["triage_calls"] += int(result.attempts)
            if result.ran:
                stats["triage_ran"] += 1
            else:
                stats["triage_skipped"] += 1
        for it in over_cap:
            triage_results[id(it)] = triage.skipped_over_cap()
            stats["triage_skipped"] += 1
        stats["triage_cost_usd"] = round(
            stats["triage_calls"] * config.TRIAGE_COST_PER_CALL_USD, 4)
        if over_cap:
            logger.warning(
                "triage: %d candidate(s) past the %d-call cap were not triaged "
                "and keep their lexical position", len(over_cap),
                config.TRIAGE_MAX_CALLS_PER_RUN)
        logger.info("triage: %d ranked semantically, %d skipped, %d call(s) "
                    "(~$%.4f)", stats["triage_ran"], stats["triage_skipped"],
                    stats["triage_calls"], stats["triage_cost_usd"])
    for it in new_candidates:
        run_tel.note_triage(lex[id(it)][0],
                            triage.telemetry_section(triage_results.get(id(it))))

    if config.TRIAGE_ENABLED:
        # The R2.1 total order. Total on purpose: every component is a property
        # of the candidate, so the queue does not depend on fetch order.
        triage_strengths = {
            key: (r.strengths if r.ran else None)
            for key, r in triage_results.items()}
        ranked = sorted(new_candidates, key=lambda it: triage.triage_sort_key(
            it, lexical_result=lex[id(it)][1],
            strengths=triage_strengths.get(id(it))))
    else:
        ranked = sorted(new_candidates,
                        key=lambda it: lex[id(it)][1]["relevance_score"],
                        reverse=True)
    for rank, it in enumerate(ranked):
        cid, result = lex[id(it)]
        run_tel.note_lexical(
            cid,
            per_ring_subtotal=result.get("per_ring_subtotal", {}),
            hits=[t for t in result.get("thematic_tags", [])
                  if t != "keyword_fallback"],
            negative_signal=bool(result.get("negative_signal")),
            rank=rank,
        )

    enrich_set = set(id(it) for it in ranked[:config.ENRICH_TOP_N])
    # 2026-09-11. An item rebuilt from the deferred queue with no text at all
    # (the requeue of abandoned items keeps only identity and URL) scores 0
    # lexically, never reaches the enrichment cut, is classified on an empty
    # haystack, scores 0, and is marked seen — retired without ever having been
    # read, which is the exact outcome the requeue exists to reverse. Such items
    # cannot be ranked, so they are read unconditionally, on top of the cut.
    unread_rebuilt = [it for it in ranked[config.ENRICH_TOP_N:]
                      if (it.metadata or {}).get("from_deferred")
                      and not (it.title or it.summary or it.raw_text)]
    enrich_set |= {id(it) for it in unread_rebuilt}
    if unread_rebuilt:
        logger.info("enrich: %d rebuilt item(s) with no text read on top of the "
                    "top-%d cut", len(unread_rebuilt), config.ENRICH_TOP_N)
    # Kept per item rather than only handed to telemetry: the V2 shadow derivation
    # needs to know whether a body was refused or simply never asked for, and
    # "not_attempted" and "refused" are the difference between an unreadable item
    # and an item we chose not to read.
    fetch_outcomes = {}
    for it in ranked[:config.ENRICH_TOP_N] + unread_rebuilt:
        cid = lex[id(it)][0]
        run_tel.note_enrichment(cid, True)
        # Read the polite fetcher's own log rather than inferring the outcome
        # from whether text came back: "no body" and "refused" are different
        # facts about a source and only one of them is about the source.
        base.reset_fetch_log()
        enrich(it)
        outcomes = base.get_fetch_log()
        fetch_outcome = outcomes[-1]["outcome"] if outcomes else "not_attempted"
        fetch_outcomes[id(it)] = fetch_outcome
        run_tel.note_access(
            cid, it,
            headline_only=it.source in config.HEADLINE_ONLY_SOURCES,
            body_fetched=bool((it.metadata or {}).get("enriched")),
            fetch_outcome=fetch_outcome,
        )
    for it in ranked[config.ENRICH_TOP_N:]:
        if id(it) in enrich_set:
            continue  # read above, on top of the cut
        cid = lex[id(it)][0]
        run_tel.note_access(
            cid, it,
            headline_only=it.source in config.HEADLINE_ONLY_SOURCES,
            body_fetched=False, fetch_outcome="not_attempted")

    # 3. Classify. LLM-classify the enriched top set; keyword-score the tail
    #    (keeps LLM volume bounded).
    #
    #    An item is marked seen ONLY on a terminal outcome. It used to be marked
    #    seen unconditionally, one line below the classifier call, which meant a
    #    parse failure or a provider outage permanently retired the item: the
    #    run reported it as classified, the state file said we were done with it,
    #    and no surface anywhere recorded that we had never actually read it.
    #    Non-terminal outcomes now go to the deferred queue to be retried, and
    #    after MAX_CLASSIFY_ATTEMPTS they are abandoned loudly.
    classified = []
    # Keyed by id(it) so the tail audit can pair an item's unenriched reading
    # with its enriched one: the unenriched half must be the number THIS run
    # produced, not one recomputed later, or the pair compares two readings
    # taken under different conditions and calls the difference enrichment.
    # Dropped on 2026-09-13 by a rebase that kept both writer and reader.
    classified_by_item: dict = {}
    deferred_now = []
    abandoned_now = []
    # Items that reached the classifier with no title, no summary and no body.
    # Terminal (marked seen; see ClassifyOutcome.UNREADABLE) and counted on their
    # own, because "we read it and it scored 0" and "there was nothing to read"
    # are opposite facts that this run summary used to report identically.
    unreadable_now = []
    pver = prompt_version()

    # The V2 shadow sample. `config.V2_SHADOW_CALLS` is "off" by default, so this
    # set is empty and no second call is made for any item — the shadow
    # derivation stays lexical and every telemetry record says `lexical_only`.
    # When it is "sample:N" the sample is the FIRST N of the enriched set in the
    # run's own rank order: deterministic, so a re-run of the same candidates
    # samples the same items, and bounded, so the cost of being wrong about this
    # is N calls rather than a run.
    v2_sample: set = set()
    if (config.STATE_MODEL_V2 != "off"
            and config.V2_SHADOW_CALLS_MODE != config.V2_SHADOW_CALLS_OFF):
        v2_sample = {id(it) for it in
                     ranked[:config.ENRICH_TOP_N][:config.V2_SHADOW_SAMPLE_N]}
        logger.info("rings: V2 shadow will call the model for %d of %d enriched "
                    "candidates (%s)", len(v2_sample),
                    min(len(ranked), config.ENRICH_TOP_N),
                    config.V2_SHADOW_CALLS_SPEC)

    for it in new_candidates:
        cid = lex[id(it)][0]
        intended = id(it) in enrich_set
        ci = None
        outcome_value = ""
        try:
            if intended:
                ci = classify_item(it, provider=provider, intended_model=True)
            else:
                ci = classify_item(it, provider=None, intended_model=False)
            # Merge enrichment metadata with the classifier's; the classifier's
            # LLM-selected notable_quote (if any) wins over the keyword heuristic.
            meta = {**(it.metadata or {}), **(ci.metadata or {})}
            if not meta.get("notable_quote"):
                meta["notable_quote"] = enrich_notable(
                    it.raw_text or it.summary or it.title)
            # Integrity: keep the notable line only when it is a genuine verbatim
            # line from an accessible source body — not the item's own headline,
            # and not from a paywalled/headline-only source. Otherwise drop it and
            # (for paywalled sources) mark it unavailable so the digest shows
            # "N/A" rather than passing the headline off as a quotation.
            nq = (meta.get("notable_quote") or "").strip()
            headline_only = it.source in config.HEADLINE_ONLY_SOURCES
            if nq and not headline_only and _norm_line(nq) not in _norm_line(it.title):
                meta["notable_quote"] = nq
            else:
                meta.pop("notable_quote", None)
                if headline_only:
                    meta["notable_unavailable"] = True
            ci.metadata = meta
            outcome_value = outcome_of(ci).value
        except Exception as exc:  # noqa: BLE001 - belt & braces
            # classify_item itself never raises; this guards the enrichment/
            # quote-integrity merge around it. It used to `continue`, leaving the
            # item neither classified nor seen — silently re-fetched and re-tried
            # every run forever. A failure here is a failure like any other now.
            logger.error("classify failed for %s: %s", it.source_id, exc)
            outcome_value = "pipeline_error"

        classified_by_item[id(it)] = (ci, outcome_value)
        cmeta = (getattr(ci, "metadata", None) if ci is not None else None) or {}
        # `ran` is whether a CLASSIFICATION HAPPENED, not whether an object came
        # back. An unreadable item returns a ClassifiedItem — it has to, so the
        # score-0 travels through selection and can be refused there — but no
        # classifier was applied to anything, so the record must not say one was.
        # The metadata it carries backs that up: path "none", model "", attempts 0.
        is_unreadable = outcome_value == ClassifyOutcome.UNREADABLE.value
        run_tel.note_classification(
            cid,
            ran=ci is not None and not is_unreadable,
            path=cmeta.get("classify_path", "none"),
            model=cmeta.get("model", ""),
            prompt_version=pver,
            outcome=outcome_value,
            attempts=int(cmeta.get("classify_attempts", 0) or 0),
            retried_strict=bool(cmeta.get("retried_strict")),
            model_score_advisory=cmeta.get("keyword_score_advisory"),
        )

        # 3a. Disposition FIRST, then the shadow derivation. The order matters
        #     and it changed here: "abandoned" is one of the seven R2.1
        #     classification states, it is decided in this block, and a verdict
        #     built before the decision would have to guess at it. An abandoned
        #     item is the one case that is finished AND never read, and the lane
        #     rule has to see it as such or an item we gave up on can reach a
        #     conclusion about its own contents (rings.CLASSIFIED_STATES).
        was_abandoned = False
        if outcome_value in TERMINAL_VALUES:
            # An unreadable item is appended to `classified` like any other
            # terminal item — deliberately, and it is the safer of the two
            # choices. It keeps its score of 0 in front of `select_surfaced`,
            # where the floor refuses it, rather than leaving publication to
            # depend on the item having been dropped from a list. It is subtracted
            # from the reported "classified" count below and recorded under its
            # own surfacing reason, so nothing counts it as read.
            classified.append(ci)
            if is_unreadable:
                unreadable_now.append(it)
            state.mark_seen(st, it.source, it.source_id, when=generated_at,
                            outcome=outcome_value, run=date_str)
            state.clear_deferral(dq, it.source, it.source_id)
            run_tel.note_dedup(cid, seen_before=False, marked_seen=True,
                               deferred=False, abandoned=False)
        else:
            attempts = state.record_deferral(dq, it, outcome_value, generated_at,
                                             charge=not provider_down)
            if attempts >= state.MAX_CLASSIFY_ATTEMPTS:
                entry = (dq.get(it.source) or {}).get(it.source_id) or {}
                state.append_abandoned(
                    it, outcome_value, attempts, date_str,
                    first_deferred=entry.get("first_deferred", ""))
                state.mark_seen(st, it.source, it.source_id, when=generated_at,
                                outcome="abandoned", run=date_str)
                state.clear_deferral(dq, it.source, it.source_id)
                abandoned_now.append((it, outcome_value, attempts))
                was_abandoned = True
                run_tel.note_dedup(cid, seen_before=False, marked_seen=True,
                                   deferred=False, abandoned=True)
                logger.error("main: ABANDONED %s / %s after %d attempts (%s)",
                             it.source, it.source_id, attempts, outcome_value)
            else:
                deferred_now.append((it, outcome_value, attempts))
                run_tel.note_dedup(cid, seen_before=False, marked_seen=False,
                                   deferred=True, abandoned=False)

        # 3b. STATE_MODEL_V2, in shadow. Derives the R2.1 lane from per-ring
        #     findings, the ISDS nexus, and where the evidence actually lives —
        #     and decides NOTHING. It is written to telemetry beside the score so
        #     the two derivations can be compared over a real corpus before
        #     anyone is asked to trust either. Wrapped because instrumentation
        #     that can take down the thing it measures is worse than none; logged
        #     at error level because a derivation that stops deriving silently is
        #     how a shadow run turns into no run at all.
        #
        #     The V2 CALL (`prompts/classifier_v2.txt`, strengths WITH verbatim
        #     spans) happens only for sampled candidates and only when
        #     config.V2_SHADOW_CALLS asks for it. Without it the derivation is
        #     lexical, and `v2_basis` says so on every record — a lexical
        #     derivation is never reported under a model's identity.
        if config.STATE_MODEL_V2 != "off":
            v2_result = None
            if id(it) in v2_sample:
                v2_result = classify_v2.classify_item_v2(it, provider=provider)
                stats["v2_shadow_calls"] += 1
            run_tel.note_v2_call(cid, classify_v2.telemetry_section(
                v2_result, mode=config.V2_SHADOW_CALLS_SPEC))
            v2_kwargs: dict = {}
            if v2_result is not None:
                v2_kwargs["v2_basis"] = v2_result.basis
                if v2_result.ok:
                    v2_kwargs["v2_strengths"] = v2_result.strengths
                    v2_kwargs["v2_spans"] = v2_result.spans
            try:
                cmeta_v2 = (getattr(ci, "metadata", None) or {}) if ci else {}
                verdict = rings.shadow_verdict(
                    it,
                    lexical_result=lex[id(it)][1],
                    classified=ci,
                    classification_outcome=outcome_value,
                    attempts=int(cmeta_v2.get("classify_attempts", 0) or 0),
                    retried_strict=bool(cmeta_v2.get("retried_strict")),
                    abandoned=was_abandoned,
                    headline_only=it.source in config.HEADLINE_ONLY_SOURCES,
                    body_fetched=bool((it.metadata or {}).get("enriched")),
                    fetch_outcome=fetch_outcomes.get(id(it), "not_attempted"),
                    **v2_kwargs,
                )
                run_tel.note_verdict_v2(cid, verdict, mode=config.STATE_MODEL_V2)
            except Exception as exc:  # noqa: BLE001 - shadow must never be fatal
                logger.error("rings: V2 shadow derivation failed for %s / %s: %s",
                             it.source, it.source_id, exc)
    # "classified" means READ. An unreadable item is terminal and is in
    # `classified` for the selection machinery's sake, and it is subtracted here
    # so the number a person reads is the number of items a classifier actually
    # looked at. The unreadable ones are reported on their own line below.
    stats["unreadable"] = len(unreadable_now)
    stats["classified"] = len(classified) - len(unreadable_now)
    stats["deferred"] = len(deferred_now)
    stats["abandoned"] = len(abandoned_now)

    # 3c. THE STRATIFIED TAIL AUDIT (council ruling of 2026-09-13, Ruling 4(c)).
    #     The enrichment cut decides what the model reads, and nothing has ever
    #     measured what it throws away. This samples the UN-ENRICHED tail — two
    #     items from each of three strata of `lexical_subtotal`, under a recorded
    #     seed — enriches each one, classifies it a SECOND time, and records the
    #     pair: the band the item got without a body and the band it gets with
    #     one. A difference is a flip, and a flip needs no human label, which is
    #     why this is buildable before the locked set holds a single label. See
    #     `src/tail_audit.py` for the design; this block is only the wiring.
    #
    #     THREE THINGS IT DELIBERATELY DOES NOT DO.
    #       - It does not run when the provider canary failed. Every
    #         re-classification would fall back to a keyword score and the audit
    #         would measure the outage rather than the gate.
    #       - It does not run on --dry-run. The ledger is cross-run memory: an
    #         item recorded as audited is never audited again, and a rehearsal
    #         must not spend the instrument's memory.
    #       - It works on a DEEP COPY of each sampled candidate, so the body it
    #         fetches cannot reach the published item, the telemetry record or
    #         the state file by any path at all.
    if config.TAIL_AUDIT_N and not provider_down and not args.dry_run:
        run_id = telemetry.compute_run_id(
            date_str, [lex[id(it)][0] for it in new_candidates])
        pool = []
        for it in ranked[config.ENRICH_TOP_N:]:
            if id(it) in enrich_set:
                continue  # read on top of the cut; not part of the tail
            ci_tail, outcome_tail = classified_by_item.get(id(it), (None, ""))
            if ci_tail is None:
                continue
            pool.append(tail_audit.tail_candidate(
                copy.deepcopy(it),
                lexical_subtotal=triage.lexical_subtotal(lex[id(it)][1]),
                classified=ci_tail, outcome=outcome_tail))
        prior = tail_audit.read_ledger()
        audit = tail_audit.run_audit(
            pool, run_id=run_id, enrich=enrich,
            classify=lambda item: classify_item(item, provider=provider,
                                                intended_model=True),
            per_stratum=tail_audit.per_stratum_n(),
            already_audited=tail_audit.audited_item_ids(prior))
        stats["tail_audit_calls"] = audit.calls
        stats["tail_audit_cost_usd"] = round(
            audit.calls * config.TAIL_AUDIT_COST_PER_CALL_USD, 4)
        stats["tail_audit_rows"] = tail_audit.append_rows(audit.rows)
        stats["tail_audit_shortfalls"] = dict(audit.shortfalls)
        stats["tail_audit_unmeasurable"] = audit.skipped_not_measurable
        logger.info("tail audit: %d tail item(s) in the pool, %d call(s) "
                    "(~$%.4f), %d pair(s) recorded, %d not measurable",
                    len(pool), audit.calls, stats["tail_audit_cost_usd"],
                    stats["tail_audit_rows"], audit.skipped_not_measurable)
        for stratum, short in sorted(audit.shortfalls.items()):
            logger.info("tail audit: stratum %s was %d short of the draw",
                        stratum, short)

    # 4. Select what to surface (see select_surfaced for the two gates).
    #
    #    Both lists are computed, because they answer different questions. The
    #    counterfactual says what the score-and-fill rule alone would have
    #    published; `surfaced` says what actually publishes after the validation
    #    gate. Their difference is what the gate HELD, and a held item has to be
    #    countable — a status-only cycle that could only report an absence would
    #    be indistinguishable from a cycle that found nothing, and those are very
    #    different facts about a week.
    stats["above_threshold"] = sum(
        1 for c in classified if c.relevance_score >= cfg.threshold)
    counterfactual = would_surface(
        classified, cfg.threshold, config.MIN_DIGEST_ITEMS, config.RELEVANCE_FLOOR)
    surfaced = select_surfaced(
        classified, cfg.threshold, config.MIN_DIGEST_ITEMS, config.RELEVANCE_FLOOR)
    # Identity, not equality: ClassifiedItem is a dataclass, so two genuinely
    # distinct candidates that happen to agree field-for-field compare equal.
    published_ids = {id(c) for c in surfaced}
    held = [c for c in counterfactual if id(c) not in published_ids]
    # Read by render.status_only_body via the stats dict, so the status message
    # states the count rather than implying zero. The gate flag rides along so
    # meta.json records WHY matches may exceed the items on disk — the archive
    # validator reconciles disk + held against screened matches.
    stats["held_for_review"] = len(held)
    stats["validation_status_only"] = bool(config.VALIDATION_STATUS_ONLY)
    # Held BECAUSE an outage produced the number, not because the validation
    # gate is on. Counted separately so that when the validation gate is one day
    # lifted, a run that suppressed an item still says so out loud.
    stats["suppressed_provider_error"] = sum(
        1 for c in held if publication_suppressed(c))

    # 4a. Record, per candidate, why it did or did not appear. "Not surfaced" has
    #     several different meanings — below the floor, above the floor but not
    #     needed to fill, never classified at all — and the digest shows none of
    #     them.
    folder_rel = f"digests/{render.folder_name(date_str)}"
    surfaced_ids = {id(c): pos for pos, c in enumerate(surfaced)}
    held_ids = {id(c) for c in held}
    unreadable_ids = {(u.source, u.source_id) for u in unreadable_now}
    for it in new_candidates:
        cid = lex[id(it)][0]
        match = next((c for c in classified
                      if c.source == it.source and c.source_id == it.source_id), None)
        if match is None:
            run_tel.note_surfacing(cid, surfaced=False, reason="not_classified",
                                   digest="", position=-1)
        elif (it.source, it.source_id) in unreadable_ids:
            # NOT "below_floor". Below the floor is a statement about a score,
            # and a score is a statement about text that was read. This item had
            # none, so the only true thing to say about why it did not appear is
            # that there was nothing to appear with.
            run_tel.note_surfacing(cid, surfaced=False, reason="unreadable",
                                   digest="", position=-1)
        elif id(match) in surfaced_ids:
            reason = ("at_or_above_threshold"
                      if match.relevance_score >= cfg.threshold else "watch_list_fill")
            run_tel.note_surfacing(cid, surfaced=True, reason=reason,
                                   digest=folder_rel,
                                   position=surfaced_ids[id(match)])
        elif id(match) in held_ids:
            # It would have published and a gate held it. Distinct from every
            # other not-surfaced reason on purpose — "below the floor" and
            # "cleared the threshold and was held" are the two ends of the range
            # and must never be summarised into the same absence. WHICH gate
            # held it is recorded too: an outage's fallback score and an item
            # awaiting validation are held for opposite reasons.
            reason = ("suppressed_keyword_after_provider_error"
                      if publication_suppressed(match)
                      else "held_validation_status_only")
            run_tel.note_surfacing(cid, surfaced=False, reason=reason,
                                   digest="", position=-1)
        else:
            if match.relevance_score < config.RELEVANCE_FLOOR:
                reason = "below_floor"
            elif config.FILL_FLOOR_SUSPENDED:
                # It cleared the floor and would once have filled the digest.
                # Recorded distinctly so the cost of the suspension is countable
                # rather than inferred from an absence.
                reason = "fill_suspended"
            else:
                reason = "above_floor_not_needed"
            run_tel.note_surfacing(cid, surfaced=False, reason=reason,
                                   digest="", position=-1)

    # 5. Render + write the dated archive folder (one file per surfaced item).
    folder_url = f"{config.REPO_URL}/tree/main/{folder_rel}"
    html = render.render_digest(surfaced, generated_at, since, stats, folder_url=folder_url)
    folder_path = render.write_digest_folder(html, surfaced, generated_at, stats)
    render.update_digests_index()
    digest_path = render.write_digest(html, date_str)

    # 5b. Persist state, the retry queue, and this run's telemetry — HERE, the
    #     moment the digest exists, not at the end of the run. Persistence used
    #     to be the last step, after the email and after the research brief, and
    #     the brief calls out to a model over the network with no exception
    #     handler around it despite the comment below promising one. Any raise in
    #     that block discarded the whole run's seen-state while the digest it had
    #     just written stayed on disk: every item in it came back as unseen the
    #     next day and was published a second time, re-classified, with a
    #     different score. Telefónica v. Colombia went out on 2026-06-09 at 32
    #     with one ring and again on 2026-06-10 at 28 with none. Writing the
    #     record and remembering that we wrote it are now one step apart, not
    #     three.
    state.save_state(st)
    state.save_deferred(dq)
    run_tel.flush()

    # 6. Email (unless dry-run / no-email). An EMPTY run — zero candidates screened,
    #    typically a re-run of an already-processed window where every candidate deduped
    #    as already seen — has nothing to report. "0 screened" is meaningless and an
    #    empty digest gets no synthetic content; we leave the existing archived record
    #    untouched. (The historical never-empty / watch-list-floor rule is suspended —
    #    FILL_FLOOR_SUSPENDED — and all item publication is gated by
    #    VALIDATION_STATUS_ONLY.) When candidates DO exist, gated cycles earn the
    #    status-only note from render.status_only_body, never an assertion that
    #    nothing relevant happened.
    empty_run = stats["total_candidates"] == 0
    email_status = "skipped"
    if args.dry_run or args.no_email:
        pass
    elif empty_run:
        email_status = "skipped (empty run: 0 candidates — nothing to send)"
        logger.info("empty run (0 candidates screened) — not sending a digest email; "
                    "existing record preserved")
    else:
        if len(surfaced) == 0 and held:
            # The gate held something. "none at/above 40" would be false, and
            # false in the direction that hides a real match, so the subject
            # states the holding instead.
            subject = (f"ISDS Thematic Watch — {date_str} "
                       f"(status-only cycle: {stats['total_candidates']} screened, "
                       f"{len(held)} held for operator review)")
        elif len(surfaced) == 0:
            # The subject must not assert what the body is careful not to. It
            # read "no thematically relevant developments", which is a finding
            # about the world; what we have is a reading off an instrument under
            # validation, and the two would have contradicted each other in the
            # same email.
            subject = (f"ISDS Thematic Watch — {date_str} "
                       f"(status-only cycle: {stats['total_candidates']} screened, "
                       f"none at/above {cfg.threshold})")
        else:
            subject = (f"ISDS Thematic Watch — {date_str} "
                       f"({len(surfaced)} item{'' if len(surfaced)==1 else 's'}, "
                       f"{stats['above_threshold']} at threshold)")
        # A run whose own health guard says its eyes are compromised must say
        # so in the subject line, before any count. On 2026-08-17 the subject
        # read as a routine status cycle while three primary sources sat at
        # 3+ zero runs — the outage was in the body, where a skim missed it.
        if stats.get("health_warnings"):
            subject = "[SOURCE ALERT] " + subject
        email_status = "sent" if send_digest(html, subject, cfg) else "failed"

    # 6b. Convene the research council and send the interpretive Research Brief — a
    #     second, interpretive weekly email (chairman → analyst+web search → security
    #     → editor). Skipped on --dry-run (it calls the API) and when disabled or the
    #     provider can't run it. A brief failure is logged but never affects the digest.
    #    On an empty run we also skip the brief, so a re-run cannot re-send a duplicate.
    #    Skipped too while VALIDATION_STATUS_ONLY is on: the brief is an
    #    interpretive reading of the items the digest surfaced, and under the gate
    #    there are none. A brief written over an empty surfaced list would either
    #    say nothing or reach past the gate to the held items — and it is a second
    #    email, so sending one would break the one-status-message-per-cycle rule
    #    the gate exists to keep. A skipped brief never touches the digest or the
    #    state; that path is the same one --dry-run and an empty run already take.
    brief_status = ("skipped (VALIDATION_STATUS_ONLY)"
                    if config.VALIDATION_STATUS_ONLY else "skipped")
    if (config.RESEARCH_BRIEF_ENABLED and not args.dry_run and not empty_run
            and not config.VALIDATION_STATUS_ONLY):
        # The promise in the comment above is now kept in code. It was only ever
        # a comment: an exception here propagated out of main().
        try:
            rlog = research_state.load()
            brief = research_brief.generate_brief(
                surfaced,
                prior_threads=rlog.get("open_threads", []),
                week_str=date_str,
                screened=stats["total_candidates"],
                provider=provider,
                escalated_gaps=research_state.escalated_gaps(rlog),
            )
            if brief:
                seq = research_state.record_issue(
                    rlog, date_str, brief.get("headline", ""), brief.get("open_threads", []))
                # G23: count GAP-UNRESOLVED markers deterministically; escalated gaps
                # become standing operator-action items (next analyst prompt + Monday
                # review packet) instead of endlessly re-searched dead ends.
                research_state.update_gap_counters(rlog, brief.get("_memo") or "")
                brief_html = render.render_research_brief(brief, generated_at, seq)
                brief_path = render.write_brief(brief_html, brief, generated_at, seq)
                research_state.save(rlog)
                # Record the weekly council session in the accountability ledger.
                council_log.append_weekly(date_str, seq, brief, generated_at)
                if args.no_email:
                    brief_status = f"written #{seq}"
                else:
                    subj = f"ISDS Research Brief #{seq} — {date_str}: {brief['headline']}"
                    brief_status = f"sent #{seq}" if send_digest(brief_html, subj, cfg) else "failed"
                print(f"brief:            {brief_status} ({brief_path})")
        except Exception as exc:  # noqa: BLE001 - the brief must never fail the digest
            logger.error("research brief failed (digest unaffected): %s", exc)
            brief_status = f"failed ({type(exc).__name__})"

    # 8. Summary.
    print("\n=== ISDS Watcher run summary ===")
    print(f"window since:     {since.isoformat()}")
    print(f"provider:         {provider or 'keyword-fallback'}")
    for s, n in stats["per_source"].items():
        print(f"  source {s:<22} new={n}")
    if stats["dropped_sources"]:
        print(f"dropped/empty:    {', '.join(stats['dropped_sources'])}")
    if stats["source_health"]:
        print("source health:")
        for sh in stats["source_health"]:
            print(f"  {sh['name']:<22} {sh['status']:<14} items={sh['count']}")
    for w in stats.get("health_warnings", []):
        print(f"  !! {w}")
    print(f"new candidates:   {stats['total_candidates']}")
    # Countable, every run, whether or not it fired — a suppression that only
    # prints when it happens is one a reader cannot confirm did not happen.
    print(f"locked-set reserved (excluded from screening): "
          f"{stats.get('reserved_excluded', 0)}")
    if stats.get("retried_deferred"):
        print(f"  of which retried from the deferred queue: {stats['retried_deferred']}")
    print(f"classified:       {stats['classified']}")
    # UNREADABLE IS ITS OWN LINE, not part of "classified" and not part of
    # DEGRADED. It is neither: the item was not read, so it was not classified,
    # and nothing failed — the fetch worked, the source is fine, and the run did
    # exactly the right thing. What it is, is an item retired without ever having
    # been read, and that is worth a line of its own on every run it happens.
    # The per-source health table above is untouched by this on purpose: an
    # unreadable item is not a source failure, and marking one would make a
    # working feed read as a broken one.
    if unreadable_now:
        print(f"  !! UNREADABLE (no title, no summary, no body — never read, "
              f"no model call, marked seen): {len(unreadable_now)}")
        for it in unreadable_now:
            print(f"     - {it.source} / {it.source_id}")
    # A run that could not classify part of its intake is DEGRADED, and it says
    # so here rather than reporting a smaller "classified" count and letting the
    # difference pass as a quiet week.
    if deferred_now or abandoned_now:
        by_outcome = {}
        for _it, oc, _n in deferred_now + abandoned_now:
            by_outcome[oc] = by_outcome.get(oc, 0) + 1
        detail = ", ".join(f"{k}={v}" for k, v in sorted(by_outcome.items()))
        print(f"  !! DEGRADED: {len(deferred_now) + len(abandoned_now)} of "
              f"{stats['total_candidates']} candidates could not be classified "
              f"({detail})")
        print(f"  !! deferred for retry (NOT marked seen): {len(deferred_now)}")
    if abandoned_now:
        print(f"  !! ABANDONED after {state.MAX_CLASSIFY_ATTEMPTS} attempts: "
              f"{len(abandoned_now)} — see {state.ABANDONED_PATH}")
        for it, oc, n in abandoned_now:
            print(f"     - {it.source} / {it.source_id} ({oc}, {n} attempts)")
    if provider_down:
        print(f"  {PROVIDER_DOWN_MARKER} ({provider}): {provider_down} — no model "
              f"call was made; {len(deferred_now)} item(s) queued WITHOUT an "
              f"attempt charged; the workflow's provider gate fails this run "
              f"after state is committed so the failure alert fires")
    if stats.get("triage_calls") or stats.get("triage_skipped"):
        print(f"triage:           {stats['triage_ran']} ranked semantically, "
              f"{stats['triage_skipped']} skipped, {stats['triage_calls']} call(s) "
              f"~${stats['triage_cost_usd']:.4f} (cap "
              f"{config.TRIAGE_MAX_CALLS_PER_RUN}/run)")
    if stats.get("suppressed_provider_error"):
        print(f"  !! NOT PUBLISHED: {stats['suppressed_provider_error']} item(s) "
              f"whose keyword score was produced after a failed provider call "
              f"({ClassifyOutcome.KEYWORD_AFTER_PROVIDER_ERROR.value}) — the "
              f"number is an outage's fallback and does not publish at any score")
    if stats.get("tail_audit_calls"):
        print(f"tail audit:       {stats['tail_audit_rows']} pair(s) recorded, "
              f"{stats['tail_audit_calls']} call(s) "
              f"~${stats['tail_audit_cost_usd']:.4f}"
              + (f", {stats['tail_audit_unmeasurable']} not measurable"
                 if stats.get("tail_audit_unmeasurable") else "")
              + (f", short: {stats['tail_audit_shortfalls']}"
                 if stats.get("tail_audit_shortfalls") else ""))
    print(f"at/above threshold ({cfg.threshold}): {stats['above_threshold']}")
    print(f"surfaced in digest: {len(surfaced)}")
    if config.VALIDATION_STATUS_ONLY:
        print(f"  !! VALIDATION_STATUS_ONLY: item-level publication is gated; "
              f"{len(held)} item(s) held for operator review")
    print(f"research brief:   {brief_status}")
    print(f"folder:           {folder_path}")
    print(f"digest:           {digest_path}")
    print(f"email:            {email_status}")
    # A failed send marks the whole run failed, so "green == delivered" and the
    # workflow's failure-alert step fires.
    return 1 if email_status == "failed" else 0


if __name__ == "__main__":
    sys.exit(main())
