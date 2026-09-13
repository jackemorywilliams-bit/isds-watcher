# Retrieval ledger — externally gated items

Nothing enters `items.json` until its primary document is retrieved and its
pinpoint verified. Status values: `QUEUED` (library task), `RETRIEVED`
(document in hand, pinpoint verified), `BLOCKED` (access barrier named).
This file is append-only; entries are dated.

## Standing blocked items (2026-08-08 — carried from the project's open list)

| Item | Status | Barrier |
|---|---|---|
| Tethyan Copper ¶¶ 1283, 1288, 1327–1333 | BLOCKED | Paywalled at IIC 1603 (2019) |
| Thailand—Cigarettes ¶¶ 7.410–7.411 | BLOCKED | PDF text layer will not extract |
| Lord Falconer Manchester Speech (2006) | BLOCKED | Absent from UK Government web archive |
| 15 J. Marshall Rev. Intell. Prop. L. bound volume (999 vs 228) | QUEUED | Law-library queue |
| Philip Morris v. Uruguay, Decision on Jurisdiction (2 Jul 2013) ¶ 185 | QUEUED | Holding-or-recital undeterminable from sources in hand |
| Vanda — Federal Circuit docket + any merits disposition | QUEUED | Not yet consulted; no number may be stated until read |
| Vanda v. United States, No. 23-629C (Fed. Cl.), slip op. 18 Jan. 2024 | RETRIEVED (2026-08-06; verified 2026-08-08) | seeds/Vanda_v_US_23-629C_FedCl_2024-01-18_slip_op.pdf |
| Vanda v. United States, No. 23-629C (Fed. Cl.), slip op. 22 Jan. 2025 | RETRIEVED (2026-08-06; verified 2026-08-08) | seeds/Vanda_v_US_23-629C_FedCl_2025-01-22_slip_op.pdf |
| Landreau award — holding and pinpoint | QUEUED | Unread |
| EMA Policy 0070 post-2023 sequence | QUEUED | Unverified against EMA primary documents |
| Lentner, 34 ICSID Rev. 569 (2019) | QUEUED | Unconfirmed against the journal |
| OI European Group v. Venezuela award | QUEUED | Bibliography entry must be drafted from the award itself |
| IBA Rules on the Taking of Evidence (2020); ICC Note to Parties; Aceris commentary | QUEUED | Entries drafted only from the instruments |

## Locked-set retrieval queue — 0 rows; 54 is a design target, not a queue

None retrieved as of 2026-08-08. The candidate matters named in the R2.1
record are leads; each row added here must carry: category, caption as printed
on the retrieved document, document date, URL, pinpoint, and the date
retrieved.

## Batch 1 — category 8, tier S — 6 rows retrieved 2026-09-13

Retrieved under Ruling 3(i) of the council's rulings session of 2026-09-13.
Source: `iareporter_headlines`, the instrument's own headline-only source
(`src/config.py` `HEADLINE_ONLY_SOURCES`; `src/enrich.py` `NO_BODY_FETCH`). The
site is paywalled and **no body was fetched for any row** — the caption below is
the whole of what was retrieved, which is what `raw_text = title` means in
production. Captions are transcribed from the homepage "News Headlines" list
(`https://www.iareporter.com/`, the listing the fetcher itself reads) and were
byte-compared against the same items' `<title>` in the site's RSS feed
(`https://www.iareporter.com/feed/`); all six matched exactly. The homepage
listing prints no date, so the **document date is the feed's `pubDate`** for the
same URL, converted to a UTC calendar date — the feed is the only date the
source publishes.

**Pinpoint:** none exists and none is asserted. A tier-S item is a caption and a
locator; there is no paragraph to pin. `SCHEMA.md:52-53`.

**Selection was positional, never by content:** the six are entries 1-6 of the
homepage list in the site's own printed order, taken in that order. No row was
chosen, moved, skipped or preferred for what it is about.

| Cat | Caption as printed | Document date | URL | Pinpoint | Retrieved |
|---|---|---|---|---|---|
| 8 | Belarusian state-owned entity turns to Russian courts to challenge arbitrator in UNCITRAL arbitration based on her dual Russian-UK citizenship | 2026-09-11 | https://www.iareporter.com/articles/belarusian-state-owned-entity-turns-to-russian-courts-to-challenge-arbitrator-based-on-her-dual-russian-uk-citizenship-in-uncitral-arbitration/ | none — tier S, headline only | 2026-09-13 |
| 8 | Greece makes appointments to ICSID panels of arbitrators and conciliators | 2026-09-11 | https://www.iareporter.com/articles/greece-makes-new-appointments-to-icsid-panels-of-arbitrators-and-conciliators/ | none — tier S, headline only | 2026-09-13 |
| 8 | Singapore court declines to set aside award in energy equipment supply dispute arising from breach of contractual sanctions clause | 2026-09-11 | https://www.iareporter.com/articles/singapore-court-declines-to-set-aside-award-in-energy-equipment-supply-dispute-arising-from-breach-of-contractual-sanctions-clause/ | none — tier S, headline only | 2026-09-13 |
| 8 | Cameroon at risk of arbitration over reported delay in implementing settlement of toll road dispute | 2026-09-10 | https://www.iareporter.com/articles/cameroons-reported-delay-in-implementing-settlement-of-toll-road-dispute-faces-arbitration-risk/ | none — tier S, headline only | 2026-09-13 |
| 8 | Cameroon is reportedly ordered to pay damages in ICSID arbitration lodged by Italian investor | 2026-09-10 | https://www.iareporter.com/articles/cameroon-reportedly-ordered-to-pay-damages-in-icsid-arbitration-lodged-by-italian-investor/ | none — tier S, headline only | 2026-09-13 |
| 8 | Collection of 5-billion-USD fine at the centre of ICSID arbitration between Kazakhstan and group of oil majors is suspended | 2026-09-10 | https://www.iareporter.com/articles/collection-of-5-billion-usd-fine-at-the-centre-of-icsid-arbitration-between-kazakhstan-and-group-of-oil-majors-is-suspended/ | none — tier S, headline only | 2026-09-13 |

### Disjointness, as run at this commit

Proved against all three development sets named at `SCHEMA.md:87-94`, not only
the two named in the executing instruction — the published matters are a
development set under Ruling 1 and the stricter constraint governs.

- **The retired 20-item holdout** (`scripts/holdout_set.json`, 20 items) and
  **the 14 frozen probes** (`analytics/fingerprint_probes.json`):
  `grep -c -F -f <the six URLs> scripts/holdout_set.json analytics/fingerprint_probes.json`
  → `0` and `0`. Matter-level as well as URL-level: the holdout's four positives
  are Loewen, Mondev, Apotex and Philip Morris v. Uruguay and its sixteen
  negatives are `iisd_itn` and `icsid` listings; all fourteen probes are
  synthetic. `grep -c -i -E "iareporter|belarus|greece|singapore|cameroon|kazakhstan"`
  over both files → `0` and `0`. No `iareporter_headlines` item is in either set.
- **The published matters** (17 article files under `digests/*/articles/`):
  `grep -rc -F -f <the six URLs> digests/ state/seen.json` → no non-zero line.
  Independently: every published digest is dated on or before 2026-09-07 and all
  six rows were published by the source on 2026-09-09 to 2026-09-11, so none can
  have been screened, let alone surfaced. They are absent from `state/seen.json`
  for the same reason.

### What these six are not

They are six rows of item content. **No label, no score, no band and no
judgement about any row's subject matter is recorded here or in `items.json`,
whose schema has no label fields** (`SCHEMA.md:16`). Per Ruling 3(iv), six items
measure grammar fidelity and whether any tier-S item surfaces at all; they are
not precision, not recall, and no seat may report batch 1 as validation.
