# Capture witness — batch 1

**What this file is for, and why it is not the lock.** `LOCK.md` freezes what was captured. It is silent on *how* the capture was made, and for batch 1 the how is the whole anti-contamination guarantee: the six items were taken by **position** — entries 1 to 6 of the source's own printed order — and not chosen. A byte-match of the captions against the site's RSS corroborates the captions; it does not corroborate the position. Once the homepage moves, nobody can re-audit "entries 1 through 6" from the live site. This file is the artefact that lets them audit it anyway.

**It is deliberately outside the hash.** `items.json`'s bytes do not change, the committed step-2 entry in `LOCK.md` stands, and nothing re-locks. No field was added to `items.json`.

> **The binding limit on what these six items may be said to measure (Ruling 3(iv), 2026-09-13, binding on every seat):** six items measure grammar fidelity — the band the instrument assigns, against `L_band` — and whether any tier-S item surfaces at all. **They do not measure precision. They do not measure recall. No seat may report batch 1 as validation.** A Clopper-Pearson interval on 6/6 is [0.54, 1.00].

---

## 1. The raw listing WAS preserved

The capture was retained at capture time and this file is written from it, not from a later fetch. Both responses are held outside the repository (they are third-party documents; the council's standing rule of 2026-08-03 is that **the reduction travels, never the document**), so what is committed here is the ordered captions, the URLs, the ordering and the digests — not the pages.

| Capture | Fetched (local, UTC-4) | Fetched (UTC) | Bytes | SHA-256 of the response body |
|---|---|---|---|---|
| `https://www.iareporter.com/` (the listing the fetcher reads) | 2026-09-13T18:18:10-0400 | 2026-09-13T22:18:10Z | 65431 | `bd3c4633c6d8a30912743a8c09c6cbd5b81df6f4f205fc45938063fc6120eedd` |
| `https://www.iareporter.com/feed/` (the positional corroborant) | 2026-09-13T18:19:12-0400 | 2026-09-13T22:19:12Z | 23739 | `9304767db1c0d587455da4656606e69bc385c58c15ee7c15332a768924d7df7e` |

The two fetches are 62 seconds apart. **The timestamps are the saved responses' modification times, not a server `Date` header** — response headers were not retained, so the capture time is evidenced to the second by the local filesystem and no better than that. Stated rather than smoothed over, because a witness that overstates its own provenance is worse than none.

**No article body was fetched, for any entry, at any point.** The source is paywalled and the caption is the whole item.

## 2. The printed listing as it stood at capture, in order

Every anchor on the homepage whose `href` contains `/articles/` is listed below **in document order**, including the three the fetcher's own filters drop — a witness that showed only the survivors would be hiding exactly the step where a selection could have been made. The filters are the source's, unmodified (`src/sources/iareporter_headlines.py`: text length > 20, deduplicate by URL).

The pool contained **14 `/articles/` anchors, 11 of which survived the filters**. There is no twentieth entry to show: the homepage does not print one.

| Printed # | Enclosing block | Caption as printed | URL | Filter outcome |
|---|---|---|---|---|
| 1 | `list-News` | Belarusian state-owned entity turns to Russian courts to challenge arbitrator in UNCITRAL arbitration based on her dual Russian-UK citizenship | https://www.iareporter.com/articles/belarusian-state-owned-entity-turns-to-russian-courts-to-challenge-arbitrator-based-on-her-dual-russian-uk-citizenship-in-uncitral-arbitration/ | kept |
| 2 | `list-News` | Greece makes appointments to ICSID panels of arbitrators and conciliators | https://www.iareporter.com/articles/greece-makes-new-appointments-to-icsid-panels-of-arbitrators-and-conciliators/ | kept |
| 3 | `list-News` | Singapore court declines to set aside award in energy equipment supply dispute arising from breach of contractual sanctions clause | https://www.iareporter.com/articles/singapore-court-declines-to-set-aside-award-in-energy-equipment-supply-dispute-arising-from-breach-of-contractual-sanctions-clause/ | kept |
| 4 | `list-News` | Cameroon at risk of arbitration over reported delay in implementing settlement of toll road dispute | https://www.iareporter.com/articles/cameroons-reported-delay-in-implementing-settlement-of-toll-road-dispute-faces-arbitration-risk/ | kept |
| 5 | `list-News` | Cameroon is reportedly ordered to pay damages in ICSID arbitration lodged by Italian investor | https://www.iareporter.com/articles/cameroon-reportedly-ordered-to-pay-damages-in-icsid-arbitration-lodged-by-italian-investor/ | kept |
| 6 | `list-News` | Collection of 5-billion-USD fine at the centre of ICSID arbitration between Kazakhstan and group of oil majors is suspended | https://www.iareporter.com/articles/collection-of-5-billion-usd-fine-at-the-centre-of-icsid-arbitration-between-kazakhstan-and-group-of-oil-majors-is-suspended/ | kept |
| 7 | `list-News` | Lima’s petition to set aside partial award in Rutas de Lima v. Lima (3) brings tribunal’s decisions to light | https://www.iareporter.com/articles/limas-petition-to-set-aside-partial-award-in-rutas-de-lima-v-metropolitan-municipality-of-lima-brings-tribunals-decisions-to-light/ | kept |
| 8 | `list-News` | Revealed: Identity of UNCITRAL tribunal hearing Mikhail Fridman’s arbitration claim against the UK comes to light | https://www.iareporter.com/articles/revealed-identity-of-uncitral-tribunal-hearing-mikhail-fridmans-arbitration-claims-against-the-uk-comes-to-light/ | kept |
| 9 | `list-News` | Dual Russian-Belarussian national makes good on earlier threat to lodge ICSID arbitration against Armenia | https://www.iareporter.com/articles/dual-russian-belarussian-national-makes-good-on-earlier-threat-to-lodge-icsid-arbitration-against-armenia/ | kept |
| 10 | `list-News` | Ukraine’s state trading company discloses details on pending LCIA arbitration against US defense supplier | https://www.iareporter.com/articles/ukraines-state-trading-company-discloses-details-on-pending-lcia-arbitration-against-us-defense-supplier/ | kept |
| — | `sidebarBlock` | Revealed: Identity of UNCITRAL tribunal hearing Mikhail Fridman’s arbitration claim against the UK comes to light | https://www.iareporter.com/articles/revealed-identity-of-uncitral-tribunal-hearing-mikhail-fridmans-arbitration-claims-against-the-uk-comes-to-light/ | skipped: duplicate URL |
| 11 | `sidebarBlock` | Solar investors withdraw US enforcement bid against Spain, following partial annulment of ECT award | https://www.iareporter.com/articles/solar-investors-withdraw-us-enforcement-bid-against-spain-following-partial-annulment-of-ect-award/ | kept |
| — | `list-News2` | view full profile | https://www.iareporter.com/articles/arbitrator/john-fellas/ | skipped: text length 17 <= 20 |
| — | `list-News2` | view full profile | https://www.iareporter.com/articles/arbitrator/ignacio-suarez-anzorena/ | skipped: text length 17 <= 20 |

Two things on the face of that table matter to the position claim:

- **Printed 1 through 10 are all in `ul.list-News`** — the block the page itself heads "News Headlines". Printed 11 is in a `sidebarBlock`, a different surface. So the six drawn are entries 1 to 6 of the News Headlines list with no ambiguity about which list was being counted.
- The one deduplicated anchor is printed 8 (Fridman), which the page repeats in a sidebar. Dropping the repeat changes no ordinal at or below 6.

## 3. The feed's own ordering over the same entries

| Feed # | `pubDate` | Title as published in the feed | URL |
|---|---|---|---|
| 1 | Fri, 11 Sep 2026 14:23:55 +0000 | Belarusian state-owned entity turns to Russian courts to challenge arbitrator in UNCITRAL arbitration based on her dual Russian-UK citizenship | https://www.iareporter.com/articles/belarusian-state-owned-entity-turns-to-russian-courts-to-challenge-arbitrator-based-on-her-dual-russian-uk-citizenship-in-uncitral-arbitration/ |
| 2 | Fri, 11 Sep 2026 14:19:21 +0000 | Greece makes appointments to ICSID panels of arbitrators and conciliators | https://www.iareporter.com/articles/greece-makes-new-appointments-to-icsid-panels-of-arbitrators-and-conciliators/ |
| 3 | Fri, 11 Sep 2026 14:02:51 +0000 | Singapore court declines to set aside award in energy equipment supply dispute arising from breach of contractual sanctions clause | https://www.iareporter.com/articles/singapore-court-declines-to-set-aside-award-in-energy-equipment-supply-dispute-arising-from-breach-of-contractual-sanctions-clause/ |
| 4 | Thu, 10 Sep 2026 17:12:39 +0000 | Cameroon at risk of arbitration over reported delay in implementing settlement of toll road dispute | https://www.iareporter.com/articles/cameroons-reported-delay-in-implementing-settlement-of-toll-road-dispute-faces-arbitration-risk/ |
| 5 | Thu, 10 Sep 2026 17:07:40 +0000 | Cameroon is reportedly ordered to pay damages in ICSID arbitration lodged by Italian investor | https://www.iareporter.com/articles/cameroon-reportedly-ordered-to-pay-damages-in-icsid-arbitration-lodged-by-italian-investor/ |
| 6 | Thu, 10 Sep 2026 17:04:09 +0000 | Collection of 5-billion-USD fine at the centre of ICSID arbitration between Kazakhstan and group of oil majors is suspended | https://www.iareporter.com/articles/collection-of-5-billion-usd-fine-at-the-centre-of-icsid-arbitration-between-kazakhstan-and-group-of-oil-majors-is-suspended/ |
| 7 | Thu, 10 Sep 2026 16:55:35 +0000 | Lima’s petition to set aside partial award in Rutas de Lima v. Lima (3) brings tribunal’s decisions to light | https://www.iareporter.com/articles/limas-petition-to-set-aside-partial-award-in-rutas-de-lima-v-metropolitan-municipality-of-lima-brings-tribunals-decisions-to-light/ |
| 8 | Wed, 09 Sep 2026 17:16:48 +0000 | Revealed: Identity of UNCITRAL tribunal hearing Mikhail Fridman’s arbitration claim against the UK comes to light | https://www.iareporter.com/articles/revealed-identity-of-uncitral-tribunal-hearing-mikhail-fridmans-arbitration-claims-against-the-uk-comes-to-light/ |
| 9 | Wed, 09 Sep 2026 17:15:38 +0000 | Dual Russian-Belarussian national makes good on earlier threat to lodge ICSID arbitration against Armenia | https://www.iareporter.com/articles/dual-russian-belarussian-national-makes-good-on-earlier-threat-to-lodge-icsid-arbitration-against-armenia/ |
| 10 | Wed, 09 Sep 2026 17:03:08 +0000 | Ukraine’s state trading company discloses details on pending LCIA arbitration against US defense supplier | https://www.iareporter.com/articles/ukraines-state-trading-company-discloses-details-on-pending-lcia-arbitration-against-us-defense-supplier/ |

## 4. Feed order against printed order — item by item

Not summarised. Each printed entry is named with the feed position it occupies and whether the two texts are byte-identical.

| Printed # | Feed # | Agree on position? | Caption byte-identical? | Caption |
|---|---|---|---|---|
| 1 | 1 | YES — both 1 | YES | Belarusian state-owned entity turns to Russian courts to challenge arbitrator in UNCITRAL arbitration based on her dual Russian-UK citizenship |
| 2 | 2 | YES — both 2 | YES | Greece makes appointments to ICSID panels of arbitrators and conciliators |
| 3 | 3 | YES — both 3 | YES | Singapore court declines to set aside award in energy equipment supply dispute arising from breach of contractual sanctions clause |
| 4 | 4 | YES — both 4 | YES | Cameroon at risk of arbitration over reported delay in implementing settlement of toll road dispute |
| 5 | 5 | YES — both 5 | YES | Cameroon is reportedly ordered to pay damages in ICSID arbitration lodged by Italian investor |
| 6 | 6 | YES — both 6 | YES | Collection of 5-billion-USD fine at the centre of ICSID arbitration between Kazakhstan and group of oil majors is suspended |
| 7 | 7 | YES — both 7 | YES | Lima’s petition to set aside partial award in Rutas de Lima v. Lima (3) brings tribunal’s decisions to light |
| 8 | 8 | YES — both 8 | YES | Revealed: Identity of UNCITRAL tribunal hearing Mikhail Fridman’s arbitration claim against the UK comes to light |
| 9 | 9 | YES — both 9 | YES | Dual Russian-Belarussian national makes good on earlier threat to lodge ICSID arbitration against Armenia |
| 10 | 10 | YES — both 10 | YES | Ukraine’s state trading company discloses details on pending LCIA arbitration against US defense supplier |
| 11 | ABSENT | n/a — not in the feed | n/a | Solar investors withdraw US enforcement bid against Spain, following partial annulment of ECT award |

### The finding, and its one divergence named

**Feed order matched printed order exactly for printed entries 1 through 10**, and each of those ten captions is byte-identical between the two surfaces. Two independently served representations of the listing agreed on the ordinal of every entry.

**The one divergence, named rather than summarised: printed 11 — "Solar investors withdraw US enforcement bid against Spain, following partial annulment of ECT award" — is absent from the feed.** The feed carries ten items and the printed list eleven, so the divergence is a **length cutoff at the feed's tail, not a reordering**: no feed entry is missing from the printed listing, and no entry appears at a different ordinal in one than the other. It is below the draw and cannot touch it — but it is the reason this file says "1 through 10 agree" and not "the two orderings are identical", which would be false.

## 5. What this witnesses, and what it does not

**Witnessed.** That at 2026-09-13T22:18:10Z the pool's printed order was as set out in §2; that a second, independently served representation of the same pool agreed on the ordinal of every entry it carried; and that `items.json`'s `cat8-01` … `cat8-06` are printed entries 1 to 6 of that order, in that order.

**Not witnessed.** That the site's printed order is itself reverse-chronological, or any other property of the source's editorial ordering — the `pubDate` column in §3 is consistent with it and is not proof of it. And nothing here speaks to whether the ordering is stable over time; it is not, which is why this file exists.

**Reproducibility, stated plainly as a limitation.** Batch 1 cannot be re-derived by re-running the fetcher: the homepage moves, and a listing taken later is evidence about later. The items are frozen by the `LOCK.md` step-2 hash and their position is frozen by this witness. A future batch that wants re-runnable provenance needs a different capture discipline, and that is a question for the chair before batch 2, not a defect cured here.

