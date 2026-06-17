# Standing review — run before any change is "done"

This is the review discipline every substantive change passes before it ships.
It exists because the same class of defect recurred three times during bring-up:
**one label ("screened", "accepted") was allowed to mean two different things on
two surfaces.** The checklist below is built to catch that and its relatives. The
test suite and `scripts/validate_archive.py` are the mechanical backstop; this
document is the judgment that runs first.

## The core invariant

> Every count and every label means **exactly one thing**, everywhere it appears.
> No surface prints a bare metric (`Screened: N`) that another surface defines
> differently. If a number is cumulative, scoped, or filtered, its label says so.

## Before declaring done

**1. Counts reconcile across surfaces.** For any digest date, the email footer,
the website "Latest run" box, the archive row, the per-date page, and `meta.json`
show the same screened / matches / accepted. Definitions are fixed:
- `screened` = candidates fetched and scored after dedupe
- `matches` = items scoring ≥ threshold (40)
- `watch-list leads` = surfaced items scoring 25–39 (floor..threshold-1)
- `accepted` = matches + watch-list leads actually shown

**2. Scope is labeled.** A cumulative or pooled artifact (the aggregate bring-up
digest) never reuses bare per-run labels. It reads "cumulative", "collected",
"distinct findings", etc., so it can't be read as a single run's numbers.

**3. No placeholders reached the output.** No "View case details", "(untitled)",
or empty titles in any surfaced item. Real case names only.

**4. Methodology floor is honored.** Nothing below the relevance floor (25) is
surfaced or archived. A quiet period yields fewer items, not padded ones.

**5. Honesty over padding.** Scores are never inflated to manufacture matches.
A zero-match period is reported as a finding, framed but not disguised. Claims in
METHODOLOGY.md match what the code actually does.

**6. The backstop is green.** `pytest tests/` passes and
`python scripts/validate_archive.py` exits clean. If the change altered counting,
labeling, or selection, a test asserts the new invariant.

## Mechanical backstop (runs without us)

- `scripts/validate_archive.py` — floor, placeholder titles, count reconciliation;
  wired as a hard gate in `.github/workflows/weekly.yml`.
- `tests/` — including `test_archive_integrity.py`, the count-consistency test,
  the cumulative-labeling test, and the no-clobber guard.

If a defect slips past this list, the fix is not only to patch it but to add the
missing check here and in the backstop, so the same class can't return.
