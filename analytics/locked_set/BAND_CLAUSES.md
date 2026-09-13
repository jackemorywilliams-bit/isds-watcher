# Band clauses — `prompts/classifier.txt`, verbatim

`SCHEMA.md:65` requires a coded band to cite the `prompts/classifier.txt` clause relied on. This sheet is that file's band clauses and nothing else, so the clause can be cited without opening the prompt and without anyone retyping it.

**Transcription rule, and the certification it is offered under.** The clauses below are copied byte-for-byte from `prompts/classifier.txt`, in the order they appear in that file, under the section the file itself heads `SCORING BANDS` (lines 74-76). Each clause is reproduced inside a code fence so that no markdown rendering can alter it. The numbers are outside the fences: they are citation handles added here, not text from the prompt. **Nothing is paraphrased, summarised, abridged, reordered or re-emphasised. No emphasis is added and none is removed** — the prompt's own capitalisation is its own. Line 84 of the source file is blank and separates clause 3 from clause 4.

> **The binding limit on what these six items may be said to measure (Ruling 3(iv), 2026-09-13, binding on every seat):** six items measure grammar fidelity — the band the instrument assigns, against `L_band` — and whether any tier-S item surfaces at all. **They do not measure precision. They do not measure recall. No seat may report batch 1 as validation.** A Clopper-Pearson interval on 6/6 is [0.54, 1.00].

---

## Clause 1 — `prompts/classifier.txt` line 77

```
- HIGH (70–100): the item sits at the INTERSECTION OF ANY TWO RINGS.
```

## Clause 2 — `prompts/classifier.txt` lines 78-80

```
- MEDIUM (40–69): one ring strong + a weaker tie to another ring; OR ANY judicial-measure
  case alone (a new case challenging a domestic court judgment / denial of justice scores
  >= MEDIUM even with no other ring — Ring 2 carries extra weight).
```

## Clause 3 — `prompts/classifier.txt` lines 81-83

```
- LOW (0–39): one ring weakly, or none. Mining / oil & gas / sovereign debt / intra-EU
  energy / vanilla expropriation default to LOW UNLESS a judicial-measure or IP angle is
  present.
```

## Clause 4 — `prompts/classifier.txt` line 85

```
The two rules to remember: TWO RINGS -> HIGH. JUDICIAL-MEASURE ALONE -> at least MEDIUM.
```

---

**Verify this sheet against its source** — it is one command, and it is the only thing that makes the sheet trustworthy:

```
sed -n '74,85p' prompts/classifier.txt
```
