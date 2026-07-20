# Ring 3 reconciliation — the council's response to the external audit

**Convened by:** the chairman of the ISDS research council
**Author:** methodology analyst
**Date:** 2026-06-29
**Status:** decision note — read-only analysis of existing artifacts; the only change it proposes is a prose fix to METHODOLOGY.md (Part II.C, the "Ring three" paragraph) and a parallel one-line fix to PLAN.md. No scoring artifact changes.

---

## 1. The discrepancy, stated precisely

METHODOLOGY.md Part II.C justifies Ring 3 partly on this sentence:

> "All three seed tribunals have a procedural commonality: none of the tribunals ever reached the merits of the public interest issues presented in their respective disputes — all three were dismissed before reaching merits because jurisdiction and/or admissibility barred the way."

The external audit is **correct that this is false as a statement of the seed dispositions.** Only one of the three seeds was disposed of on jurisdiction/admissibility. The verified dispositions:

- **Philip Morris Asia Ltd v. Australia**, PCA Case No. 2012-12, Award on Jurisdiction and Admissibility (17 Dec 2015): claims held **inadmissible** for abuse of rights (restructuring into a Hong Kong entity once a dispute over plain packaging was reasonably foreseeable); the tribunal **declined to exercise jurisdiction**. This *is* a jurisdiction/admissibility disposition.
- **Eli Lilly & Co. v. Canada**, ICSID Case No. UNCT/14/2, Final Award (16 Mar 2017): all claims dismissed **on the merits** — the claimant "failed to establish the factual premise of its case" (the promise/utility-doctrine NAFTA 1105 claim). This is a **merits** disposition, not jurisdiction/admissibility.
- **Bridgestone Licensing Services, Inc. & Bridgestone Americas, Inc. v. Panama**, ICSID Case No. ARB/16/34: at the Decision on Expedited Objections (13 Dec 2017) the tribunal **upheld jurisdiction** — BSAM's licence to use the FIRESTONE mark, and BSLS's ownership of the mark, each constituted a "covered investment" under the US–Panama TPA and the ICSID Convention — and at the Award (14 Aug 2020) the denial-of-justice claim **failed on the merits**: the tribunal found some errors in the Panamanian Supreme Court's judgment but held they did not meet the high threshold for a denial of justice. The **final disposition is merits-based**, though a live and partly dispositive jurisdiction/standing/"covered investment" question ran through the case.

So the true scorecard is: **one** jurisdiction/admissibility disposition (Philip Morris), **two** merits dispositions (Eli Lilly; Bridgestone), with Bridgestone additionally carrying a serious Ring-3 jurisdictional fight that it won at the threshold and then lost the case on the merits.

**Sources (all confirmed for this note):**

- Philip Morris v. Australia — abuse of rights, claims inadmissible, jurisdiction declined: IISD/ITN, "Corporate restructuring and abuse of rights: PCA tribunal deems Philip Morris's claims … inadmissible," https://www.iisd.org/itn/2016/08/10/philip-morris-asia-limited-v-the-commonwealth-of-australia-pca-case-no-2012-12/ ; award on jusmundi, https://jusmundi.com/en/document/decision/en-philip-morris-asia-limited-v-the-commonwealth-of-australia-award-on-jurisdiction-and-admissibility-thursday-17th-december-2015 ; italaw docket, https://www.italaw.com/cases/851 ; UNCTAD ISDS Navigator, https://investmentpolicy.unctad.org/investment-dispute-settlement/cases/421/philip-morris-v-australia
- Eli Lilly v. Canada — all claims dismissed on the merits ("failed to establish the factual premise"): Lexology, "ICSID Tribunal dismisses Eli Lilly's NAFTA claim against Canada," https://www.lexology.com/library/detail.aspx?g=17077fd1-0a24-4647-9c6f-21ffb23e004d ; italaw docket, https://www.italaw.com/cases/1625 ; UNCTAD ISDS Navigator, https://investmentpolicy.unctad.org/investment-dispute-settlement/cases/507/eli-lilly-v-canada
- Bridgestone v. Panama — jurisdiction upheld at Expedited Objections (licence/mark a covered investment), denial of justice rejected on the merits at the Award: IISD/ITN, "ICSID tribunal rejects denial of justice claim against the Republic of Panama," https://www.iisd.org/itn/2020/12/19/icsid-tribunal-rejects-denial-of-justice-claim-against-the-republic-of-panama/ ; Award on jusmundi, https://jusmundi.com/en/document/decision/en-bridgestone-americas-inc-and-bridgestone-licensing-services-inc-v-republic-of-panama-final-award-friday-14th-august-2020 ; Decision on Expedited Objections (13 Dec 2017), http://icsidfiles.worldbank.org/icsid/icsidblobs/OnlineAwards/C5946/DS10865_En.pdf ; italaw docket, https://www.italaw.com/cases/4475 ; UNCTAD ISDS Navigator, https://investmentpolicy.unctad.org/investment-dispute-settlement/cases/750/bridgestone-v-panama

---

## 2. The question put to the council

Does the correction undermine the three-ring **scoring system** and the HIGH/MEDIUM/LOW **relevance bands** — or only the **narrative justification**? What is the minimal reconciliation that keeps the project's basis intact?

**Bottom line up front:** the false claim is confined to the *narrative justification* of Ring 3 in METHODOLOGY.md Part II.C (echoed in one line of PLAN.md). **Nothing in the actual scoring depends on it.** No weight, no band threshold, no trigger, and no combination rule in `fingerprint.yaml` or `src/classify.py` references the disposition of the seeds at all. The minimal reconciliation is a **prose fix only**. The corrected prose is, if anything, a *stronger* justification, because it grounds Ring 3 in the doctrinal *vocabulary* the seeds actually contributed rather than in a disposition they do not all share — and the dimension it names is the one the project's own research question is built around. The holdout already provides empirical support for keeping the dimension, and it does so independently of any narrative about dispositions.

I take the five examination points in turn.

---

## 3. Point-by-point analysis

### Point 1 — Does Ring 3 earn its place as a doctrinal *dimension*, even though only one seed was *dismissed* on it?

**Yes, decisively, and on grounds that have nothing to do with "the common disposition."**

The error in the original prose is a category mistake: it justified a *dimension of the fingerprint* (what doctrines a case engages) by appeal to a *disposition statistic* (how the seed cases ended). Those are different things. A thematic fingerprint indexes the **doctrinal language a case engages**, not the **outcome** the tribunal reached. The instrument is explicitly lexical-thematic, not outcome-predictive: METHODOLOGY.md Part II.A says "the methodological issue here is interpretative and not lexical," and the index unit is "the arbitrators' own language — the operative phrases were taken directly from the awards." The disposition of a case is not in the fingerprint and is not scored.

What Ring 3 actually encodes is visible in `fingerprint.yaml` (the `jurisdictional_admissibility` ring) and in PLAN.md's per-ring extraction. Every substantive Ring-3 trigger is drawn verbatim from **Philip Morris and Bridgestone** — not from a disposition, but from the **doctrinal questions those cases litigated**:

- From Philip Morris: `abuse of right` (w12), `abuse of process` (w9), `treaty shopping` (w9), `corporate restructuring` (w8), `restructure its investment to gain Treaty protection` (w8), `reasonably foreseeable` (w7), `pre-existing or reasonably foreseeable dispute` (w7), `critical date` (w6), `treaty protection` (w5).
- From Bridgestone: `shell subsidiary` (w6), `definition of investor` (w5), `standing of licensor vs licensee` (w4), `standing to claim denial of justice when not a party` (w4), `abusive tactics` (w4), `exhaustion of local remedies` (w3).
- Theme extensions (small weights): `denial of benefits` (w2), `substantial business activities` (w1).

The salience test for a *dimension* is whether the doctrine is recurring and live across the seed corpus — not whether it was the disposition in every case. On that test Ring 3 is plainly earned:

- It was **dispositive** in Philip Morris (abuse of right → inadmissibility).
- It was a **live, litigated, and partly dispositive** question in Bridgestone — the standing of the licensor (BSLS) versus the licensee (BSAM), the shell-subsidiary allegation, and whether the licence/mark was a "covered investment" were fought at the Expedited Objections phase and resolved there (jurisdiction upheld). That this jurisdictional fight ended in the claimant's favour at the threshold, and the case was then lost on the merits, does not make the jurisdictional dimension absent — it makes Bridgestone a case where Ring 3 was *engaged and contested*, which is exactly what a thematic index should capture.
- It is the **explicit subject of the research question.** METHODOLOGY.md Part I frames the project around the case in which "a rule of law is applied at the jurisdictional/admissibility level that determines that the case cannot proceed." Removing Ring 3 would amputate one of the three doctrines the project was convened to watch. The dimension is the research question, not an artifact of how three awards happened to end.

So Ring 3's place rests on **doctrinal salience and recurrence** (dispositive in one seed, live in a second, central to the research question), which the corrected facts fully support. It never rested on the "all three were dismissed on jurisdiction" claim — that claim was a rhetorical over-reach bolted onto an independently sound dimension.

### Point 2 — Does Ring 2's weighting depend on the false claim?

**No.** Ring 2's extra weight depends on a fact the audit leaves **entirely intact**: two of the three seeds (Eli Lilly, Bridgestone) are judicial-measure / denial-of-justice cases.

This is encoded as `extra_weight: true` on the `judicial_or_regulatory_measure` ring (`fingerprint.yaml` line 49) and implemented in `src/classify.py` via `EXTRA_WEIGHT_RING` and the single-ring promotion branch (the `only == EXTRA_WEIGHT_RING` clause, scoring to ≥ MEDIUM). The justification in METHODOLOGY.md Part II.C for Ring 2 is the *prevalence* of the judicial-measure pattern in the corpus ("two of them were brought against domestic courts," "the seed corpus emphasizes this ring significantly") — and PLAN.md states the rationale as "EXTRA WEIGHT: 2/3 seeds are judicial-measure cases."

Both Eli Lilly (NAFTA 1105 denial-of-justice framing against the promise/utility doctrine, a judicial measure) and Bridgestone (denial of justice against the Panamanian Supreme Court judgment) remain judicial-measure cases after the correction. The audit corrected the *disposition* of those two cases (merits, not jurisdiction), which is a Ring-3 fact, not a Ring-2 fact. Ring 2's weighting is therefore untouched. Indeed, the correction *reinforces* Ring 2: the two judicial-measure seeds were litigated **to the merits on the denial-of-justice question** (Eli Lilly's 1105 claim assessed and rejected on the facts; Bridgestone's denial-of-justice claim assessed and rejected on the merits), which is if anything a fuller engagement of the Ring-2 doctrine than a threshold dismissal would have been.

### Point 3 — Do the relevance bands depend on the false claim?

**No.** The bands (HIGH ≥ 70, MEDIUM 40–69, LOW < 40) and the digest threshold (40) are calibrated empirically, against the **score distribution the deterministic scorer produces**, not against any narrative about seed dispositions. METHODOLOGY.md Part VI.A states the basis explicitly: off-theme texts cluster at 0–8, on-theme texts at 40–75, with an empty band between; "the threshold of forty therefore sits at the floor of the on-theme cluster," and the ring-present floor of twelve "sits in the dead band well above the off-theme noise." `fingerprint.yaml` lines 5–9 set `threshold: 40`, `high: 70`, `medium: 40`, `low: 0`; the calibration constants `PRESENT_FLOOR = 12` and `STRONG_SUBTOTAL = 18` live in `src/classify.py`.

None of these numbers is derived from, or sensitive to, whether the seeds were dismissed on jurisdiction or on the merits. They are derived from the separation between on-theme and off-theme score clusters. The false claim could be deleted in full and every band threshold would be unchanged and unjustified by it either way.

### Point 4 — Does anything in the actual scoring need to change?

**No.** I inspected the full scoring surface:

- `fingerprint.yaml`: ring weights (each ring sums to 100), the three rings' keyword triggers, `threshold`, `scoring` bands, `combination_rules`, `negative_signals`, and the seven `few_shot_examples` with their expected bands.
- `src/classify.py`: `keyword_score()` (the deterministic scorer), `PRESENT_FLOOR`, `STRONG_SUBTOTAL`, `EXTRA_WEIGHT_RING`, the combination logic, and negative-signal handling.
- `src/config.py`: `threshold`, `MIN_DIGEST_ITEMS`, `RELEVANCE_FLOOR`.

**Not one line references the disposition of the seed cases.** The scorer keys on the presence and weight of doctrinal phrases in candidate text. The seeds enter the system only through the *vocabulary they contributed* (the `seed:` tags on each keyword), and those tags are attributions of *where a phrase came from*, not claims about *how a case ended*. The false sentence in METHODOLOGY.md is a justification narrative with **no downstream representation in code or data**.

Therefore the minimal reconciliation is a **prose fix only**. I considered, and reject, three candidate scoring changes:

1. *"Down-weight Ring 3 because only one seed was dismissed on it."* Rejected. Ring weights are not disposition-counts; all three rings already carry equal `weight: 100` and the band logic turns on intersection and per-ring subtotals, not on a per-ring disposition tally. Ring 3's internal weights are calibrated so that Philip Morris and Bridgestone score on their own text, which they do; the holdout's Philip Morris v. Uruguay item (score 73) exercises the Ring-1/Ring-2 intersection, and the seeds exercise Ring 3 directly. There is no calibration evidence that Ring 3 is over-weighted.
2. *"Remove Ring 3's extra-weight promotion."* Rejected as moot — Ring 3 has `extra_weight: false` already (`fingerprint.yaml` line 72). Only Ring 2 carries extra weight, and Point 2 shows that is correctly justified. The false claim never produced a Ring-3 scoring privilege to retract.
3. *"Add a Ring-3 disposition trigger."* Rejected. The instrument is thematic, not outcome-predictive; adding a disposition trigger would change its character and is unsupported by any audit finding.

The single honest caveat already lives in the system and should not be papered over: the holdout's lone false negative, **Apotex Holdings v. United States**, is precisely a case decided on a Ring-3 disposition — the tribunal held the claimant's FDA/regulatory rights were *not* a covered investment and disposed of the case "on the definition of investor and jurisdiction." The deterministic scorer under-detects cases that hinge on a *negative* jurisdictional finding (non-investment). This is already documented in METHODOLOGY.md Part VI.B and Part IX, and it is a known limitation of the lexical stage (which the LLM stage exists to mitigate), **not** a reason to change a weight. It is worth noting for candor that the dimension the audit questioned is the same dimension on which the scorer has its one acknowledged miss — but the response to that is the documented two-stage design, not a re-weighting.

### Point 5 — How does the backtest empirically test that the fingerprint generalizes independent of the narrative?

There is **no `scripts/backtest.py` or `scripts/site_templates/backtest.html.j2` in the repository** outside agent worktrees; that artifact named in the brief does not yet exist on this branch. The empirical out-of-sample test that *does* exist, and that performs the function the brief describes, is `scripts/eval_holdout.py` over `scripts/holdout_set.json`. I ran it for this note; it reproduces the figures in METHODOLOGY.md Part VI.B exactly:

```
Holdout: 20 items (4 on-theme, 16 off-theme) | threshold = 40
  ok label=1 score= 56 pred=1  loewen_v_us
  ok label=1 score= 62 pred=1  mondev_v_us
  X  label=1 score=  8 pred=0  apotex_v_us
  ok label=1 score= 73 pred=1  pm_v_uruguay
  ... (16 off-theme items, all score 0, all correctly rejected) ...
Confusion: TP=3 FP=0 TN=16 FN=1
Precision=1.00  Recall=0.75  Accuracy=0.95  F1=0.86
```

This is exactly the evidence that decouples the fingerprint's validity from the disposition narrative, in three respects:

1. **It tests vocabulary, not dispositions.** The holdout scores four on-theme awards that played no part in development (Loewen, Mondev, Apotex, Philip Morris v. Uruguay) on their own distinct language, against sixteen real off-theme listings. Three of four unseen on-theme awards are flagged; all sixteen off-theme items are rejected. That generalization is a property of the *doctrinal vocabulary* the fingerprint encodes, and is established without reference to how any seed case ended.

2. **A merits-disposed on-theme case scores HIGH.** Philip Morris **Brands** v. **Uruguay** scores **73** (HIGH) in the holdout — and its disposition was a **merits** outcome: the plain-packaging measures were upheld and the denial-of-justice claim was rejected on the merits. A case that ended on the merits nonetheless registers at the top of the on-theme band, because it *engages* the Ring-1 (covered investment / trademark) and Ring-2 (regulatory measure / denial of justice) doctrines. This is direct empirical proof that the instrument keys on doctrinal engagement, not on a jurisdiction/admissibility disposition. The original narrative's premise ("relevance flows from being dismissed on jurisdiction") is falsified by the instrument's own out-of-sample behaviour.

3. **The one jurisdiction-disposed holdout case is the miss.** Apotex — the holdout item actually decided on a Ring-3 *disposition* (non-investment / definition of investor / jurisdiction) — is the single false negative. So even within the out-of-sample test, "disposed of on jurisdiction" does not track "scores high"; if anything the lexical scorer is *weakest* on the negative-jurisdictional-finding pattern. This further severs the link between the disposition narrative and the scoring, and corroborates the documented limitation rather than contradicting it.

The holdout therefore confirms the corrected position: the fingerprint generalizes as a *thematic-doctrinal* index, and its band behaviour is independent of, and in one case directly contrary to, the false "all three dismissed on jurisdiction" narrative. The holdout is small and NAFTA/ICSID-skewed (stated plainly in Part IX), but its design is exactly the right empirical control for this audit question.

---

## 4. The council's position and the minimal reconciliation

**Position.** The audit is correct on the facts and the correction is material to candor, but it touches only the **narrative justification** of Ring 3. The **scoring system, the bands, the triggers, the weights, the combination rules, and the threshold all stand unchanged**, because none of them was ever derived from the false claim. Ring 3 is a sound doctrinal dimension on independent grounds (dispositive in Philip Morris, live and contested in Bridgestone, central to the research question), and the out-of-sample holdout empirically confirms that the fingerprint keys on doctrinal engagement rather than on case disposition — including a HIGH-scoring merits case (Philip Morris v. Uruguay) and a missed jurisdiction-disposed case (Apotex). The minimal reconciliation is a **prose correction**, not a scoring change.

**Concrete scoring change warranted:** **none.** No edit to `fingerprint.yaml`, `src/classify.py`, or `src/config.py` is justified by the audit. (For the record: the relevant lines I checked and am affirmatively *not* changing are `fingerprint.yaml` line 5 `threshold: 40`, lines 6–9 the band map, line 49 Ring-2 `extra_weight: true`, line 72 Ring-3 `extra_weight: false`, lines 70–91 the Ring-3 triggers and weights, and lines 93–99 the combination rules; and `src/classify.py` `PRESENT_FLOOR = 12`, `STRONG_SUBTOTAL = 18`, `EXTRA_WEIGHT_RING`.)

**Prose fix warranted:** two locations.

1. **METHODOLOGY.md, Part II.C, the "Ring three" paragraph.** Replace the false disposition claim with a justification grounded in doctrinal salience and the corrected dispositions. Recommended replacement language for the council to adopt (the principal/author to finalize wording and citations):

   > Ring three — jurisdictional and admissibility doctrines as the gateway the case must pass. This ring indexes the threshold doctrines — abuse of right, treaty-shopping, corporate restructuring, the critical date, shell-subsidiary and standing questions, and the definition of a covered investor/investment — that determine whether a tribunal will hear an IP-as-investment, judicial-measure claim at all. The dimension is salient and recurring across the seed corpus rather than a shared disposition: in Philip Morris Asia v. Australia it was dispositive, the tribunal holding the claims inadmissible for abuse of right after the claimant restructured into a treaty state once a dispute over plain packaging was reasonably foreseeable; in Bridgestone v. Panama it was a live and contested threshold fight — the licensor/licensee standing split, the shell-subsidiary allegation, and whether the trademark licence was a "covered investment" — which the tribunal resolved in the claimant's favour at the Decision on Expedited Objections before the case was decided on the merits. (Eli Lilly v. Canada, by contrast, was dismissed on the merits, and Bridgestone's denial-of-justice claim likewise failed on the merits; the seeds therefore do not share a common disposition, and the instrument does not score for one — it is a thematic index of the doctrines a case engages, not a predictor of how a case will end.) The synthesis controlling this ring is Baumgartner, Treaty Shopping in International Investment Law (2016), drawing on the abuse-of-right principle (Byers, 2002) and the treatise standards (Dolzer & Schreuer, 2012; McLachlan et al., 2017). Triggers for ring three include: abuse of right; reasonably foreseeable; critical date; shell subsidiary.

   The decisive moves in this replacement are: (a) it justifies the *dimension* by doctrinal salience and recurrence, not by disposition; (b) it states the **true** dispositions of all three seeds, pre-empting the audit; (c) it makes explicit the conceptual correction — the instrument is a thematic doctrinal index, not an outcome predictor — which is consistent with Part II.A and Part VI.A; and (d) it keeps the same trigger list, which is correct and unchanged.

2. **PLAN.md, Ring 3 heading / scoring-model note.** The PLAN.md per-ring extraction (the `### Ring 3` block) is already correct — it lists only the doctrinal vocabulary and never asserts a common disposition — so it needs no change. The one line to verify and, if it overstates, align is the Ring-3 description; as written it is sound. No change is required to PLAN.md's scoring model (HIGH/MEDIUM/LOW), which restates the bands accurately.

**Guidance for keeping the new prose defensible.** (i) Never justify a *fingerprint dimension* by a *disposition statistic* again — justify it by doctrinal salience, recurrence across seeds, and fit to the research question. (ii) State the true dispositions wherever the seeds' outcomes are characterized (one jurisdiction/admissibility dismissal: Philip Morris; two merits dispositions: Eli Lilly and Bridgestone; with Bridgestone carrying a contested but claimant-favourable jurisdictional threshold). (iii) Anchor the claim that the fingerprint is thematic-not-predictive to the existing artifacts: Part II.A (interpretive index of the arbitrators' own language), Part VI.A (bands calibrated on the score distribution), and the holdout's HIGH-scoring merits case (Philip Morris v. Uruguay) and jurisdiction-disposed miss (Apotex). (iv) Retain the existing candor about the Apotex/non-investment under-detection (Parts VI.B and IX) — it is the honest counterpart to keeping Ring 3, and it should be cited, not hidden, in any defense of the dimension.

**How the backtest confirms it.** Running `scripts/eval_holdout.py` on the unchanged scorer yields precision 1.00, recall 0.75, accuracy 0.95, F1 0.86 over a 20-item out-of-sample set built from awards the instrument never saw. Because the prose fix changes no weight, threshold, or trigger, these figures are unchanged by the reconciliation — which is the point: the correction is purely narrative, and the empirical performance that grounds the project's basis is undisturbed. The holdout independently demonstrates (via the HIGH-scoring merits case and the missed jurisdiction-disposed case) that scoring tracks doctrinal engagement, not disposition, exactly as the corrected prose now says.

---

## 5. One-paragraph bottom line

The audit is right, and the fix is small. The false "all three dismissed on jurisdiction" sentence is a justification over-reach in METHODOLOGY.md Part II.C with **no representation anywhere in the scoring** — not in `fingerprint.yaml`'s weights, bands, triggers, or combination rules, and not in `src/classify.py`. Ring 3 earns its place as a doctrinal dimension on independent and now-corrected grounds (dispositive in Philip Morris; a live, contested threshold question in Bridgestone; the explicit subject of the research question), and the out-of-sample holdout confirms the fingerprint keys on doctrines engaged rather than on dispositions — a merits case (Philip Morris v. Uruguay) scores HIGH, and the one jurisdiction-disposed case (Apotex) is the scorer's only miss. The minimal, sufficient reconciliation is to correct the prose of the Ring-3 justification to state the true dispositions and to recast the rationale as doctrinal salience, with **no change to any weight, band, threshold, or trigger.** Honesty preserved; basis intact.

<!-- graph:auto start -->
Map: [[Research Question]]
<!-- graph:auto end -->
