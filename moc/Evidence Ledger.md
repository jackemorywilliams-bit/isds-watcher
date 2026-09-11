# Evidence Ledger

What the project actually knows, and on whose authority. Claims live in the
append-only verification ledger; only the operator can mark them verified.

- [[HUMAN_REVIEW]] — review checkpoints and completed cycles.
- [[REVIEW]] — the standing review discipline.
- Ledger: analytics/verification_ledger.jsonl (CLI: python scripts/verify.py status).
- analytics/locked_set/ — the planned 54-item validation set. **Empty of items on purpose**
  (SCHEMA.md), and RETRIEVAL_LEDGER.md records which primary documents are in hand:
  re-read 2026-08-09 and **unchanged from 2026-08-08 — two RETRIEVED, three BLOCKED, eight
  QUEUED**. Nothing enters the set on a memo's authority. `scripts/check_lock.py` (written
  2026-08-09, wired into CI) now enforces the hash discipline and reports the empty set as
  **the designed state rather than an error**, so it will begin doing real work the moment the
  first item lands.
  - **2026-09-10 — "empty on purpose" is now known to understate it: the 54 are not
    unretrieved, they are UNNAMED.** The nine category headings exist in exactly one place,
    SCHEMA.md:75-83, and no file in the repository assigns a single named matter to any of them.
    Their sole named source, **the R2.1 record, is not a file in this repository and never has
    been on any branch** — 56 occurrences of the literal across 17 tracked files at `948947b`,
    pointing at a document that has never been under version control. RETRIEVAL_LEDGER.md:26's
    header "Locked-set retrieval queue (54 items)" is followed by "None retrieved as of
    2026-08-08" and **no rows**; the 13 rows that do exist are the pre-existing open-source list,
    not locked-set items. **Zero of the 54 exist as ledger rows.** The scoping is binding: a grep
    establishes absence **from the repository**, never from the project — no seat may restate
    this as "the R2.1 record does not exist", and its probable home is the operator's chat
    history from the 2026-08-08/09 master-prompt session. **No seat may author, propose,
    pre-fill or reconstruct any part of the set** (BLOCKING 2), the coder is Emory alone, and
    "no second coder" includes "a second model reviews it".
    Source: analytics/daily-research/2026-09-10-special-session.md:128-174, :558-565;
    [[Workflow Threads]] **S1** and **B7**.
- **A retrieval that is real but is not in that ledger.** On 2026-08-09 the H&H v. Egypt
  (ICSID ARB/09/15) Decision on Jurisdiction and the Award's Rule 48(4) excerpts were retrieved
  into `seeds/` and 21 spans verified — but that matter has never had a row in
  RETRIEVAL_LEDGER.md, so it neither advances nor appears in the counts above. **The full Award
  is unpublished**: every quotation, and the zero-occurrence screen for IP vocabulary, is scoped
  to the published excerpts and the Decision on Jurisdiction. That is a **permanent scope limit,
  not a gap awaiting retrieval**, and the distinction is the point of recording it here.
- analytics/retrospective-audit-2026-08-08.md — the published archive re-derived from the
  files: 14 article files are **13 distinct URLs and 12 distinct matters**, and **6 of the 14
  entries disclaim themselves** in their own annotation.

Two standing cautions for anyone quoting a number from here. Seventeen of Emory's own
verification marks have never reached `main` (`agents/Workflow Threads.md` F1), so the ledger
count understates the review actually done. And no item has ever scored a true match (≥40) in
**492 screening events across the 16 archived runs** — read from the sixteen meta.json files at
the special session of 2026-09-10 and re-derived independently there, superseding the "347 in
11 runs" this note carried through 2026-08-03 — so no published figure is evidence about the
instrument's accuracy at the boundary its harness measures.

**Read 492 exactly as it is defined, because that is binding.** It is the sum of screening
**events** across the sixteen archived runs. No cross-run **distinct** total has been computed,
the denominator is not yet defined (row K, PR #163), same-day re-runs overwrite meta.json in
place so the archive retains the **last** run of a date rather than every run of it, and four
dates carry multiple runs. **No total above 492 and no de-duplicated figure may be published**,
and **nothing at all may be published from `per_source`** until
GAP-UNRESOLVED: per-source-count-semantics is resolved. Source:
analytics/daily-research/2026-09-10-special-session.md:57-72, :913-923; [[Workflow Threads]]
**S7**; [[Claim Map]] **C8**.
