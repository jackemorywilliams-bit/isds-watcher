"""Unit tests for the ISDS watcher: state bootstrap, scoring bands, parsing,
config, and rendering. No network or API key required."""

import datetime
import json
import os
import sys

import pytest
import yaml

from src import config, state
from src.classify import keyword_score, parse_json_response, classify_item
from src.main import parse_since
from src.sources.base import CandidateItem, parse_date

UTC = datetime.timezone.utc


def _item(title="t", summary="", raw=""):
    now = datetime.datetime.now(UTC)
    return CandidateItem("test", title, "http://x", title, now, summary, raw, {})


# --- state -------------------------------------------------------------------
def test_state_bootstrap_when_missing(tmp_path):
    p = tmp_path / "seen.json"
    st = state.load_state(str(p))
    assert st == {"sources": {}}


def test_state_corrupt_treated_empty(tmp_path):
    p = tmp_path / "seen.json"
    p.write_text("{not valid json")
    assert state.load_state(str(p)) == {"sources": {}}


def test_state_mark_and_roundtrip(tmp_path):
    p = tmp_path / "seen.json"
    st = state.load_state(str(p))
    state.mark_seen(st, "iisd_itn", "id-1")
    assert state.is_seen(st, "iisd_itn", "id-1")
    state.save_state(st, str(p))
    again = state.load_state(str(p))
    assert state.is_seen(again, "iisd_itn", "id-1")
    assert not state.is_seen(again, "iisd_itn", "id-2")


# --- since parsing -----------------------------------------------------------
def test_parse_since_units():
    now = datetime.datetime.now(UTC)
    assert (now - parse_since("7d")).days in (6, 7)
    assert (now - parse_since("48h")).total_seconds() >= 47 * 3600
    # bad input falls back to 7d
    assert (now - parse_since("garbage")).days in (6, 7)


def test_parse_since_is_tz_aware():
    assert parse_since("7d").tzinfo is not None


# --- digest selection / padding floor -----------------------------------------
def _classified(score, sid=None):
    from src.classify import ClassifiedItem
    now = datetime.datetime.now(UTC)
    return ClassifiedItem("s", sid or f"id{score}", "u", "t", now, "", "",
                          relevance_score=score)


# These two test the score-and-fill RULE, which lives in would_surface.
# select_surfaced is that rule plus the validation gate on top, and while the gate
# is on it returns [] for any input — which would make these two pass for the
# wrong reason and stop testing the floor at all.
def test_select_surfaced_never_below_floor():
    from src.main import would_surface
    items = [_classified(s) for s in (80, 45, 30, 24, 10, 0)]
    out = would_surface(items, threshold=40, min_items=6, floor=25)
    # No item below the floor may ever be surfaced.
    assert all(c.relevance_score >= 25 for c in out)
    # Every match (>= threshold) is included, with no upper cap.
    assert {c.relevance_score for c in out} >= {80, 45}
    # The 30 (>= floor) fills toward the minimum; 24/10/0 never appear.
    assert 24 not in {c.relevance_score for c in out}


def test_select_surfaced_quiet_week_is_empty_not_padded():
    from src.main import would_surface
    # Nothing above the floor -> empty digest rather than padding to min_items.
    items = [_classified(s) for s in (24, 10, 0)]
    assert would_surface(items, threshold=40, min_items=6, floor=25) == []


# --- first-run bootstrap (index without surfacing) ----------------------------
def test_main_nonempty_subject_builds(tmp_path, monkeypatch):
    # Regression: the non-empty email subject must build (it referenced a removed
    # variable). Exercises the surfaced>0 path with the email block active.
    import src.main as main_mod
    import src.state as state
    from src.sources.base import CandidateItem
    now = datetime.datetime.now(UTC)
    on_theme = ("denial of justice manifestly unjust judgment minimum standard of "
                "treatment abuse of right shell subsidiary covered investment "
                "promise utility doctrine trademark trade secret")

    class FakeSource:
        name = "iisd_itn"
        priority = "primary"
        def fetch(self, since):
            return [CandidateItem("iisd_itn", "cand-1", "http://x/1",
                                  "Patent denial of justice", now, on_theme, on_theme, {})]

    monkeypatch.setattr(main_mod, "all_sources", lambda cfg=None: [FakeSource()])
    monkeypatch.setattr(main_mod, "enrich", lambda it: it)      # offline
    monkeypatch.delenv("MODEL_PROVIDER", raising=False)          # keyword fallback
    # Explicit override: this test is about the surfaced>0 subject line, which is
    # unreachable while the validation gate is on.
    monkeypatch.setattr(main_mod.config, "VALIDATION_STATUS_ONLY", False)
    captured = {}
    monkeypatch.setattr(main_mod, "send_digest",
                        lambda html, subject, cfg, **k: captured.update(subject=subject) or True)
    # Render needs the templates/ dir relative to cwd; copy it into the sandbox.
    import shutil
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    shutil.copytree(os.path.join(repo, "templates"), tmp_path / "templates")
    monkeypatch.chdir(tmp_path)
    # Pre-seed state so this is NOT a bootstrap run (so the item actually surfaces).
    state.save_state({"sources": {"iisd_itn": {"_seed": "t"}}}, "state/seen.json")

    rc = main_mod.main(["--since", "30d"])   # no --no-email -> builds the subject
    assert rc == 0
    assert "at threshold)" in captured.get("subject", "")


def test_counts_consistent_across_surfaces(tmp_path, monkeypatch):
    # Fix 1: the email footer, meta.json, and the website build must report the
    # SAME screened / matches / accepted numbers for one run, with one definition.
    import json
    import shutil
    import importlib
    from pathlib import Path
    from src import render
    from src.classify import ClassifiedItem
    now = datetime.datetime.now(UTC)
    # One sub-threshold watch-list lead; 80 screened; 0 matches; 1 accepted (shown).
    items = [ClassifiedItem("iisd_itn", "u1", "http://x/1", "Case A", now, "s", "r",
                            relevance_score=30, matched_rings=[], thematic_tags=[],
                            digest_summary="A. B.")]
    stats = {"total_candidates": 80, "above_threshold": 0, "threshold": 40,
             "classified": 80, "per_source": {"iisd_itn": 80}, "dropped_sources": [],
             "provider": "claude"}
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    shutil.copytree(os.path.join(repo, "templates"), tmp_path / "templates")
    monkeypatch.chdir(tmp_path)

    html = render.render_digest(items, now, now, stats)
    assert "Screened: 80" in html
    assert "Matches (&ge;40): 0" in html
    assert "Watch-list leads shown: 1" in html
    # Fix 2: header splits matches from watch-list leads (no bare "1 item").
    assert "0 matches &middot; 1 watch-list lead" in html
    # Two labeled sections, with the empty "Direct matches" block called out.
    assert "Direct matches" in html and "Watch-list near-matches" in html
    assert "No direct matches this week" in html

    folder = render.write_digest_folder(html, items, now, stats)
    meta = json.loads(Path(folder, "meta.json").read_text())
    assert (meta["screened"], meta["matches"], meta["accepted"], meta["watch_list_leads"]) \
        == (80, 0, 1, 1)

    sys.path.insert(0, os.path.join(repo, "scripts"))
    bs = importlib.import_module("build_site")
    accepted, matches, screened, _per_source, _accepted_by_source = bs._resolve_counts(
        Path(folder), 80, len(items))
    assert (screened, matches, accepted) == (80, 0, 1)


def test_empty_rerun_does_not_clobber_existing_record(tmp_path, monkeypatch):
    # Run identity is keyed by date. A same-day empty re-run (0 screened, 0
    # surfaced — e.g. everything already deduped against state) must NOT overwrite
    # a substantive record already written for that date.
    import json
    import shutil
    from pathlib import Path
    from src import render
    from src.classify import ClassifiedItem
    now = datetime.datetime.now(UTC)
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    shutil.copytree(os.path.join(repo, "templates"), tmp_path / "templates")
    monkeypatch.chdir(tmp_path)

    # 1) A real run for the date: 80 screened, 1 surfaced watch-list lead.
    real = [ClassifiedItem("iisd_itn", "u1", "http://x/1", "Case A", now, "s", "r",
                           relevance_score=30, matched_rings=[], thematic_tags=[],
                           digest_summary="A. B.")]
    real_stats = {"total_candidates": 80, "above_threshold": 0, "threshold": 40,
                  "per_source": {"iisd_itn": 80}, "provider": "claude"}
    html = render.render_digest(real, now, now, real_stats)
    folder = render.write_digest_folder(html, real, now, real_stats)
    assert (tmp_path / folder / "articles" / "01_case-a.md").exists() or \
        list((tmp_path / folder / "articles").glob("*.md"))

    # 2) An empty re-run for the SAME date must preserve the substantive record.
    empty_stats = {"total_candidates": 0, "above_threshold": 0, "threshold": 40,
                   "per_source": {}, "provider": "claude"}
    empty_html = render.render_digest([], now, now, empty_stats)
    render.write_digest_folder(empty_html, [], now, empty_stats)
    meta = json.loads(Path(folder, "meta.json").read_text())
    assert (meta["screened"], meta["matches"], meta["accepted"]) == (80, 0, 1)
    assert list((tmp_path / folder / "articles").glob("*.md"))  # article survived

    # 3) A non-empty re-run (legitimate correction) DOES overwrite.
    corr = [real[0], ClassifiedItem("italaw", "u2", "http://x/2", "Case B", now,
                                    "s", "r", relevance_score=55, matched_rings=["R2"],
                                    thematic_tags=[], digest_summary="C. D.")]
    corr_stats = {"total_candidates": 90, "above_threshold": 1, "threshold": 40,
                  "per_source": {"iisd_itn": 45, "italaw": 45}, "provider": "claude"}
    render.write_digest_folder(render.render_digest(corr, now, now, corr_stats),
                               corr, now, corr_stats)
    meta = json.loads(Path(folder, "meta.json").read_text())
    assert (meta["screened"], meta["matches"], meta["accepted"]) == (90, 1, 2)


def test_cumulative_digest_relabels_counts_vs_per_run(tmp_path, monkeypatch):
    # The aggregate pools many runs; its counts MUST be labeled cumulative so a
    # reader never reads its "Screened: 251" as the website's per-run "Screened: 80".
    import shutil
    from src import render
    from src.classify import ClassifiedItem
    now = datetime.datetime.now(UTC)
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    shutil.copytree(os.path.join(repo, "templates"), tmp_path / "templates")
    monkeypatch.chdir(tmp_path)
    items = [ClassifiedItem("italaw", "u", "http://x", "Case", now, "s", "r",
                            relevance_score=30, matched_rings=[], thematic_tags=[],
                            digest_summary="A. B.")]
    stats = {"total_candidates": 251, "above_threshold": 0, "threshold": 40,
             "per_source": {"a": 1}, "provider": "claude"}

    per_run = render.render_digest(items, now, now, stats)
    assert "Screened:" in per_run and "cumulative" not in per_run.lower()

    agg = render.render_digest(items, now, now, stats, cumulative_runs=4)
    assert "Cumulative across 4 bring-up runs" in agg
    assert "Screened (cumulative): 251" in agg
    assert "Bring-up to date (4 runs)" in agg
    assert "watch-list lead" in agg and "collected" in agg


def test_italaw_uses_real_case_name_not_view_details():
    # Regression: the homepage /cases/<id> link always reads "View case details";
    # the real case name lives in the sibling /node/<id> link. The parser must use
    # the case name, never the generic label.
    from bs4 import BeautifulSoup
    from src.sources.italaw import ItalawSource
    html = """
    <div class="view-content">
      <div class="views-row views-row-1">
        <span class="date-display-single">11 Jun 2026</span>
        <a href="/node/9748">Windstream Energy v. Canada (II)</a>
        <div class="views-field views-field-view-node">
          <span class="field-content"><a href="/cases/9748">View case details</a></span>
        </div>
      </div>
      <div class="views-row views-row-2">
        <span class="date-display-single">9 Jun 2026</span>
        <a href="/node/10666">Silver Bull v. Mexico</a>
        <span class="field-content"><a href="/cases/10666">View case details</a></span>
      </div>
    </div>
    """
    items = ItalawSource()._parse_primary(BeautifulSoup(html, "html.parser"))
    titles = {it.url.rsplit("/", 1)[-1]: it.title for it in items}
    assert titles["9748"] == "Windstream Energy v. Canada (II)"
    assert titles["10666"] == "Silver Bull v. Mexico"
    assert all("View case details" not in it.title for it in items)


def test_main_bootstrap_indexes_without_surfacing(tmp_path, monkeypatch):
    import glob
    import src.main as main_mod
    import src.state as state
    from src.sources.base import CandidateItem
    now = datetime.datetime.now(UTC)

    class FakeSource:
        name = "iisd_itn"
        priority = "primary"
        def fetch(self, since):
            return [CandidateItem("iisd_itn", f"id{i}", f"http://x/{i}",
                                  f"title {i}", now, "s", "r", {}) for i in range(3)]

    monkeypatch.setattr(main_mod, "all_sources", lambda cfg=None: [FakeSource()])
    monkeypatch.chdir(tmp_path)

    rc = main_mod.main(["--dry-run", "--since", "7d", "--no-email"])
    assert rc == 0

    # Every fetched item is now indexed as seen...
    st = state.load_state("state/seen.json")
    assert not state.is_empty(st)
    assert all(state.is_seen(st, "iisd_itn", f"id{i}") for i in range(3))
    # ...but the bootstrap run surfaced nothing: no dated digest folder was written.
    assert glob.glob("digests/*_ISDS-Thematic-Watch") == []


# --- date parsing ------------------------------------------------------------
def test_google_alerts_resolve_redirect():
    from src.sources.google_alerts import resolve_redirect, GoogleAlertsSource
    g = "https://www.google.com/url?rct=j&sa=t&url=https://www.iareporter.com/articles/x/&ct=ga"
    assert resolve_redirect(g) == "https://www.iareporter.com/articles/x/"
    # a plain (non-redirect) link is returned unchanged
    assert resolve_redirect("https://example.org/a") == "https://example.org/a"
    # no feeds configured -> inactive, returns [] (never raises)
    assert GoogleAlertsSource().fetch(datetime.datetime.now(UTC)) == []


def test_parse_scholar_email(monkeypatch):
    from src.sources.gmail_scholar import parse_scholar_email, GmailScholarSource
    html = (
        "<div>"
        '<h3><a href="https://scholar.google.com/scholar_url?url=https://example.org/paper1&hl=en">'
        "Title One</a></h3>"
        "<div>A. Author, B. Author - Journal, 2026</div>"
        '<h3><a href="https://scholar.google.com/scholar_url?url=https://example.org/paper2&hl=en">'
        "Title Two</a></h3>"
        "<div>C. Author - Other Journal, 2026</div>"
        "</div>"
    )
    entries = parse_scholar_email(html)
    assert len(entries) == 2
    assert entries[0]["title"] == "Title One"
    assert entries[0]["url"] == "https://example.org/paper1"
    assert entries[1]["title"] == "Title Two"
    assert entries[1]["url"] == "https://example.org/paper2"

    # no credentials -> inactive, returns [] (never raises)
    monkeypatch.delenv("GMAIL_ALERT_USER", raising=False)
    monkeypatch.delenv("GMAIL_ALERT_PASS", raising=False)
    assert GmailScholarSource().fetch(datetime.datetime.now(UTC)) == []


def test_gmail_scholar_finds_unlabeled_alerts_in_all_mail(monkeypatch):
    """The alerts arrive but are not filed under the dedicated label (no Gmail
    filter). The label mailbox reads empty; the source must still find them by
    searching [Gmail]/All Mail, scoped to the Scholar sender."""
    import src.sources.gmail_scholar as gs

    html = (
        '<h3><a href="https://scholar.google.com/scholar_url?url=https://example.org/p1&hl=en">'
        "Paper One</a></h3><div>A. Author - Journal, 2026</div>"
    )
    raw = (
        b"From: scholaralerts-noreply@google.com\r\n"
        b"Date: Mon, 24 Aug 2026 13:00:00 +0000\r\n"
        b'Content-Type: text/html; charset="utf-8"\r\nMIME-Version: 1.0\r\n\r\n'
        + html.encode("utf-8")
    )

    class _FakeIMAP:
        def __init__(self, *a, **k):
            self.selected = None

        def login(self, u, p):
            return ("OK", [b""])

        def select(self, mailbox, readonly=False):
            self.selected = mailbox
            return ("OK", [b"1"])

        def search(self, charset, *criteria):
            if self.selected == '"[Gmail]/All Mail"':
                return ("OK", [b"101"])
            return ("OK", [b""])

        def fetch(self, uid, spec):
            return ("OK", [(b"101 (RFC822 {%d}" % len(raw), raw)])

        def close(self):
            pass

        def logout(self):
            pass

    monkeypatch.setattr(gs.imaplib, "IMAP4_SSL", _FakeIMAP)
    monkeypatch.setenv("GMAIL_ALERT_USER", "wemory531@gmail.com")
    monkeypatch.setenv("GMAIL_ALERT_PASS", "app-password")
    since = datetime.datetime(2026, 8, 20, tzinfo=UTC)
    items = gs.GmailScholarSource().fetch(since)
    assert len(items) == 1
    assert items[0].url == "https://example.org/p1"
    assert items[0].title == "Paper One"
    assert items[0].source == "gmail_scholar"


def test_parse_date_to_utc():
    d = parse_date("Tue, 21 Apr 2026 17:02:05 +0000")
    assert d is not None and d.tzinfo is not None
    assert parse_date("not a date") is None
    assert parse_date(None) is None


# --- scoring bands (the calibrated few-shot gold set) ------------------------
def test_scorer_matches_fingerprint_examples():
    fp = yaml.safe_load(open("fingerprint.yaml"))
    for ex in fp["few_shot_examples"]:
        r = keyword_score(_item(ex["title"], ex["summary"], ex["summary"]))
        s = r["relevance_score"]
        band = "HIGH" if s >= 70 else "MEDIUM" if s >= 40 else "LOW"
        assert band == ex["expected_band"], f"{ex['title']}: got {s} ({band})"


def test_fingerprint_examples_declare_the_score_they_actually_get():
    """The band alone was the only field ever asserted, and under that cover all seven
    expected_score values drifted wrong (88/84/58/52/12/8/10 against 73/75/40/56/7/0/7)
    while every band still passed. A band is a wide target; a score is not. Asserting
    the score means a lexicon re-weighting has to re-measure this set on purpose."""
    fp = yaml.safe_load(open("fingerprint.yaml"))
    for ex in fp["few_shot_examples"]:
        r = keyword_score(_item(ex["title"], ex["summary"], ex["summary"]))
        assert r["relevance_score"] == ex["expected_score"], (
            f"{ex['title']}: scored {r['relevance_score']}, "
            f"fingerprint.yaml declares {ex['expected_score']}")


def test_fingerprint_examples_declare_the_rings_they_actually_get():
    """matched_rings records what keyword_score RETURNS — every ring with any nonzero
    hit, sub-floor brushes included — not the rings that are PRESENT for scoring. Four
    of the seven lists were wrong while unasserted. Comparing lists, not sets, also
    pins the emission order to fingerprint.yaml's ring order."""
    fp = yaml.safe_load(open("fingerprint.yaml"))
    for ex in fp["few_shot_examples"]:
        r = keyword_score(_item(ex["title"], ex["summary"], ex["summary"]))
        assert r["matched_rings"] == ex["matched_rings"], (
            f"{ex['title']}: matched {r['matched_rings']}, "
            f"fingerprint.yaml declares {ex['matched_rings']}")


def test_every_fingerprint_example_carries_all_four_declared_fields():
    """A field deleted rather than corrected is how the previous drift would come back:
    the two tests above pass vacuously over an example that declares neither."""
    fp = yaml.safe_load(open("fingerprint.yaml"))
    assert fp["few_shot_examples"], "the gold set is empty"
    for ex in fp["few_shot_examples"]:
        for field in ("expected_band", "expected_score", "matched_rings", "why"):
            assert field in ex, f"{ex['title']}: missing {field}"


def test_the_scoring_boundaries_the_yaml_documents_are_the_ones_the_code_applies():
    """fingerprint.yaml's combination_rules are descriptive only — nothing reads them,
    which is how they came to describe a "subtotal >= 30" bar that exists nowhere in
    src/classify.py and had never changed a score. These are the three boundaries the
    rewritten block states, measured against the live scorer."""
    from src.classify import PRESENT_FLOOR, STRONG_SUBTOTAL
    assert (PRESENT_FLOOR, STRONG_SUBTOTAL) == (12, 18)

    # one ring exactly at the floor (abuse of right = 12), no second ring -> LOW
    assert keyword_score(_item("t", "", "abuse of right"))["relevance_score"] == 28
    # the same ring plus a single 1-point brush elsewhere (copyright = 1) -> a MATCH
    assert keyword_score(
        _item("t", "", "abuse of right copyright"))["relevance_score"] == 41
    # one ring at the strong-single-ring floor (12+3+2+1 = 18), no second ring -> MEDIUM
    assert keyword_score(_item("t", "", "abuse of right exhaustion of local remedies "
                                        "denial of benefits substantial business "
                                        "activities"))["relevance_score"] == 40
    # the extra-weight ring alone, at the floor (7+5 = 12) -> MEDIUM, not LOW
    assert keyword_score(
        _item("t", "", "domestic court arbitrary or discriminatory")
    )["relevance_score"] == 45


def test_scorer_rejects_offtheme():
    r = keyword_score(_item("Ferrer v. Ecuador", "ICSID case registered", ""))
    assert r["relevance_score"] < 40
    assert "keyword_fallback" in r["thematic_tags"]


# --- JSON parsing (LLM response robustness) ----------------------------------
def test_parse_json_strips_fences():
    raw = '```json\n{"relevance_score": 80, "matched_rings": ["ip_as_investment"], ' \
          '"thematic_tags": ["patent"], "digest_summary": "A. B."}\n```'
    out = parse_json_response(raw)
    assert out and out["relevance_score"] == 80
    assert out["matched_rings"] == ["ip_as_investment"]


def test_parse_json_rejects_garbage():
    assert parse_json_response("not json at all") is None


# --- verbatim-quote integrity -------------------------------------------------
def test_quote_in_source_accepts_verbatim_and_curly():
    from src.classify import _quote_in_source
    it = _item("Title", "", "The tribunal found the ruling manifestly unjust and shocking.")
    # exact substring
    assert _quote_in_source("the ruling manifestly unjust and shocking", it)
    # only differs by curly quotes / em dash typography
    it2 = _item("T", "", 'He called it an "abuse of right" — a clear one indeed.')
    assert _quote_in_source('an “abuse of right” — a clear one indeed', it2)


def test_quote_in_source_rejects_paraphrase_and_short():
    from src.classify import _quote_in_source
    it = _item("Title", "", "The tribunal dismissed the claim on abuse of right grounds.")
    # a paraphrase that is not actually in the text
    assert not _quote_in_source("the panel threw out the case for treaty shopping reasons", it)
    # too short to be meaningful
    assert not _quote_in_source("abuse", it)


def test_parse_json_coerces_invalid_rings():
    raw = '{"relevance_score": 50, "matched_rings": ["ip_as_investment", "bogus"], ' \
          '"thematic_tags": [], "digest_summary": "A. B."}'
    out = parse_json_response(raw)
    assert "bogus" not in out["matched_rings"]
    assert "ip_as_investment" in out["matched_rings"]


# --- classify_item offline fallback path (no provider/key) -------------------
def test_classify_item_offline_never_raises(monkeypatch):
    monkeypatch.delenv("MODEL_PROVIDER", raising=False)
    ci = classify_item(_item("Patent dispute", "promise utility doctrine denial of justice", ""))
    assert ci.relevance_score >= 0
    assert isinstance(ci.matched_rings, list)


def test_classify_records_model_in_metadata(monkeypatch):
    # Offline path records the keyword model; the LLM paths record the model ID.
    monkeypatch.delenv("MODEL_PROVIDER", raising=False)
    ci = classify_item(_item("t", "denial of justice supreme court", ""))
    assert ci.metadata.get("model") == "keyword"


def test_resolved_model_ids():
    from src.classify import _resolved_model, DEFAULT_ANTHROPIC_MODEL, DEFAULT_GEMINI_MODEL
    assert _resolved_model("anthropic") == DEFAULT_ANTHROPIC_MODEL
    assert _resolved_model("gemini") == DEFAULT_GEMINI_MODEL
    assert _resolved_model(None) is None


# --- config ------------------------------------------------------------------
def test_recipients_hardcoded():
    # Temporarily narrowed to a single recipient on request.
    assert config.RECIPIENTS == ["jackemorywilliams@icloud.com"]


def test_missing_email_secrets_detected():
    cfg = config.Config(smtp_user=None, smtp_pass=None)
    miss = config.missing_email_secrets(cfg)
    assert "SMTP_USER" in miss and "SMTP_PASS" in miss


# --- render ------------------------------------------------------------------
def test_render_empty_and_populated():
    from src import render
    from src.classify import ClassifiedItem
    now = datetime.datetime.now(UTC)
    stats = {"total_candidates": 0, "classified": 0, "above_threshold": 0,
             "per_source": {"iisd_itn": 0}, "dropped_sources": [], "threshold": 60,
             "provider": None}
    empty = render.render_digest([], now, now, stats)
    # The zero-state no longer claims nothing relevant happened — it reports what
    # the instrument returned. Asserted against the authoritative copy, not a
    # retyped fragment of it.
    assert render.status_only_body(0, 60) in empty

    ci = ClassifiedItem("iisd_itn", "id", "http://x", "Patent case", now,
                        "s", "r", relevance_score=85,
                        matched_rings=["ip_as_investment"], thematic_tags=["patent"],
                        digest_summary="One. Two.")
    ci.metadata = {"notable_quote": "A notable doctrinal line."}
    stats["above_threshold"] = 1
    html = render.render_digest([ci], now, now, stats)
    assert "Patent case" in html and "85" in html
    assert "notable doctrinal line" in html


# =============================================================================
# Seen-state, deferral, and abandonment (Phase 1)
#
# The unifying question behind these: when the classifier does not produce an
# answer, what does the run remember? It used to remember "processed" — the item
# was marked seen one line below the classifier call, whatever had happened, so a
# provider outage and a clean classification left identical records and the
# failure was unrecoverable by the next run and invisible to every surface.
# =============================================================================
ON_THEME = ("denial of justice manifestly unjust judgment minimum standard of "
            "treatment abuse of right shell subsidiary covered investment "
            "promise utility doctrine trademark trade secret")
OFF_THEME = "The weather forecast for tomorrow is mild with light winds."

GOOD_JSON = json.dumps({"relevance_score": 80,
                        "matched_rings": ["ip_as_investment"],
                        "thematic_tags": ["patent"],
                        "digest_summary": "A tribunal ruled. It mattered."})


def _cand(sid, title="Patent denial of justice", text=ON_THEME, source="iisd_itn"):
    from src.sources.base import CandidateItem
    return CandidateItem(source, sid, f"http://x/{sid}", title,
                         datetime.datetime.now(UTC), text, text, {})


def _sandbox(tmp_path, monkeypatch, items, responder, *, status_only=False):
    """An isolated watcher install whose provider answers with ``responder``.

    Returns a callable that runs main() once. The provider is real
    ``classify_item`` machinery with only the HTTP call swapped, so these tests
    exercise the actual parse/retry/fallback paths rather than a mock of them.

    ``status_only`` sets ``config.VALIDATION_STATUS_ONLY`` for the run and
    defaults to FALSE — an explicit test override, the only way the pre-gate
    publication behaviour is reachable. The tests below this line are about
    classification, deferral, dedup, and archiving, and each needs an item to
    reach the digest to prove its point; leaving the shipped default on would
    have silently converted every one of them into a test of the gate. The gate
    has its own tests, which pass ``status_only=True``.
    """
    import copy
    import shutil
    import src.classify as classify_mod
    import src.main as main_mod
    from src import config as config_mod

    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not (tmp_path / "templates").exists():
        shutil.copytree(os.path.join(repo, "templates"), tmp_path / "templates")
    monkeypatch.chdir(tmp_path)

    class FakeSource:
        name = "iisd_itn"
        priority = "primary"

        def fetch(self, since):
            # Fresh objects each run: the pipeline mutates item metadata.
            return [copy.deepcopy(it) for it in items]

    monkeypatch.setattr(main_mod, "all_sources", lambda cfg=None: [FakeSource()])
    monkeypatch.setattr(main_mod, "enrich", lambda it: it)     # offline
    monkeypatch.setattr(config_mod, "RESEARCH_BRIEF_ENABLED", False)
    monkeypatch.setattr(config_mod, "VALIDATION_STATUS_ONLY", status_only)
    monkeypatch.setenv("MODEL_PROVIDER", "claude")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setattr(classify_mod, "_call_anthropic", responder)
    # Pre-seed so this is not a bootstrap run. A bare string on purpose: it is
    # the legacy shape, so every run here also exercises the read-time migration.
    state.save_state({"sources": {"iisd_itn": {"_seed": "2026-01-01T00:00:00+00:00"}}},
                     "state/seen.json")
    return lambda: main_mod.main(["--since", "30d", "--no-email"])


# --- (1) a malformed classification survives to the next run -----------------
def test_malformed_classification_is_deferred_and_succeeds_on_the_retry(
        tmp_path, monkeypatch):
    reply = {"text": "I'm afraid I can't produce JSON for this one."}
    run = _sandbox(tmp_path, monkeypatch, [_cand("cand-1")],
                   lambda prompt: reply["text"])

    assert run() == 0
    st = state.load_state("state/seen.json")
    assert not state.is_seen(st, "iisd_itn", "cand-1"), \
        "an item we could not classify was retired as processed"
    dq = state.load_deferred("state/deferred.json")
    entry = dq["iisd_itn"]["cand-1"]
    assert entry["attempts"] == 1
    assert entry["last_outcome"] == "parse_failed"
    assert entry["url"] == "http://x/cand-1"
    assert "raw_text" not in entry, "the deferred queue must hold identity, not text"

    # Run 2: the provider answers properly. The item comes back (it was never
    # marked seen), classifies, and reaches the digest.
    reply["text"] = GOOD_JSON
    assert run() == 0
    st = state.load_state("state/seen.json")
    assert state.is_seen(st, "iisd_itn", "cand-1")
    assert state.seen_outcome(st, "iisd_itn", "cand-1") == "ok"
    assert state.load_deferred("state/deferred.json").get("iisd_itn", {}) == {}

    from pathlib import Path
    from src import render
    folder = Path(f"digests/{render.folder_name(datetime.datetime.now(UTC).strftime('%Y-%m-%d'))}")
    meta = json.loads((folder / "meta.json").read_text())
    assert meta["accepted"] == 1
    assert list((folder / "articles").glob("*.md"))


# --- (2) a provider outage retires nothing and says so -----------------------
def test_provider_outage_marks_zero_enriched_items_seen_and_reports_degradation(
        tmp_path, monkeypatch, capsys):
    def outage(prompt):
        raise RuntimeError("529 overloaded_error")

    items = [_cand(f"cand-{i}") for i in range(3)]
    run = _sandbox(tmp_path, monkeypatch, items, outage)
    assert run() == 0

    st = state.load_state("state/seen.json")
    assert state.seen_ids(st, "iisd_itn") == {"_seed"}, \
        "an outage marked items seen; the failure would be permanent"
    dq = state.load_deferred("state/deferred.json")
    assert len(dq["iisd_itn"]) == 3
    assert {e["last_outcome"] for e in dq["iisd_itn"].values()} == {"provider_error"}

    out = capsys.readouterr().out
    assert "DEGRADED" in out
    assert "provider_error=3" in out
    assert "deferred for retry (NOT marked seen): 3" in out
    # ...and the keyword scores behind the outage were NOT published as results.
    assert "classified:       0" in out


# --- (3) three failures end in a loud, ledgered abandonment ------------------
def test_three_failures_abandon_the_item_loudly_and_the_guard_enforces_it(
        tmp_path, monkeypatch, capsys):
    import importlib
    run = _sandbox(tmp_path, monkeypatch, [_cand("cand-1")],
                   lambda prompt: "still not JSON")

    for _ in range(2):
        assert run() == 0
        assert not state.is_seen(state.load_state("state/seen.json"),
                                 "iisd_itn", "cand-1")
    capsys.readouterr()

    assert run() == 0                      # the third failure
    out = capsys.readouterr().out
    assert "ABANDONED" in out and "3 attempts" in out

    st = state.load_state("state/seen.json")
    assert state.is_seen(st, "iisd_itn", "cand-1")
    assert state.seen_outcome(st, "iisd_itn", "cand-1") == "abandoned"
    assert state.load_deferred("state/deferred.json").get("iisd_itn", {}) == {}

    from pathlib import Path
    ledger = Path("analytics/abandoned_candidates.jsonl")
    lines = [ln for ln in ledger.read_text().splitlines() if ln.strip()]
    assert len(lines) == 1
    rec = json.loads(lines[0])
    assert (rec["source"], rec["source_id"], rec["attempts"]) == \
        ("iisd_itn", "cand-1", 3)
    assert rec["last_outcome"] == "parse_failed"

    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(repo, "scripts"))
    guard = importlib.import_module("check_seen_integrity")
    argv = ["check_seen_integrity", "--state", "state/seen.json",
            "--ledger", str(ledger)]
    assert guard.main(argv) == 0

    # The ledger line is the only public record of the abandonment. Remove it and
    # the state file alone claims something nothing corroborates.
    ledger.write_text("")
    assert guard.main(argv) == 1


# --- (4) legacy seen entries migrate without loss ----------------------------
def test_legacy_seen_entries_migrate_losslessly_at_read_time(tmp_path):
    p = tmp_path / "seen.json"
    legacy = {"sources": {"italaw": {"https://italaw.com/cases/1": "2026-01-01T00:00:00+00:00",
                                     "https://italaw.com/cases/2": "2026-02-02T00:00:00+00:00"}}}
    p.write_text(json.dumps(legacy, indent=2))

    st = state.load_state(str(p))
    assert state.seen_ids(st, "italaw") == set(legacy["sources"]["italaw"])
    assert all(state.is_seen(st, "italaw", k) for k in legacy["sources"]["italaw"])
    assert st["sources"]["italaw"]["https://italaw.com/cases/1"] == {
        "at": "2026-01-01T00:00:00+00:00", "outcome": "legacy"}
    assert state.seen_outcome(st, "italaw", "https://italaw.com/cases/2") == "legacy"
    # Reading does not rewrite the file.
    assert json.loads(p.read_text()) == legacy

    # New entries coexist with migrated ones through a save/load round trip.
    state.mark_seen(st, "italaw", "https://italaw.com/cases/3",
                    when=datetime.datetime(2026, 8, 1, 9, 0, tzinfo=UTC), outcome="ok")
    state.save_state(st, str(p))
    again = state.load_state(str(p))
    assert again["sources"]["italaw"]["https://italaw.com/cases/1"]["outcome"] == "legacy"
    assert again["sources"]["italaw"]["https://italaw.com/cases/1"]["at"] == \
        "2026-01-01T00:00:00+00:00"
    entry = again["sources"]["italaw"]["https://italaw.com/cases/3"]
    assert (entry["outcome"], entry["run"]) == ("ok", "2026-08-01")


def test_corrupt_seen_value_keeps_the_key_and_admits_it_cannot_describe_it(tmp_path):
    # Dedup must survive a value we cannot read: dropping the key would republish
    # the item, which is a worse failure than an unknown outcome.
    p = tmp_path / "seen.json"
    p.write_text(json.dumps({"sources": {"italaw": {"a": 12345}}}))
    st = state.load_state(str(p))
    assert state.is_seen(st, "italaw", "a")
    assert state.seen_outcome(st, "italaw", "a") == "legacy"


# --- (5) the failure states stay distinct ------------------------------------
def test_classification_failure_states_never_collapse(monkeypatch):
    import src.classify as classify_mod
    from src.classify import (TERMINAL_OUTCOMES, ClassifyOutcome, classify_item,
                              outcome_of)

    # Four states, four values, and only two of them mean "done with it".
    assert len({o.value for o in ClassifyOutcome}) == 4
    assert TERMINAL_OUTCOMES == {ClassifyOutcome.OK,
                                 ClassifyOutcome.KEYWORD_ONLY_BY_DESIGN}
    assert ClassifyOutcome.PARSE_FAILED not in TERMINAL_OUTCOMES
    assert ClassifyOutcome.PROVIDER_ERROR not in TERMINAL_OUTCOMES

    monkeypatch.setenv("MODEL_PROVIDER", "claude")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    it = _item("Patent denial of justice", ON_THEME, ON_THEME)

    def outage(prompt):
        raise RuntimeError("529 overloaded_error")

    # A provider error on an item we meant to model-classify: the keyword number
    # exists, and is not published.
    monkeypatch.setattr(classify_mod, "_call_anthropic", outage)
    err = classify_item(it, provider="claude", intended_model=True)
    assert outcome_of(err) is ClassifyOutcome.PROVIDER_ERROR
    assert err.relevance_score == 0
    assert err.metadata["keyword_score_advisory"] > 0

    # The same failure on an item we never intended to model-classify is the
    # result it was always going to get, and publishes.
    tail = classify_item(it, provider="claude", intended_model=False)
    assert outcome_of(tail) is ClassifyOutcome.KEYWORD_ONLY_BY_DESIGN
    assert tail.relevance_score == err.metadata["keyword_score_advisory"]

    # A parse failure is neither of those.
    monkeypatch.setattr(classify_mod, "_call_anthropic", lambda p: "not json at all")
    bad = classify_item(it, provider="claude", intended_model=True)
    assert outcome_of(bad) is ClassifyOutcome.PARSE_FAILED
    assert bad.relevance_score == 0
    assert bad.metadata["retried_strict"] is True
    assert bad.metadata["classify_attempts"] == 2

    # No key configured at all is a designed state, not a degradation: this is
    # how an offline --dry-run works, and it must keep publishing.
    monkeypatch.delenv("ANTHROPIC_API_KEY")
    offline = classify_item(it, provider="claude")
    assert outcome_of(offline) is ClassifyOutcome.KEYWORD_ONLY_BY_DESIGN
    assert offline.relevance_score > 0

    # And a clean answer is OK.
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setattr(classify_mod, "_call_anthropic", lambda p: GOOD_JSON)
    good = classify_item(it, provider="claude", intended_model=True)
    assert outcome_of(good) is ClassifyOutcome.OK
    assert good.relevance_score == 80


# --- (6) the keyword tail is still terminal ----------------------------------
def test_tail_keyword_items_are_still_marked_seen_during_an_outage(
        tmp_path, monkeypatch):
    # More candidates than ENRICH_TOP_N, so there is a genuine tail. The top set
    # is intended for the model and must survive the outage unretired; the tail
    # was always going to be keyword-scored and must not be held back by it.
    def outage(prompt):
        raise RuntimeError("529 overloaded_error")

    top = [_cand(f"on-{i}") for i in range(config.ENRICH_TOP_N)]
    tail = [_cand(f"off-{i}", title="Local weather", text=OFF_THEME) for i in range(2)]
    run = _sandbox(tmp_path, monkeypatch, top + tail, outage)
    assert run() == 0

    st = state.load_state("state/seen.json")
    seen = state.seen_ids(st, "iisd_itn")
    assert {"off-0", "off-1"} <= seen, "the keyword tail was not finished with"
    assert all(state.seen_outcome(st, "iisd_itn", s) == "keyword_only_by_design"
               for s in ("off-0", "off-1"))
    assert not any(f"on-{i}" in seen for i in range(config.ENRICH_TOP_N))
    assert len(state.load_deferred("state/deferred.json")["iisd_itn"]) == \
        config.ENRICH_TOP_N


# --- telemetry is emitted by a real run --------------------------------------
def test_a_run_emits_exactly_one_telemetry_record_per_candidate(
        tmp_path, monkeypatch):
    import importlib
    from src import telemetry
    items = [_cand(f"cand-{i}") for i in range(3)]
    run = _sandbox(tmp_path, monkeypatch, items, lambda prompt: GOOD_JSON)
    assert run() == 0

    recs = telemetry.load_records("analytics/candidate_telemetry.jsonl")
    assert len(recs) == 3
    assert len({r["candidate_id"] for r in recs}) == 3
    assert len({r["run_id"] for r in recs}) == 1
    assert all(r["classification"]["outcome"] == "ok" for r in recs)
    assert all(r["dedup"]["marked_seen"] for r in recs)
    assert all(r["surfacing"]["surfaced"] for r in recs)
    assert all(r["classification"]["prompt_version"] for r in recs)

    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(repo, "scripts"))
    guard = importlib.import_module("check_telemetry_privacy")
    assert guard.main(["check_telemetry_privacy", "--path",
                       "analytics/candidate_telemetry.jsonl"]) == 0


def test_telemetry_records_the_score_an_outage_cost_without_publishing_it(
        tmp_path, monkeypatch):
    from src import telemetry

    def outage(prompt):
        raise RuntimeError("529 overloaded_error")

    run = _sandbox(tmp_path, monkeypatch, [_cand("cand-1")], outage)
    assert run() == 0
    rec = telemetry.load_records("analytics/candidate_telemetry.jsonl")[0]
    assert rec["classification"]["outcome"] == "provider_error"
    assert rec["classification"]["model_score_advisory"] > 0
    assert rec["dedup"] == {"seen_before": False, "marked_seen": False,
                            "deferred": True, "abandoned": False}
    assert rec["surfacing"]["surfaced"] is False
    assert rec["surfacing"]["reason"] == "not_classified"


# --- the seen-state is durable the moment the digest exists ------------------
def test_a_failing_research_brief_cannot_unwrite_the_seen_state(
        tmp_path, monkeypatch):
    """Regression: Telefónica v. Colombia went out on 2026-06-09 (score 32, one
    ring) and again on 2026-06-10 (score 28, no ring) — same URL, same source,
    consecutive runs. State was persisted at the very end of main(), after the
    research brief, and the brief's network call had no exception handler despite
    a comment promising one. A raise there threw away the run's whole seen-state
    while leaving the digest it had already written on disk."""
    import src.main as main_mod
    from src import config as config_mod, research_brief as rb_mod

    run = _sandbox(tmp_path, monkeypatch, [_cand("cand-1")], lambda p: GOOD_JSON)
    monkeypatch.setattr(config_mod, "RESEARCH_BRIEF_ENABLED", True)
    monkeypatch.setattr(main_mod.config, "RESEARCH_BRIEF_ENABLED", True)

    def exploding_brief(*a, **k):
        raise RuntimeError("web search tool unavailable")

    monkeypatch.setattr(rb_mod, "generate_brief", exploding_brief)
    monkeypatch.setattr(main_mod.research_brief, "generate_brief", exploding_brief)

    assert run() == 0, "a failing brief took the whole run down with it"
    st = state.load_state("state/seen.json")
    assert state.is_seen(st, "iisd_itn", "cand-1"), \
        "the digest was written but the run forgot it — the item republishes tomorrow"


def test_a_seen_item_is_not_reclassified_or_republished_on_the_next_run(
        tmp_path, monkeypatch):
    calls = {"n": 0}

    def counting(prompt):
        calls["n"] += 1
        return GOOD_JSON

    run = _sandbox(tmp_path, monkeypatch, [_cand("cand-1")], counting)
    assert run() == 0
    assert calls["n"] == 1

    # Same item, same source, next run: deduped before it reaches the classifier.
    assert run() == 0
    assert calls["n"] == 1, "a seen item was classified a second time"


# =============================================================================
# Publication safety (Workstream H)
#
# The fill was the mechanism by which almost everything ever sent to the
# professor was published: no item has yet scored a true match, so a digest with
# six items in it was six items the classifier declined to call matches. The fill
# is suspended while the classifier is validated. What clears the threshold still
# publishes; what does not is reported as what it is.
# =============================================================================
def test_fill_floor_suspended_publishes_nothing_below_the_threshold():
    from src.main import select_surfaced
    # A thin week: one item just under the threshold, several above the floor.
    items = [_classified(s) for s in (39, 30, 27, 25, 24, 10)]
    out = select_surfaced(items, threshold=40, min_items=6, floor=25,
                          fill_floor_suspended=True)
    assert out == [], "a sub-threshold item was published to fill the digest"


def test_an_item_at_the_threshold_still_clears_the_fill_rule_while_suspended():
    from src.main import would_surface
    items = [_classified(s) for s in (80, 40, 39, 30)]
    out = would_surface(items, threshold=40, min_items=6, floor=25,
                        fill_floor_suspended=True)
    assert [c.relevance_score for c in out] == [80, 40]
    # Exactly at the threshold counts as clearing it; 39 does not.
    assert 39 not in {c.relevance_score for c in out}
    # ...and clearing the fill rule is no longer the same as publishing: the
    # validation gate holds both of these. That is Workstream 1's whole point.
    from src.main import select_surfaced
    assert select_surfaced(items, 40, 6, 25, status_only=True) == []


def test_suspension_is_the_default_and_the_flag_restores_the_old_behaviour():
    from src.main import would_surface
    items = [_classified(s) for s in (80, 45, 30, 24, 10, 0)]

    # Default: reads config.FILL_FLOOR_SUSPENDED, which ships suspended.
    assert config.FILL_FLOOR_SUSPENDED is True
    assert {c.relevance_score for c in
            would_surface(items, 40, 6, 25)} == {80, 45}

    # Flag off: the pre-suspension behaviour, fill and all.
    restored = would_surface(items, 40, 6, 25, fill_floor_suspended=False)
    scores = {c.relevance_score for c in restored}
    assert scores == {80, 45, 30}, "turning the flag off did not restore the fill"
    assert 24 not in scores          # the floor still binds under either setting


def test_zero_surfaced_cycle_emits_the_status_only_body_verbatim():
    from src import render
    now = datetime.datetime.now(UTC)
    stats = {"total_candidates": 83, "classified": 83, "above_threshold": 0,
             "per_source": {"iisd_itn": 83}, "dropped_sources": [], "threshold": 40,
             "provider": "claude"}
    html = render.render_digest([], now, now, stats)

    expected = (
        "The watcher screened 83 candidates this cycle and assigned none a score "
        "at or above 40. Because the classifier is undergoing validation, this "
        "reports the instrument's output and does not establish that no relevant "
        "development exists. Retrieval, scoring, archiving, and telemetry "
        "continue; shadow runs preserve the time series."
    )
    assert expected in html, "the status-only body is not emitted verbatim"
    assert render.status_only_body(83, 40) == expected
    # The claim it replaced must be gone: it asserted a fact about the world.
    assert "No thematically relevant developments" not in html


def test_a_status_only_cycle_still_archives_and_still_says_what_it_screened(
        tmp_path, monkeypatch):
    # check_claims.py counts archived runs off digests/[0-9]*.html. Suspending
    # the fill changes WHAT is surfaced, never WHETHER the run is archived.
    import glob
    from pathlib import Path
    from src import render

    below = json.dumps({"relevance_score": 30, "matched_rings": [],
                        "thematic_tags": [], "digest_summary": "A. B."})
    run = _sandbox(tmp_path, monkeypatch, [_cand("cand-1")], lambda p: below)
    assert run() == 0

    date_str = datetime.datetime.now(UTC).strftime("%Y-%m-%d")
    assert glob.glob(f"digests/{date_str}.html"), "the run was not archived"
    folder = Path(f"digests/{render.folder_name(date_str)}")
    meta = json.loads((folder / "meta.json").read_text())
    assert (meta["screened"], meta["matches"], meta["accepted"]) == (1, 0, 0)

    html = Path(f"digests/{date_str}.html").read_text()
    assert render.status_only_body(1, 40) in html
    # The item was still classified, scored, and marked seen — only not published.
    st = state.load_state("state/seen.json")
    assert state.seen_outcome(st, "iisd_itn", "cand-1") == "ok"
    from src import telemetry
    rec = telemetry.load_records("analytics/candidate_telemetry.jsonl")[0]
    assert rec["surfacing"]["surfaced"] is False
    # It cleared the floor and would have filled the digest before the
    # suspension; the telemetry says so, so the cost of suspending is countable.
    assert rec["surfacing"]["reason"] == "fill_suspended"


# =============================================================================
# Publication safety, second gate: VALIDATION_STATUS_ONLY
#
# Suspending the fill was defended on the ground that no item has ever scored a
# true match, so the fill was the only route to the professor. That is true of
# the record and false of the code. `prompts/classifier.txt` Example 4 — a
# construction denial-of-justice case, judicial ring only, explicitly "not
# intellectual property" and raising "no abuse-of-right or treaty-shopping
# issue" — is taught to the model as a 55. `select_surfaced` published on the
# score alone. So the one configuration the fill suspension could not protect
# against was the one that matters: an off-theme item scoring over 40.
#
# These six tests are the gate. The first two are the hole itself.
# =============================================================================
EXAMPLE_4_TEXT = (
    "A construction investor filed an ICSID claim contending that a domestic "
    "Supreme Court judgment setting aside a commercial arbitration award was "
    "manifestly unjust and shocked a sense of judicial propriety, amounting to a "
    "denial of justice and a breach of the minimum standard of treatment. The "
    "dispute concerns infrastructure concessions, not intellectual property, and "
    "raises no abuse-of-right or treaty-shopping issue."
)

# Verbatim from prompts/classifier.txt Example 4. Not paraphrased: the point of
# the test is that this exact taught answer is publishable, so the taught answer
# is what the fake provider returns.
EXAMPLE_4_JSON = json.dumps({
    "relevance_score": 55,
    "matched_rings": ["judicial_or_regulatory_measure"],
    "thematic_tags": ["denial_of_justice", "judicial_measure"],
    "digest_summary": "A construction investor claims denial of justice. It scores MEDIUM.",
})

THREE_RING_JSON = json.dumps({
    "relevance_score": 95,
    "matched_rings": ["ip_as_investment", "judicial_or_regulatory_measure",
                      "jurisdictional_admissibility"],
    "thematic_tags": ["trademark", "denial_of_justice", "standing"],
    "digest_summary": "All three rings. It scores HIGH.",
})


def _gated_run(tmp_path, monkeypatch, sid, payload, text=EXAMPLE_4_TEXT):
    """One full gated cycle over a single item; returns its telemetry record."""
    from src import telemetry
    run = _sandbox(tmp_path, monkeypatch, [_cand(sid, text=text)],
                   lambda p: payload, status_only=True)
    assert run() == 0
    recs = telemetry.load_records("analytics/candidate_telemetry.jsonl")
    assert len(recs) == 1
    return recs[0]


def _digest_folder():
    from pathlib import Path
    from src import render
    return Path("digests/"
                + render.folder_name(datetime.datetime.now(UTC).strftime("%Y-%m-%d")))


# --- (1) the taught 55 does not publish --------------------------------------
def test_the_example_4_judicial_only_item_publishes_nothing_while_gated(
        tmp_path, monkeypatch):
    rec = _gated_run(tmp_path, monkeypatch, "cand-doj", EXAMPLE_4_JSON)

    folder = _digest_folder()
    meta = json.loads((folder / "meta.json").read_text())
    assert meta["accepted"] == 0, \
        "an off-theme item scoring 55 reached the digest through the score alone"
    assert list((folder / "articles").glob("*.md")) == []
    # It DID score 55 and it IS counted as at/above threshold — the gate holds
    # the publication, it does not rewrite the measurement.
    assert meta["matches"] == 1
    assert rec["surfacing"]["surfaced"] is False
    assert rec["surfacing"]["reason"] == "held_validation_status_only"


# --- (2) a real three-ring match is held too, and countably -------------------
def test_a_score_95_three_ring_item_is_also_held_and_recorded(
        tmp_path, monkeypatch):
    # The gate is not a filter on items we already distrust. If it only held the
    # ones we doubted it would be a scoring rule wearing a gate's name.
    rec = _gated_run(tmp_path, monkeypatch, "cand-three", THREE_RING_JSON,
                     text=ON_THEME)

    folder = _digest_folder()
    assert json.loads((folder / "meta.json").read_text())["accepted"] == 0
    assert rec["surfacing"]["reason"] == "held_validation_status_only"
    assert rec["classification"]["outcome"] == "ok"
    # Held is not lost: it was classified, marked seen, and archived as today.
    assert rec["dedup"]["marked_seen"] is True
    st = state.load_state("state/seen.json")
    assert state.seen_outcome(st, "iisd_itn", "cand-three") == "ok"
    date_str = datetime.datetime.now(UTC).strftime("%Y-%m-%d")
    assert os.path.exists(f"digests/{date_str}.html"), \
        "the run stopped archiving — check_claims counts these files"

    # And the operator is told, in the one message that goes out, that something
    # is being held. A held match that produced a silent cycle would be the same
    # failure as publishing it, in the other direction.
    from src import render
    html = open(f"digests/{date_str}.html", encoding="utf-8").read()
    assert render.status_only_body(1, 40, held=1) in html
    assert "1 item was flagged internally at or above the match threshold" in html
    # The zero-held sentence would have been a false statement here.
    assert "assigned none a score at or above" not in html


def test_the_status_body_keeps_its_approved_wording_when_nothing_is_held():
    from src import render
    # Byte-identical to the approved copy: the held clause is additive, and every
    # cycle the watch has actually run is a zero-held cycle.
    expected = (
        "The watcher screened 83 candidates this cycle and assigned none a score "
        "at or above 40. Because the classifier is undergoing validation, this "
        "reports the instrument's output and does not establish that no relevant "
        "development exists. Retrieval, scoring, archiving, and telemetry "
        "continue; shadow runs preserve the time series."
    )
    assert render.status_only_body(83, 40) == expected
    assert render.status_only_body(83, 40, held=0) == expected

    # Held: the screening clause no longer asserts what a held item contradicts.
    held_body = render.status_only_body(83, 40, held=2)
    assert held_body.startswith("The watcher screened 83 candidates this cycle. "
                                "2 items were flagged internally at or above the "
                                "match threshold and are held for operator review "
                                "pending validation.")
    assert "assigned none" not in held_body
    assert "no relevant development exists" in held_body


# --- (3) exactly one communication per cycle ---------------------------------
def test_a_gated_cycle_sends_exactly_one_status_message(tmp_path, monkeypatch):
    import src.main as main_mod
    from src import config as config_mod, research_brief as rb_mod

    _sandbox(tmp_path, monkeypatch, [_cand("cand-1"), _cand("cand-2")],
             lambda p: THREE_RING_JSON, status_only=True)
    # The brief is a SECOND email, so leaving it disabled would prove nothing
    # about "exactly one". Enable it and let the gate be the thing that stops it.
    monkeypatch.setattr(config_mod, "RESEARCH_BRIEF_ENABLED", True)
    monkeypatch.setattr(rb_mod, "generate_brief",
                        lambda *a, **k: pytest.fail("the brief ran while gated"))
    monkeypatch.setattr(main_mod.research_brief, "generate_brief",
                        lambda *a, **k: pytest.fail("the brief ran while gated"))

    sent = []
    monkeypatch.setattr(main_mod, "send_digest",
                        lambda html, subject, cfg, **k: sent.append(subject) or True)
    assert main_mod.main(["--since", "30d"]) == 0

    assert len(sent) == 1, f"a gated cycle sent {len(sent)} messages, not one"
    assert "status-only cycle" in sent[0]
    assert "2 held for operator review" in sent[0]
    # The subject must not deny what the body reports.
    assert "none at/above" not in sent[0]


# --- (4) the two flags are independent ---------------------------------------
def test_the_fill_flag_cannot_disable_the_status_only_gate():
    from src.main import select_surfaced, would_surface
    items = [_classified(s) for s in (95, 55, 30, 24)]

    # All four combinations. The gate wins wherever it is on, and the fill flag
    # only ever chooses between two shapes of "nothing".
    assert select_surfaced(items, 40, 6, 25,
                           fill_floor_suspended=True, status_only=True) == []
    assert select_surfaced(items, 40, 6, 25,
                           fill_floor_suspended=False, status_only=True) == [], \
        "restoring the fill reopened item-level publication"

    gate_off_fill_on = select_surfaced(items, 40, 6, 25,
                                       fill_floor_suspended=True, status_only=False)
    assert {c.relevance_score for c in gate_off_fill_on} == {95, 55}

    gate_off_fill_off = select_surfaced(items, 40, 6, 25,
                                        fill_floor_suspended=False, status_only=False)
    assert {c.relevance_score for c in gate_off_fill_off} == {95, 55, 30}

    # Both flags ship ON, and each is read from its own name.
    assert config.VALIDATION_STATUS_ONLY is True
    assert config.FILL_FLOOR_SUSPENDED is True
    assert select_surfaced(items, 40, 6, 25) == []
    # The fill rule underneath is untouched and still computable — that is what
    # lets the gate report what it held rather than only that it held.
    assert {c.relevance_score for c in would_surface(items, 40, 6, 25)} == {95, 55}


# --- (5) the historical behaviour needs both overrides, explicitly ------------
def test_the_pre_gate_behaviour_is_reachable_only_by_setting_both_flags_off():
    from src.main import select_surfaced
    items = [_classified(s) for s in (80, 45, 30, 24, 10, 0)]

    # The digest as it was actually published for eleven runs: matches, then the
    # fill down to the floor. Nothing short of naming both flags gets here.
    old = select_surfaced(items, 40, 6, 25,
                          fill_floor_suspended=False, status_only=False)
    assert {c.relevance_score for c in old} == {80, 45, 30}
    assert 24 not in {c.relevance_score for c in old}   # the floor still binds

    for kwargs in ({}, {"fill_floor_suspended": False}, {"status_only": True},
                   {"fill_floor_suspended": False, "status_only": True}):
        assert select_surfaced(items, 40, 6, 25, **kwargs) == [], \
            f"the pre-gate behaviour leaked through {kwargs or 'the defaults'}"


# --- (6) no research brief while gated ----------------------------------------
def test_no_research_brief_is_generated_while_the_gate_is_on(tmp_path, monkeypatch):
    import src.main as main_mod
    from src import config as config_mod, research_brief as rb_mod

    calls = {"n": 0}

    def counting_brief(*a, **k):
        calls["n"] += 1
        return {"headline": "h", "open_threads": [], "_memo": "m"}

    run = _sandbox(tmp_path, monkeypatch, [_cand("cand-1")],
                   lambda p: THREE_RING_JSON, status_only=True)
    monkeypatch.setattr(config_mod, "RESEARCH_BRIEF_ENABLED", True)
    monkeypatch.setattr(rb_mod, "generate_brief", counting_brief)
    monkeypatch.setattr(main_mod.research_brief, "generate_brief", counting_brief)

    assert run() == 0
    assert calls["n"] == 0, "the brief ran on a cycle with no surfaced items"
    assert not os.path.isdir("briefs"), "a gated cycle wrote a brief to disk"
    # Skipping it changes nothing about the digest or the state — the same path
    # --dry-run and an empty run already take.
    st = state.load_state("state/seen.json")
    assert state.seen_outcome(st, "iisd_itn", "cand-1") == "ok"
    assert (_digest_folder() / "meta.json").exists()


# =============================================================================
# STATE_MODEL_V2 shadow derivation, through a real run
#
# The contract itself is tested exhaustively in tests/test_rings.py. What is
# tested here is the WIRING — that a real cycle derives a verdict, writes it
# beside the score, and changes nothing else. A shadow derivation that quietly
# stopped deriving would look exactly like one that had nothing to say.
# =============================================================================
def test_a_run_writes_the_v2_verdict_to_telemetry_and_changes_nothing_else(
        tmp_path, monkeypatch):
    import importlib
    from src import config as config_mod, rings, telemetry

    assert config_mod.STATE_MODEL_V2 == "shadow", \
        "the shipped default is shadow: derived every run, authoritative over nothing"

    run = _sandbox(tmp_path, monkeypatch, [_cand("cand-1")],
                   lambda p: EXAMPLE_4_JSON, status_only=True)
    assert run() == 0

    rec = telemetry.load_records("analytics/candidate_telemetry.jsonl")[0]
    v2 = rec["verdict_v2"]
    assert v2["derived"] is True and v2["mode"] == "shadow"
    assert v2["lane"] in {lane.value for lane in rings.Lane}
    assert v2["lane_reason"] in rings.ALL_REASON_CODES
    assert set(v2["rings"]) == set(rings.RINGS)
    # The legacy score is carried beside the lane, explicitly non-authoritative.
    assert v2["model_score_advisory"] == 55

    # It decided nothing: the surfacing reason is still the gate's, and the score
    # the run recorded is still the classifier's.
    assert rec["surfacing"]["reason"] == "held_validation_status_only"
    assert rec["classification"]["outcome"] == "ok"

    # And it is telemetry-safe. The guard, not an inspection of the fields.
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(repo, "scripts"))
    guard = importlib.import_module("check_telemetry_privacy")
    assert guard.main(["check_telemetry_privacy", "--path",
                       "analytics/candidate_telemetry.jsonl"]) == 0


def test_turning_state_model_v2_off_leaves_the_record_honestly_empty(
        tmp_path, monkeypatch):
    from src import config as config_mod, telemetry

    run = _sandbox(tmp_path, monkeypatch, [_cand("cand-1")],
                   lambda p: GOOD_JSON, status_only=True)
    monkeypatch.setattr(config_mod, "STATE_MODEL_V2", "off")
    assert run() == 0

    v2 = telemetry.load_records("analytics/candidate_telemetry.jsonl")[0]["verdict_v2"]
    # Present and saying "we did not do that" — not absent. A query must not have
    # to tell a missing field from a false one.
    assert v2["derived"] is False
    assert v2["lane"] == "" and v2["rings"] == {}


def test_state_model_v2_refuses_to_be_switched_on(monkeypatch):
    from src import config as config_mod

    # "on" is publication-lane authority. It is not validated and nothing is
    # wired to consult it, so the config coerces it to shadow rather than
    # accepting a value that would change what a professor receives.
    assert config_mod.STATE_MODEL_V2_PUBLICATION_READY is False
    assert config_mod._state_model_v2_mode("on") == "shadow"
    assert config_mod._state_model_v2_mode("ON") == "shadow"
    # The other two are honoured, and anything unrecognised fails closed to shadow.
    assert config_mod._state_model_v2_mode("off") == "off"
    assert config_mod._state_model_v2_mode("shadow") == "shadow"
    assert config_mod._state_model_v2_mode("yes please") == "shadow"
    assert config_mod._state_model_v2_mode("") == "shadow"


def test_the_v2_prompt_asks_for_evidence_and_never_for_a_score():
    # prompts/classifier_v2.txt is the other half of the contract. It is not
    # wired into production and must not acquire a score field by drift.
    text = open("prompts/classifier_v2.txt", encoding="utf-8").read()
    assert '"relevance_score"' not in text, \
        "V2 removes scoring; a score field would restore the thing it fixes"
    # The field name survives only in two places, both of them prohibitions: the
    # design note explaining what was removed, and the output rules telling the
    # model not to invent one. It appears in no example answer.
    assert "There is NO relevance_score" in text
    for block in text.split("OUTPUT:\n")[1:]:
        assert "relevance_score" not in block.split("\n", 1)[0]
    for ring in ("ip_as_investment", "judicial_or_regulatory_measure",
                 "jurisdictional_admissibility"):
        assert ring in text
    assert "evidence_span" in text and "isds_nexus" in text
    for word in ("absent", "weak", "present", "strong"):
        assert f'"{word}' in text or f"{word}|" in text or f"|{word}" in text

    # The resolved contradiction is stated in the header, not left implied.
    assert "NEVER a match and is" in text
    assert "never automatically MEDIUM" in text

    # The five-fold {{TEXT}} inlining of classifier.txt is not repeated here.
    assert text.count("{{TEXT}}") == 1

    # Production still reads V1 until the flag says otherwise.
    from src import classify
    assert classify._PROMPT_PATH.name == "classifier.txt"


# =============================================================================
# Workstream F and the V2 shadow, wired into a real run
# =============================================================================
# Markers unique to one prompt each. "OUTPUT CONTRACT" is NOT one of them:
# prompts/classifier.txt carries that heading too, and using it silently routed
# every V1 call into the V2 branch the first time these tests were written.
V2_MARKER = '"nexus_evidence"'
TRIAGE_MARKER = "Judge the PARAPHRASE, not the vocabulary."


def _is_v2(prompt):
    return V2_MARKER in prompt


def _is_triage(prompt):
    return TRIAGE_MARKER in prompt


def _three_prompt_responder(v2_payload=None, triage_payload=None,
                            log=None):
    """One provider stub for all three prompts, dispatching on their contract.

    The pipeline now sends three different prompts through the same transport.
    Routing on their content is not a convenience — it is the assertion that the
    three ARE distinguishable, and the call log proves how many of each a run
    actually made.
    """
    def responder(prompt):
        if log is not None:
            log.append(prompt)
        if _is_v2(prompt):
            return v2_payload or ""
        if _is_triage(prompt):
            return triage_payload or ""
        return GOOD_JSON
    return responder


def test_the_three_prompts_are_distinguishable_from_one_another():
    """The premise every test below rests on, checked rather than assumed."""
    from src import classify, classify_v2, triage as triage_mod

    v1 = classify._load_prompt_template()
    v2 = classify_v2.load_v2_prompt()
    tri = triage_mod.load_triage_prompt()
    assert _is_v2(v2) and not _is_v2(v1) and not _is_v2(tri)
    assert _is_triage(tri) and not _is_triage(v1) and not _is_triage(v2)


V2_GOOD = json.dumps({
    "rings": {
        "ip_as_investment": {
            "strength": "present",
            "evidence_span": "patent invalidated by the domestic courts"},
        "judicial_or_regulatory_measure": {
            "strength": "present",
            "evidence_span": "domestic courts applying the promise utility "
                             "doctrine"},
        "jurisdictional_admissibility": {"strength": "absent",
                                         "evidence_span": ""},
    },
    "isds_nexus": "established",
    "nexus_evidence": "ICSID Case No. ARB/16/34",
    "thematic_tags": ["patent"],
    "digest_summary": "A patent was invalidated. Two rings are present.",
})

TRIAGE_GOOD = json.dumps({"rings": {
    "ip_as_investment": "present",
    "judicial_or_regulatory_measure": "weak",
    "jurisdictional_admissibility": "absent"}})


def test_a_default_run_makes_no_triage_and_no_v2_call_and_says_lexical_only(
        tmp_path, monkeypatch):
    """The shipped configuration: nothing extra is spent and nothing is claimed."""
    from src import config as config_mod, telemetry

    log = []
    run = _sandbox(tmp_path, monkeypatch, [_cand("cand-1"), _cand("cand-2")],
                   _three_prompt_responder(log=log), status_only=True)
    assert config_mod.TRIAGE_ENABLED is False
    assert config_mod.V2_SHADOW_CALLS_MODE == config_mod.V2_SHADOW_CALLS_OFF
    assert run() == 0

    # Two candidates, two classification calls. Nothing else was bought.
    assert len(log) == 2
    recs = telemetry.load_records("analytics/candidate_telemetry.jsonl")
    assert len(recs) == 2
    for rec in recs:
        assert rec["triage"]["ran"] is False
        assert rec["triage"]["basis"] == "not_run"
        assert rec["v2_call"]["called"] is False
        v2 = rec["verdict_v2"]
        assert v2["derived"] is True
        assert v2["v2_basis"] == "lexical_only", \
            "a lexical derivation was reported as something else"
        assert "semantic:" not in json.dumps(v2)


def test_the_v2_sample_is_bounded_and_only_the_sampled_item_names_a_model(
        tmp_path, monkeypatch):
    from src import config as config_mod, telemetry

    log = []
    items = [_cand(f"cand-{i}") for i in range(4)]
    run = _sandbox(tmp_path, monkeypatch, items,
                   _three_prompt_responder(v2_payload=V2_GOOD, log=log),
                   status_only=True)
    monkeypatch.setattr(config_mod, "V2_SHADOW_CALLS_MODE", "sample")
    monkeypatch.setattr(config_mod, "V2_SHADOW_SAMPLE_N", 1)
    monkeypatch.setattr(config_mod, "V2_SHADOW_CALLS_SPEC", "sample:1")
    monkeypatch.setenv("ANTHROPIC_MODEL", "test-model-id")
    assert run() == 0

    v2_prompts = [p for p in log if _is_v2(p)]
    assert len(v2_prompts) == 1, "the sample bound was not respected"

    recs = telemetry.load_records("analytics/candidate_telemetry.jsonl")
    called = [r for r in recs if r["v2_call"]["called"]]
    assert len(called) == 1
    assert called[0]["verdict_v2"]["v2_basis"] == "semantic:test-model-id"
    assert called[0]["verdict_v2"]["claims_source"] == "v2_prompt"
    # ...and every other record is honestly lexical.
    for rec in recs:
        if rec["v2_call"]["called"]:
            continue
        assert rec["verdict_v2"]["v2_basis"] == "lexical_only"
        assert rec["verdict_v2"]["claims_source"] != "v2_prompt"


def test_a_v2_call_that_fails_never_lands_under_the_models_identity(
        tmp_path, monkeypatch):
    """The named defect, at the level of a real run."""
    from src import config as config_mod, telemetry

    def responder(prompt):
        if _is_v2(prompt):
            raise RuntimeError("the V2 provider is down")
        return GOOD_JSON

    run = _sandbox(tmp_path, monkeypatch, [_cand("cand-1")], responder,
                   status_only=True)
    monkeypatch.setattr(config_mod, "V2_SHADOW_CALLS_MODE", "sample")
    monkeypatch.setattr(config_mod, "V2_SHADOW_SAMPLE_N", 3)
    monkeypatch.setattr(config_mod, "V2_SHADOW_CALLS_SPEC", "sample:3")
    monkeypatch.setenv("ANTHROPIC_MODEL", "test-model-id")
    assert run() == 0, "a V2 provider failure must not fail the run"

    rec = telemetry.load_records("analytics/candidate_telemetry.jsonl")[0]
    assert rec["v2_call"]["called"] is True
    assert rec["v2_call"]["basis"] == "semantic_unavailable_provider_error"
    # The model is named as an operational fact and is NOT the basis.
    assert rec["v2_call"]["model"] == "test-model-id"
    assert rec["verdict_v2"]["v2_basis"] == "semantic_unavailable_provider_error"
    assert rec["verdict_v2"]["claims_source"] != "v2_prompt"
    # The legacy classification is untouched: V2 replaces nothing.
    assert rec["classification"]["outcome"] == "ok"


def test_a_triage_pass_runs_over_every_candidate_and_is_recorded(
        tmp_path, monkeypatch):
    from src import config as config_mod, rings as rings_mod, telemetry

    log = []
    items = [_cand(f"cand-{i}") for i in range(3)]
    run = _sandbox(tmp_path, monkeypatch, items,
                   _three_prompt_responder(triage_payload=TRIAGE_GOOD, log=log),
                   status_only=True)
    monkeypatch.setattr(config_mod, "TRIAGE_ENABLED", True)
    monkeypatch.setenv("ANTHROPIC_MODEL", "test-model-id")
    assert run() == 0

    triage_prompts = [p for p in log if _is_triage(p)]
    assert len(triage_prompts) == 3, "triage must run over every candidate"
    # No body is ever sent to triage.
    assert all("{{TEXT}}" not in p for p in triage_prompts)

    for rec in telemetry.load_records("analytics/candidate_telemetry.jsonl"):
        t = rec["triage"]
        assert t["ran"] is True
        assert t["basis"] == "semantic:test-model-id"
        assert t["semantic_rank"] > 0
        assert set(t["strengths"]) == set(rings_mod.RINGS)


def test_a_triage_outage_is_recorded_and_the_run_still_completes(
        tmp_path, monkeypatch):
    from src import config as config_mod, telemetry

    def responder(prompt):
        if _is_triage(prompt):
            raise RuntimeError("triage provider is down")
        return GOOD_JSON

    run = _sandbox(tmp_path, monkeypatch, [_cand("cand-1"), _cand("cand-2")],
                   responder, status_only=True)
    monkeypatch.setattr(config_mod, "TRIAGE_ENABLED", True)
    assert run() == 0, "a triage outage must not fail the run"

    for rec in telemetry.load_records("analytics/candidate_telemetry.jsonl"):
        t = rec["triage"]
        assert t["ran"] is False
        assert t["basis"] == "skipped_provider_error"
        assert t["semantic_rank"] == 0
        assert t["strengths"] == {}
        # The classification still happened; only the ranking hint was lost.
        assert rec["classification"]["outcome"] == "ok"


def test_an_abandoned_item_is_recorded_as_abandoned_not_as_still_retrying(
        tmp_path, monkeypatch):
    """R2.1's retry_abandoned, end to end, including the lane it must not reach."""
    from src import state as state_mod, telemetry

    run = _sandbox(tmp_path, monkeypatch, [_cand("cand-1")],
                   lambda p: "never valid json", status_only=True)
    for _ in range(state_mod.MAX_CLASSIFY_ATTEMPTS):
        assert run() == 0

    recs = telemetry.load_records("analytics/candidate_telemetry.jsonl")
    final = recs[-1]
    assert final["dedup"]["abandoned"] is True
    v2 = final["verdict_v2"]
    assert v2["classification_state"] == "retry_abandoned"
    assert v2["lane_reason"] == "classification_abandoned"
    assert v2["lane"] == "RETRY"
    # The operational outcome it was abandoned FOR is still on the record.
    assert v2["classification_outcome"] == "parse_failed"
    assert final["classification"]["outcome"] == "parse_failed"


def test_the_new_telemetry_sections_pass_the_privacy_guard(tmp_path, monkeypatch):
    """Spans, strengths and hashes — and still no candidate text anywhere."""
    import importlib

    from src import config as config_mod

    run = _sandbox(tmp_path, monkeypatch, [_cand("cand-1")],
                   _three_prompt_responder(v2_payload=V2_GOOD,
                                           triage_payload=TRIAGE_GOOD),
                   status_only=True)
    monkeypatch.setattr(config_mod, "TRIAGE_ENABLED", True)
    monkeypatch.setattr(config_mod, "V2_SHADOW_CALLS_MODE", "sample")
    monkeypatch.setattr(config_mod, "V2_SHADOW_SAMPLE_N", 3)
    monkeypatch.setattr(config_mod, "V2_SHADOW_CALLS_SPEC", "sample:3")
    assert run() == 0

    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(repo, "scripts"))
    guard = importlib.import_module("check_telemetry_privacy")
    assert guard.main(["check_telemetry_privacy", "--path",
                       "analytics/candidate_telemetry.jsonl"]) == 0

    blob = open("analytics/candidate_telemetry.jsonl", encoding="utf-8").read()
    assert "patent invalidated by the domestic courts" not in blob, \
        "a V2 evidence span reached telemetry as text"
    assert ON_THEME[:60] not in blob


def test_recovery_guard_heals_a_not_read_source(tmp_path, monkeypatch):
    """A documented-active source whose origin refused us (NOT-READ, 0 items)
    and which the recovery registry knows is read from the Internet Archive,
    inside the run — so its status becomes RECOVERED and no SOURCE ACCESS
    FAILURE line is produced. This is the autonomous guard end to end."""
    import glob
    import json
    import shutil
    import src.main as main_mod
    import src.state as state
    from src.sources.base import CandidateItem
    now = datetime.datetime.now(UTC)

    class WalledItalaw:
        name = "italaw"
        priority = "primary"
        def fetch(self, since):
            return []                      # origin 403 -> honest dark

    # The fetch loop reads base.get_fetch_log() to distinguish a refusal from a
    # quiet week; force a refusal so status becomes NOT-READ.
    monkeypatch.setattr(main_mod.all_sources.__self__ if False else main_mod,
                        "all_sources", lambda cfg=None: [WalledItalaw()])
    monkeypatch.setattr(main_mod.base, "get_fetch_log",
                        lambda: [{"url": "https://www.italaw.com/",
                                  "outcome": "refused", "detail": "403"}])
    monkeypatch.setattr(main_mod.base, "reset_fetch_log", lambda: None)
    # The Archive returns one real case page.
    recovered = [CandidateItem("italaw", "https://www.italaw.com/cases/9990",
                               "https://www.italaw.com/cases/9990",
                               "Newco v. Ruritania", None, "s", "trade secret",
                               {"retrieved_via": "internet-archive", "body_final": True})]
    monkeypatch.setattr(main_mod.source_recovery, "recover",
                        lambda name, since=None: list(recovered))
    monkeypatch.setattr(main_mod, "enrich", lambda it: it)
    monkeypatch.delenv("MODEL_PROVIDER", raising=False)
    monkeypatch.setattr(main_mod, "send_digest", lambda *a, **k: True)
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    shutil.copytree(os.path.join(repo, "templates"), tmp_path / "templates")
    monkeypatch.chdir(tmp_path)
    state.save_state({"sources": {"italaw": {"_seed": "t"}}}, "state/seen.json")

    rc = main_mod.main(["--since", "30d"])
    assert rc == 0
    folder = glob.glob("digests/*_ISDS-Thematic-Watch")[0]
    meta = json.loads(open(os.path.join(folder, "meta.json")).read())
    italaw = next(s for s in meta["source_health"] if s["name"] == "italaw")
    assert italaw["status"] == "RECOVERED (Internet Archive)"
    assert italaw["count"] == 1
    # The healed source produced no degradation / access-failure warning.
    assert not any("ACCESS FAILURE" in w or "DEGRADATION" in w
                   for w in meta.get("health_warnings", []))
