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
347 screenings, so no published figure is evidence about the instrument's accuracy at the
boundary its harness measures.
