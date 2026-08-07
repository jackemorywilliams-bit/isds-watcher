# Bounded Change Protocol

**Status:** binding on every automated contributor to this repository.
**Operator:** Emory Williams.
**Principal investigator:** Dr. Ximena Benavides.

---

## Why this file exists in the repository

This protocol governed the project from 2026-07-18 and until 2026-08-06 it lived in
exactly one place: a private memory directory outside the repository, unversioned,
readable by no collaborator and by no reviewer. Every scope ruling that cited it —
including rulings by the council itself, on the same day this file was created — rested
on a document nobody but the operator could open.

That is a governance defect of the same shape as the research defects this project spent
2026-08-06 correcting: an authority asserted in one place and unverifiable everywhere
else. A rule that cannot be read cannot be checked, contested, or inherited.

It is now versioned, and it changes by pull request like anything else.

---

## The protocol

### 1. Preflight and plan before edits

State what will change and why **before** changing it. A plan that arrives with the diff
is not a plan.

### 2. The allowed-change manifest

Automated contributors may change, without further authorization:

- `scripts/verify.py`, `scripts/build_graph.py`
- the integrity-gate and analyst stage files
- `tests/`
- `working/`, `moc/`
- `.gitignore`
- `HANDOFF.md`, `README.md`, `METHODOLOGY.md`, `COUNCIL.md`
- model configuration

**Outside the manifest, and requiring the operator's explicit authorization each time:**

- `src/` — the pipeline itself
- `HUMAN_REVIEW.md`
- anything that pushes, merges, or publishes

### 3. Fail closed on missing evidence

Where evidence is absent, stop and say so. Do not infer, do not proceed on the balance of
probability, and do not record an inference in a form that will later read as a finding.
A guard that skips when its input is missing reproduces the defect it was built to
prevent — see `scripts/check_sources.py`, which fails rather than skipping when a
declared source is absent, and says why in its own docstring.

### 4. The verification ledger is append-only and operator-gated

Only the operator marks a claim verified (`scripts/verify.py mark`). No automated path
may, and `verify.py` enforces this by raising rather than by convention. A claim becomes
a validated finding only after a person has opened its source, confirmed it supports the
claim, and signed.

### 5. Commit in named units, each leaving the repository runnable

One idea per commit, with a message that explains the reasoning and not just the diff.

### 6. No push without explicit authorization

Protocol work stays local until the operator says otherwise.

### 7. Report requested-versus-actual model fallbacks

Where a model differs from what was requested, record it in `HANDOFF.md`.

---

## Why the operator adopted it

A live research system with a professor-facing deliverable, after being burned by
unverified assertions and by jargon-laden correspondence. The protocol exists to make
both failure modes expensive.

---

## Standing rules that sit alongside it

These are not part of the protocol proper but bind the same contributors and are
recorded here because they have the same problem the protocol had — they were carried in
conversation and in private memory rather than in the repository.

- **Third-party text never enters the repository.** The repo is public and a commit is
  publication. Dr. Benavides's review comments, and any correspondence, stay outside it.
- **Copyrighted sources stay in gitignored `seeds/`.** The two literature articles and
  the three award PDFs live there and must never be committed.
- **`docs/` is generated** from `scripts/site_templates/` by `scripts/build_site.py`.
  Never hand-edited; source and build are committed together.
- **`METHODOLOGY.md` and `lit-review/*.md` are the operator's first-person documents.**
  Surgical edits only — never rewritten, restructured, reordered, or retitled.
- **No second coder.** Any proposal resting on two independent coders or inter-rater
  agreement is out of scope permanently, in any form, including "a second model reviews
  it."

---

## The guards that enforce parts of this

| Guard | Enforces |
|---|---|
| `scripts/check_marks.py` | Verification marks are present and well-formed |
| `scripts/check_models.py` | Card, definition and vault note agree on every seat's model |
| `scripts/check_claims.py` | A registry of facts stays consistent across the repo |
| `scripts/check_sources.py` | Every quotation exists in the source it names; fails closed on a missing source |
| `scripts/check_currency.py` | A note may not claim to be current when git says it is not |

None of them enforces §1, §2, §5 or §6. Those remain human obligations, and this file is
where they are now written down.
