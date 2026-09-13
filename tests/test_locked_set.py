"""Locked-set reservation — council SUPPLEMENTARY RULING 2026-09-13 ¶5.

Every test here is a way the reservation could fail open, i.e. a way a locked
validation-set item could be screened, scored and published by the instrument
that the set exists to measure. That damage is not repairable after the fact —
once a locked-set item carries the instrument's own verdict, the set's
disjointness from production is broken retroactively — so these are build
failures, not review notes.
"""

import datetime
import json
import os
import shutil
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import locked_set                                        # noqa: E402

UTC = datetime.timezone.utc
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# A real batch-1 URL shape: iareporter, path-identified, no query.
RESERVED_URL = ("https://www.iareporter.com/articles/belarusian-state-owned-entity-"
                "turns-to-russian-courts-to-challenge-arbitrator/")
OPEN_URL = "https://www.iareporter.com/articles/some-other-item-entirely/"

# Enough on-theme text that the item would certainly be screened and scored if
# the reservation failed — the test must not pass because the item was boring.
ON_THEME = ("denial of justice manifestly unjust judgment minimum standard of "
            "treatment abuse of right shell subsidiary covered investment "
            "promise utility doctrine trademark trade secret")


def _write_locked_set(root, urls, *, subdir="", raw=None):
    """Create `analytics/locked_set[/subdir]/items.json` under `root`."""
    directory = os.path.join(root, "analytics", "locked_set", subdir)
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, "items.json")
    with open(path, "w", encoding="utf-8") as fh:
        if raw is not None:
            fh.write(raw)
        else:
            json.dump([{"id": f"cat8-{i:02d}", "category": 8, "tier": "S",
                        "source_url": u, "document_title": "t",
                        "document_date": "2026-09-11", "text": "t",
                        "access_status": "paywalled"}
                       for i, u in enumerate(urls, start=1)], fh, indent=2)
    return path


def _run(tmp_path, monkeypatch, *, feed_urls, classified_sink=None,
         forbidden=RESERVED_URL, recovered_urls=None, deferred_urls=None):
    """A full offline pipeline run over `feed_urls`, in a sandboxed cwd.

    `recovered_urls` drives the Internet-Archive recovery route (intake point 2):
    the source refuses and yields nothing, so it lands on NOT-READ, and the
    recovery registry returns those URLs instead.

    `deferred_urls` drives the deferred-queue rebuild route (intake point 3):
    the queue is pre-seeded with those URLs and the feed does not list them, so
    `deferred_candidates` rebuilds them from the queue.

    Returns the parsed meta.json for the run's digest folder.
    """
    import src.main as main_mod
    import src.state as state
    from src.classify import ClassifiedItem
    from src.sources import base
    from src.sources.base import CandidateItem

    now = datetime.datetime.now(UTC)

    def _item(u):
        return CandidateItem("iareporter_headlines", u, u, "Arbitrator challenge",
                             now, ON_THEME, ON_THEME, {})

    class FakeSource:
        name = "iareporter_headlines"
        priority = "primary"

        def fetch(self, since):
            if recovered_urls is not None:
                # A refusal with nothing read and nothing yielded is what puts
                # the source on NOT-READ, which is what gates the recovery.
                base._record_outcome("https://www.iareporter.com/", "refused", "403")
                return []
            return [_item(u) for u in feed_urls]

    if recovered_urls is not None:
        monkeypatch.setattr(main_mod.source_recovery, "is_recoverable",
                            lambda name: name == "iareporter_headlines")
        monkeypatch.setattr(
            main_mod.source_recovery, "recover_with_report",
            lambda name, since: ([_item(u) for u in recovered_urls],
                                 main_mod.source_recovery.RecoveryReport()))

    def responder(item, provider=None, intended_model=False, **kw):
        """The classifier stand-in. It RAISES on a reserved item.

        The raise is the statement of intent; the recorded list below it is the
        assertion that actually bites, because `src/main.py` deliberately
        swallows an exception from this call site (a classifier failure must not
        kill a run). Both are here so that the intent survives a future change to
        that error handling.
        """
        if forbidden and (locked_set.identity(item.url)[0]
                          == locked_set.identity(forbidden)[0]):
            raise AssertionError(
                f"a reserved locked-set item reached classification: {item.url}")
        if classified_sink is not None:
            classified_sink.append(item.url)
        return ClassifiedItem(item.source, item.source_id, item.url, item.title,
                              item.published, item.summary, item.raw_text,
                              relevance_score=30, matched_rings=[],
                              thematic_tags=[], digest_summary="A. B.")

    monkeypatch.setattr(main_mod, "all_sources", lambda cfg=None: [FakeSource()])
    monkeypatch.setattr(main_mod, "enrich", lambda it: it)        # offline
    monkeypatch.setattr(main_mod, "classify_item", responder)
    monkeypatch.setattr(main_mod.config, "RESEARCH_BRIEF_ENABLED", False)
    monkeypatch.delenv("MODEL_PROVIDER", raising=False)
    shutil.copytree(os.path.join(REPO, "templates"), tmp_path / "templates")
    monkeypatch.chdir(tmp_path)
    # Pre-seed the seen-state so this is not a bootstrap run.
    state.save_state({"sources": {"iareporter_headlines": {"_seed": "t"}}},
                     "state/seen.json")
    if deferred_urls:
        state.save_deferred({"iareporter_headlines": {
            u: {"first_deferred": now.isoformat(), "attempts": 1,
                "last_outcome": "malformed_output", "url": u,
                "title": "Arbitrator challenge", "published": now.isoformat(),
                "summary": ON_THEME}
            for u in deferred_urls}})

    rc = main_mod.main(["--since", "30d", "--no-email"])
    assert rc == 0
    from src import render
    folder = os.path.join("digests",
                          render.folder_name(datetime.datetime.now(UTC)
                                             .strftime("%Y-%m-%d")))
    with open(os.path.join(folder, "meta.json"), encoding="utf-8") as fh:
        return json.load(fh)


# --------------------------------------------------------------------------- #
# 1. The exclusion itself.
# --------------------------------------------------------------------------- #

def test_a_reserved_url_never_reaches_classification(tmp_path, monkeypatch, capsys):
    _write_locked_set(tmp_path, [RESERVED_URL])
    seen = []
    meta = _run(tmp_path, monkeypatch, feed_urls=[RESERVED_URL], classified_sink=seen)
    assert RESERVED_URL not in seen
    assert seen == []
    # Nothing was screened, so nothing could be scored or published.
    assert meta["screened"] == 0
    assert meta["accepted"] == 0
    assert meta["reserved_excluded"] == 1


def test_an_unreserved_item_from_the_same_source_is_screened_exactly_as_before(
        tmp_path, monkeypatch):
    _write_locked_set(tmp_path, [RESERVED_URL])
    seen = []
    meta = _run(tmp_path, monkeypatch, feed_urls=[RESERVED_URL, OPEN_URL],
                classified_sink=seen)
    assert seen == [OPEN_URL]
    assert meta["screened"] == 1
    assert meta["reserved_excluded"] == 1
    # The reservation is OUR decision about an item, not a fact about the feed:
    # source health must still report what the source actually returned (2), or a
    # healthy source starts reading as a half-quiet one.
    health = {h["name"]: h for h in meta["source_health"]}
    assert health["iareporter_headlines"]["count"] == 2
    assert health["iareporter_headlines"]["status"] == "HEADLINE-ONLY"
    # ...while per-source screening counts report what was actually screened.
    assert meta["per_source"]["iareporter_headlines"] == 1


# The CI step is named "No locked-set item can reach production screening" and
# `src/main.py` applies the split at THREE intake points. The two tests below
# exist because the integrity officer deleted the other two guards and the full
# suite stayed green: only the fetch loop was covered, so the step asserted three
# paths while testing one. Each of these goes red when its own guard is removed.

def test_a_reserved_url_recovered_from_the_archive_never_reaches_classification(
        tmp_path, monkeypatch):
    # INTAKE POINT 2 — src/main.py, the Internet-Archive recovery block. A source
    # that refused us is re-read from the Archive, keyed to the real origin URL.
    # That is the same URL the locked set reserves, so a reservation that only
    # covered the live fetch would be bypassed by the instrument's own self-heal.
    _write_locked_set(tmp_path, [RESERVED_URL])
    seen = []
    meta = _run(tmp_path, monkeypatch, feed_urls=[],
                recovered_urls=[RESERVED_URL, OPEN_URL], classified_sink=seen)
    assert seen == [OPEN_URL]
    assert meta["reserved_excluded"] == 1
    assert meta["screened"] == 1
    # The recovery itself still reports honestly: it recovered two pages, and the
    # reservation is not allowed to make the self-heal look like a failure.
    health = {h["name"]: h for h in meta["source_health"]}
    assert health["iareporter_headlines"]["status"] == "RECOVERED (Internet Archive)"
    assert health["iareporter_headlines"]["count"] == 2


def test_a_reserved_url_rebuilt_from_the_deferred_queue_never_reaches_classification(
        tmp_path, monkeypatch):
    # INTAKE POINT 3 — src/main.py, the deferred-queue rebuild. An item queued by
    # an earlier run, before its batch was locked, is rebuilt from the queue when
    # the feed has dropped it. A rebuilt item carries no body text, so it is read
    # UNCONDITIONALLY, on top of the enrichment cut — it is the one candidate that
    # cannot be kept away from the classifier by ranking.
    _write_locked_set(tmp_path, [RESERVED_URL])
    seen = []
    meta = _run(tmp_path, monkeypatch, feed_urls=[],
                deferred_urls=[RESERVED_URL, OPEN_URL], classified_sink=seen)
    assert seen == [OPEN_URL]
    assert meta["reserved_excluded"] == 1
    assert meta["screened"] == 1
    # The queue is left alone: it is not a publication surface, it holds no score,
    # and clearing it would erase the record that we once had the item.
    import src.state as state
    assert RESERVED_URL in state.load_deferred()["iareporter_headlines"]


# --------------------------------------------------------------------------- #
# 2. Identity, not a string that can drift.
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("variant", [
    RESERVED_URL,                                        # exactly as recorded
    RESERVED_URL.rstrip("/"),                            # no trailing slash
    RESERVED_URL + "?utm_source=rss",                    # tracking query added
    RESERVED_URL.rstrip("/") + "?utm_source=rss&utm_medium=email",
    RESERVED_URL + "#comments",                          # fragment
    RESERVED_URL.replace("https://", "http://"),         # scheme
    RESERVED_URL.replace("https://www.", "https://"),    # no www
    RESERVED_URL.replace("https://www.", "HTTPS://WWW."),  # case in scheme/host
    RESERVED_URL.replace("https://www.iareporter.com",
                         "https://www.iareporter.com:443"),  # default port
])
def test_near_miss_urls_are_still_reserved(variant):
    reservations = {}
    locked_set._reserve(reservations, RESERVED_URL)
    assert locked_set.is_reserved(variant, reservations), variant


@pytest.mark.parametrize("other", [
    "https://www.iareporter.com/articles/a-different-article/",
    RESERVED_URL.rstrip("/") + "-and-more/",             # prefix, not the item
    "https://www.iareporter.com/",
    "",
    "not a url at all",
])
def test_a_different_url_is_not_reserved(other):
    reservations = {}
    locked_set._reserve(reservations, RESERVED_URL)
    assert not locked_set.is_reserved(other, reservations), other


def test_a_reserved_query_identifies_the_item_and_does_not_reserve_its_neighbour():
    # When the query IS the identity (?p=1234), dropping it would over-reserve
    # every other item on the same path. Added parameters are still absorbed.
    reservations = {}
    locked_set._reserve(reservations, "https://example.org/?p=1234")
    assert locked_set.is_reserved("http://example.org?p=1234", reservations)
    assert locked_set.is_reserved("https://example.org/?p=1234&utm_source=rss",
                                  reservations)
    assert not locked_set.is_reserved("https://example.org/?p=1235", reservations)
    assert not locked_set.is_reserved("https://example.org/", reservations)


def test_a_near_miss_url_is_excluded_by_the_running_pipeline(tmp_path, monkeypatch):
    # The normaliser is unit-tested above; this is the wiring: a feed that emits
    # the decorated form of a reserved URL must still be withheld.
    _write_locked_set(tmp_path, [RESERVED_URL])
    decorated = RESERVED_URL.rstrip("/") + "?utm_source=rss"
    seen = []
    meta = _run(tmp_path, monkeypatch, feed_urls=[decorated], classified_sink=seen)
    assert seen == []
    assert meta["reserved_excluded"] == 1
    assert meta["screened"] == 0


# --------------------------------------------------------------------------- #
# 3. Visible and countable, as ruled.
# --------------------------------------------------------------------------- #

def test_the_count_reaches_the_run_summary_and_meta_json(tmp_path, monkeypatch, capsys):
    _write_locked_set(tmp_path, [RESERVED_URL])
    meta = _run(tmp_path, monkeypatch, feed_urls=[RESERVED_URL, OPEN_URL])
    out = capsys.readouterr().out
    assert "locked-set reserved (excluded from screening): 1" in out
    assert meta["reserved_excluded"] == 1


def test_the_count_is_printed_and_recorded_as_zero_when_nothing_is_reserved(
        tmp_path, monkeypatch, capsys):
    # A suppression that only prints when it fires is one a reader cannot confirm
    # did NOT fire. Zero is a reading, not an absence.
    _write_locked_set(tmp_path, [])
    meta = _run(tmp_path, monkeypatch, feed_urls=[OPEN_URL])
    assert "locked-set reserved (excluded from screening): 0" in capsys.readouterr().out
    assert meta["reserved_excluded"] == 0


def test_the_per_item_telemetry_record_says_the_item_was_reserved(tmp_path, monkeypatch):
    _write_locked_set(tmp_path, [RESERVED_URL])
    _run(tmp_path, monkeypatch, feed_urls=[RESERVED_URL, OPEN_URL])
    from src import telemetry
    records = [json.loads(ln) for ln in
               open(telemetry.TELEMETRY_PATH, encoding="utf-8") if ln.strip()]
    reserved_cid = telemetry.candidate_id("iareporter_headlines", RESERVED_URL)
    rec = next(r for r in records if r["candidate_id"] == reserved_cid)
    assert rec["surfacing"]["reason"] == "reserved_locked_set"
    assert rec["surfacing"]["surfaced"] is False
    # Observed, never screened, and NOT marked seen — see the seen-vs-skip note
    # in src/main.py: marking it seen would silence the count after one run.
    assert rec["classification"]["ran"] is False
    assert rec["entered_enrichment"] is False
    assert rec["dedup"]["marked_seen"] is False


def test_the_reservation_is_not_recorded_as_a_source_failure(tmp_path, monkeypatch):
    # Every item this source returned is reserved. That is a fully healthy fetch
    # of a source that happens to be entirely locked, and it must not read as a
    # dropped, degraded or failed source.
    _write_locked_set(tmp_path, [RESERVED_URL, OPEN_URL])
    meta = _run(tmp_path, monkeypatch, feed_urls=[RESERVED_URL, OPEN_URL])
    assert meta["reserved_excluded"] == 2
    health = {h["name"]: h for h in meta["source_health"]}
    assert health["iareporter_headlines"]["count"] == 2
    assert health["iareporter_headlines"]["status"] == "HEADLINE-ONLY"
    assert meta["health_warnings"] == []


# --------------------------------------------------------------------------- #
# 4. Derived from items.json — never a hand-kept parallel list.
# --------------------------------------------------------------------------- #

def test_reservations_are_read_from_items_json_not_from_a_hard_coded_list(tmp_path):
    # The guard: a URL that is in NO items.json is not reserved, and a URL that is
    # in one IS — so the behaviour tracks the file rather than any list in the
    # source. A hand-kept list would drift from the set it protects.
    with_item = _write_locked_set(tmp_path, [RESERVED_URL])
    assert locked_set.is_reserved(
        RESERVED_URL, locked_set.load_reservations(str(tmp_path)))
    os.remove(with_item)
    assert not locked_set.is_reserved(
        RESERVED_URL, locked_set.load_reservations(str(tmp_path)))
    # And nothing in the shipped source hard-codes a locked-set URL.
    src_dir = os.path.join(REPO, "src")
    for name in sorted(os.listdir(src_dir)):
        if name.endswith(".py"):
            body = open(os.path.join(src_dir, name), encoding="utf-8").read()
            assert "iareporter.com/articles/" not in body, name


def test_later_batches_under_batch_n_directories_are_reserved_too(tmp_path):
    # The chairman ruled batches 2-9 live at analytics/locked_set/batch-N/. They
    # must be picked up by the same glob, with no code change per batch.
    _write_locked_set(tmp_path, [RESERVED_URL])
    _write_locked_set(tmp_path, [OPEN_URL], subdir="batch-2")
    reservations = locked_set.load_reservations(str(tmp_path))
    assert locked_set.is_reserved(RESERVED_URL, reservations)
    assert locked_set.is_reserved(OPEN_URL, reservations)
    assert locked_set.reserved_count(reservations) == 2


# --------------------------------------------------------------------------- #
# 5. Fail safe — and say which way that is.
# --------------------------------------------------------------------------- #

def test_an_absent_locked_set_directory_leaves_the_run_unchanged(
        tmp_path, monkeypatch, caplog):
    # No analytics/locked_set at all: the reservation set is empty, the item is
    # screened normally, and the pipeline does not stop collecting. A missing
    # validation artifact must never take the instrument down.
    caplog.set_level("WARNING", logger="isds.locked_set")
    seen = []
    meta = _run(tmp_path, monkeypatch, feed_urls=[OPEN_URL], classified_sink=seen,
                forbidden=None)
    assert seen == [OPEN_URL]
    assert meta["screened"] == 1
    assert meta["reserved_excluded"] == 0
    assert any("is absent" in r.getMessage() for r in caplog.records)


def test_a_corrupt_items_file_leaves_the_run_unchanged_and_warns(
        tmp_path, monkeypatch, caplog):
    caplog.set_level("WARNING", logger="isds.locked_set")
    _write_locked_set(tmp_path, None, raw="{ this is not json ")
    seen = []
    meta = _run(tmp_path, monkeypatch, feed_urls=[OPEN_URL, RESERVED_URL],
                classified_sink=seen, forbidden=None)
    # Fail-safe direction, stated out loud: an unreadable locked set reserves
    # NOTHING and screening proceeds. The cost is recorded as a warning, never
    # passed over in silence.
    assert sorted(seen) == sorted([OPEN_URL, RESERVED_URL])
    assert meta["screened"] == 2
    assert meta["reserved_excluded"] == 0
    assert any("unreadable" in r.getMessage() for r in caplog.records)


def test_a_corrupt_batch_does_not_un_reserve_a_batch_that_reads_cleanly(tmp_path, caplog):
    # The one softening of "empty on any failure": dropping batch 1's
    # reservations because batch 7 is malformed would expose items to protect
    # none.
    caplog.set_level("WARNING", logger="isds.locked_set")
    _write_locked_set(tmp_path, [RESERVED_URL])
    _write_locked_set(tmp_path, None, subdir="batch-7", raw="[[[")
    reservations = locked_set.load_reservations(str(tmp_path))
    assert locked_set.is_reserved(RESERVED_URL, reservations)
    assert any("unreadable" in r.getMessage() for r in caplog.records)


def test_an_items_file_of_the_wrong_shape_reserves_nothing_and_warns(tmp_path, caplog):
    caplog.set_level("WARNING", logger="isds.locked_set")
    _write_locked_set(tmp_path, None, raw='{"schema": 1}')
    assert locked_set.load_reservations(str(tmp_path)) == {}
    assert any("not a list" in r.getMessage() for r in caplog.records)


def test_a_reserved_url_that_carries_a_query_warns_by_item_id_and_parameter(
        tmp_path, caplog):
    # The subset rule's fatal direction, guarded by a warning rather than by
    # changing the rule. A capture recorded WITH a tracking parameter does not
    # reserve the clean URL a feed emits, and the person doing the batch-2+
    # capture is the one who can fix it — so they are told, by item id and by
    # parameter name, at the moment the file is read.
    caplog.set_level("WARNING", logger="isds.locked_set")
    _write_locked_set(tmp_path, None, raw=json.dumps([
        {"id": "cat3-04", "source_url": RESERVED_URL.rstrip("/") + "?utm_source=rss"},
        {"id": "cat3-05", "source_url": OPEN_URL},
    ]))
    reservations = locked_set.load_reservations(str(tmp_path))
    hit = [r.getMessage() for r in caplog.records if "WITH a query" in r.getMessage()]
    assert len(hit) == 1, [r.getMessage() for r in caplog.records]
    assert "cat3-04" in hit[0]
    assert "utm_source" in hit[0]
    # The clean item is not warned about, and the RULE ITSELF IS UNCHANGED: the
    # query-bearing capture still reserves only the decorated URL. The warning is
    # the fix path, not a silent relaxation of identity.
    assert "cat3-05" not in hit[0]
    assert locked_set.is_reserved(RESERVED_URL.rstrip("/") + "?utm_source=rss",
                                  reservations)
    assert not locked_set.is_reserved(RESERVED_URL, reservations)


def test_a_query_free_capture_is_not_warned_about(tmp_path, caplog):
    # Batch 1 is entirely query-free and must produce no capture warning at all,
    # or the signal is already noise by the time batch 2 lands.
    caplog.set_level("WARNING", logger="isds.locked_set")
    _write_locked_set(tmp_path, [RESERVED_URL, OPEN_URL])
    locked_set.load_reservations(str(tmp_path))
    assert not [r for r in caplog.records if "query" in r.getMessage()]


def test_an_items_wrapper_object_is_accepted(tmp_path):
    # Tolerated so a future schema revision cannot silently reserve nothing.
    _write_locked_set(tmp_path, None,
                      raw=json.dumps({"items": [{"source_url": RESERVED_URL}]}))
    assert locked_set.is_reserved(RESERVED_URL,
                                  locked_set.load_reservations(str(tmp_path)))


def test_an_item_without_a_usable_source_url_is_skipped_not_fatal(tmp_path, caplog):
    caplog.set_level("WARNING", logger="isds.locked_set")
    _write_locked_set(tmp_path, None, raw=json.dumps(
        [{"id": "a"}, {"source_url": ""}, {"source_url": RESERVED_URL}, "junk"]))
    reservations = locked_set.load_reservations(str(tmp_path))
    assert locked_set.reserved_count(reservations) == 1
    assert locked_set.is_reserved(RESERVED_URL, reservations)


def test_identity_never_raises_on_junk():
    for junk in ["", None, "http://[oops", "::::", "https://", "a b c"]:
        assert isinstance(locked_set.identity(junk), tuple)
    assert locked_set.is_reserved("http://[oops", {"x": (frozenset(),)}) is False
