# The validation record (2026-09-13)

Cited as **the validation record (2026-09-13)**. This file is
`analytics/locked_set/VALIDATION_RECORD.md`.

---

## 0. Provenance — what this replaces, and why it does not wear its name

This record **replaces** the document this repository cites throughout as **"the
R2.1 record"**: the stated source of the locked validation set's design — its nine
categories, its 54 named candidate matters, its tier rules, its acceptance criteria
V1–V6, its stop-publication rules S1–S4, its stability thresholds and its triage
costing table.

**The R2.1 record has never existed as a file on any branch of this repository.**

The check, run at the commit this record was drafted against:

```
git log --all --diff-filter=A --name-only --pretty=format: | sort -u | grep -i r2
```

returns **nothing** — no path ever added to this repository, on any branch, in the
whole of the reachable history, has `r2` in its name. The coordinating seat also
searched the working tree, this project's session transcripts, the cloud routines
and the operator's document folders. It is not there either. The document was
reasoned from and cited; it was never committed.

**The loss is not concealed and the name is not reused.** A document that never
existed must not be silently satisfied by a different document wearing its name:
that would convert a documented absence into an undetectable substitution, and the
record of the loss is itself evidence this project needs. "R2.1" therefore survives
in two places only — inside historical narrative (`analytics/daily-research/*`,
`analytics/*-2026-08-*.md`, the special-session record), which is **not edited**,
because editing a record of what was lost falsifies the record of the loss; and
inside this provenance header.

### The authority for re-deriving it

The operator's delegation of 2026-09-13, quoted verbatim, typographical errors
included, as the written authority:

> "dont be fucking lazy whatever is lost isw lost becuase of you, figrue it outr and
> bridge tghe gaps, make the judgement calls by convening the councl and undertsand to do
> it as efficiently as possible maximizing token usage and update me when all is updated,
> use your judgement to make the required fixes dont tell me to do soemthing myself that
> you yourself a. fucked up and b. orginally took on to begin wiht proactivley"

Under that delegation the council ruled (RULING 1, rulings of the chair,
2026-09-13) that it re-derives the candidate list rather than reconstructing the
lost record.

### On the face of this record

1. **A seat chose the candidate matters in §3 under delegated authority.** They are
   one analyst's nominations, not the operator's, and not a recovered list.
2. **The operator may substitute any row freely, at any time, without stating a
   reason.** No row in §3 has standing against his substitution.
3. **The original R2.1 record was never under version control on any branch.**
4. **No row in §3 is a label, a score, or a finding.** Every row is a LEAD. Per
   §3's binding constraints, no item enters `items.json` on this record's authority.

---

## 1. What survives in the repository — verified line by line, not re-derived

Re-deriving something the repository already holds is fabrication dressed as
recovery. Each survivor below was opened and read at
`origin/main` = `66df2d2`, and is quoted with its own pinpoint. **The line numbers
in this section are as of `66df2d2`**; the tier-P amendment committed on this same
branch (RULING 2) lengthens the tier-P bullet from 6 printed lines to 14, so every
`SCHEMA.md` citation below line 51 shifts by **+8** after that commit. Both
numbers are given where the shift applies.

| Element | Status | Pinpoint (at `66df2d2`) | Pinpoint (after the RULING 2 amendment) |
|---|---|---|---|
| Nine categories, with definitions | **SURVIVES** | `SCHEMA.md:74` (heading), `:76-84` (the nine) | `:82`, `:84-92` |
| Six-each / twenty-positives structure | **SURVIVES** | `SCHEMA.md:74` | `:82` |
| P / S / C tier rules | **SURVIVES** | `SCHEMA.md:43-55` (P at `:46-51`, as amended by RULING 2; S at `:52-53`; C at `:54-55`) | `:43-63` |
| `labels.json` field set | **SURVIVES** | `SCHEMA.md:57-72` (JSON block `:59-67`) | `:65-80` (JSON block `:67-75`) |
| Blind commit order | **SURVIVES** | `SCHEMA.md:14-20`, enforced by `scripts/check_lock.py` (wired at `.github/workflows/pipeline-guards.yml:140,160`, per `SCHEMA.md:22-24`) | unchanged / `:22-24` |
| Disjointness constraints | **SURVIVES** | `SCHEMA.md:86-94` | `:94-102` |
| 20×10 stability design + four blocking thresholds | **SURVIVES VERBATIM** | `SCHEMA.md:105-107` | `:113-115` |
| S4 stop-publication rule | **SURVIVES IN SUBSTANCE** | `SCHEMA.md:107-109` | `:115-117` |
| Triage per-call cost | **SURVIVES AS A COMMITTED CONSTANT** | `src/config.py`, `TRIAGE_COST_PER_CALL_USD = 0.0014` | unchanged |
| **The 54 named candidate matters** | **LOST** | — | — |
| **V1–V6 acceptance criteria; S1–S3** | **LOST** | — | — |

**Correction to the ruling's own citations, filed against this seat's instruction
rather than around it.** RULING 1's survivor table cites `SCHEMA.md:75-83`,
`:45-54`, `:14-20`/`:56-71`, `:87-89`, `:106-107` and `:108-109`. Re-measured at
`66df2d2`, four of those ranges are off by one line or truncate the element they
name (the nine categories run `:76-84`, not `:75-83`; the tier rules run `:43-55`;
the `labels.json` section runs `:57-72`; the disjointness paragraph runs `:86-94`;
the stability sentence begins at `:105`, not `:106`; S4's sentence begins at
`:107`). The **content** the ruling identified survives in every case and no
survivor was lost or added by the correction. The ranges above are the measured
ones and supersede the ruling's, per taxonomy entry 25 — work from a freshly
measured list at the executing commit, never from a remembered one.

### The four blocking thresholds, transcribed verbatim

From `SCHEMA.md:105-107`:

> Stability: 20 items × 10 runs; blocking thresholds per the R2.1 record (decision
> flip > 0.10, mean score range > 10, any range > 20, silent-fallback rate > 0.05).

These four numbers are **carried, not re-derived**: they are read off a committed
file, not remembered. The clause "per the R2.1 record" attributes them to the lost
document; the numbers themselves are in `SCHEMA.md` and are therefore preserved.
The 20×10 design is preserved by the same sentence.

### S4, in substance

From `SCHEMA.md:107-109`:

> Acceptance V1–V6 and stop-publication S1–S4 per the R2.1 record; S4 (zero
> positives reach 40 on the production path) is the current state of the system and
> the reason the fill-floor is suspended.

S4's **content** — zero positives reach 40 on the production path — is preserved on
the face of `SCHEMA.md`. Its identifier, its ordering among S1–S3, and any threshold
or tolerance it carried are not.

---

## 2. What is LOST and is NOT reconstructed

**The 54 named candidate matters are lost.** §3 below is a new list drafted by a
seat in 2026, not a recovery of theirs. No claim is made that any row in §3 was in
the lost record, and no claim is made that any row of the lost record is absent
from §3. Those two lists cannot be compared, because one of them no longer exists.

**V1–V6 and S1–S3 are lost and are not re-derived under their own names.**

Rebuilding six acceptance criteria and three stop-publication rules from a
remembered number set **would fabricate the acceptance bar itself.** That is
strictly worse than having no acceptance bar at all: an instrument with no bar
reports an uncalibrated result and says so, while an instrument that passes a
fabricated bar produces a *validated-looking* result with no provenance, and no
later reader — the operator, the recipient, an external auditor — could tell the
difference from the artefact. The number that decides whether this project's
classifier is fit to publish must not be a number someone remembered.

### The replacement schedule — drafted by another seat, not here

A new, smaller, pre-registered schedule is being drafted under **new prefixes that
cannot be confused with the originals**:

- **`ACC-1 … ACC-n`** — acceptance criteria.
- **`HALT-1 … HALT-n`** — stop-publication rules. `HALT-1` carries S4's preserved
  content, because that content is *preserved* (`SCHEMA.md:107-109`), not
  remembered.

The 20×10 stability design and its four thresholds are transcribed into that
schedule from `SCHEMA.md:105-107` and marked **carried, not re-derived**.

**Seat: systems-researcher drafts. Integrity-officer reviews. Chairman adopts.**
It is committed **before the first label is coded**, as a pre-registration, and per
taxonomy entry 34 it states only what the repository supports and marks anything
inferred as inferred.

### PLACEHOLDER — reserved, deliberately empty

> ### 2.1 `ACC-1 … ACC-n` and `HALT-1 … HALT-n`
>
> **Not written here. Reserved for the systems-researcher's pre-registered
> schedule.** This analyst seat drafted the candidate list in §3 and therefore holds
> a stake in what the acceptance bar says; it does not write the bar. Any criteria
> appearing in this section that are not the systems-researcher's committed,
> integrity-reviewed, chairman-adopted schedule are void.
>
> Until that schedule is committed, **this instrument has no acceptance criteria**,
> and no seat may report the locked set as passing or failing anything.

---
