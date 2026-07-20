# Fingerprint drift — Ring 1 vs the live research question

**Status: RECOMMENDATION ONLY. No weights have been changed.** Proposed reweighting
awaits operator approval; apply by editing `fingerprint.yaml` and re-running the
backtest (`analytics/backtest.md`) before trusting new scores.

## What Ring 1 currently rewards

Ring 1 (`ip_as_investment`) is still weighted toward the seed awards' subject matter —
patent and trademark disputes:

| Cluster | Phrases (weight) | Total |
|---|---|---|
| Patent (Eli Lilly) | promise utility doctrine (14), utility requirement (10), patent invalidation (5), promise doctrine (3) | **32** |
| Trademark (Bridgestone) | trademark (8), exploitation of the trademark (3), licenses that constitute its investment (4), licensor (4), licensee (4), brand value (4) | **27** |
| General IP | covered investment (8), intellectual property (4), geographical indication (4), copyright (2) | **18** |
| **Trade-secret / clinical-data (the live question)** | trade secret (6), clinical trial data (5), data exclusivity (4), test data (3), unfair commercial use (3), trips article 39 (2) | **23** |

## What the live question needs

The research front has moved to pharmaceutical trade secrets and clinical trial data
(Ferguson/Kim; *Einarsson* pending; China's 2026 data-exclusivity regime; USTR 2026
Special 301 "unfair commercial use" language — the operator-verified claim in the
ledger). A candidate squarely on that front — e.g. an item about "regulatory data
protection" and "marketing approval" that never says "patent" or "trademark" — scores
at most 23 of Ring 1's weight, while an off-question patent-utility story can score 32.
The instrument is tuned for where the question was, not where it is.

Known related gap (METHODOLOGY.md Part VI.B): the scorer also misses
"not-a-covered-investment" *rejections* (the Apotex outer limit; now also the *Hela
Schwarz* shape) because Ring 1 has no negative-space phrasings.

## Proposed reweighting (for operator approval — not applied)

Raise the trade-secret/clinical-data cluster to parity with the patent cluster, funded
by trimming seed-specific phrasings that only ever match retellings of the seed cases
themselves; add the missing regulatory-data vocabulary:

| Phrase | Now | Proposed | Rationale |
|---|---|---|---|
| trade secret | 6 | **10** | core of the live question |
| clinical trial data | 5 | **9** | core (Kim) |
| data exclusivity | 4 | **8** | China 2026 regime vocabulary |
| unfair commercial use | 3 | **6** | TRIPS 39(3) / USTR operative phrase |
| trips article 39 | 2 | **5** | treaty hook named by Ferguson/Kim |
| regulatory data protection | — | **6** | new; the term of art in the 2026 China instruments |
| undisclosed test or other data | — | **4** | new; TRIPS 39(3)/USTR literal phrase |
| know-how | — | **3** | new; the BIT investment-definition hook (China–Switzerland/France) |
| promise utility doctrine | 14 | **8** | seed-specific; matches little beyond Eli Lilly retellings |
| utility requirement | 10 | **6** | same |
| brand value | 4 | **2** | weak discriminator |

Net effect: trade-secret/clinical-data cluster 23 → **51**; patent cluster 32 → **22**.
Ring 2 and Ring 3 untouched. Risks: (a) more MEDIUM-band pharma-regulatory news that is
IP-adjacent but not ISDS — mitigated because Ring 1 alone still cannot cross the digest
threshold (40) without a second ring; (b) backtest F1 (illustrative 0.86) must be re-run
— seed awards themselves must still score HIGH, which they do on the trademark/patent
phrases they retain.

**Decision requested from the operator:** approve as-is, approve with edits, or reject.

<!-- graph:auto start -->
Map: [[Workflow]]
<!-- graph:auto end -->
