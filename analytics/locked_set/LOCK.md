# LOCK — the locked validation set, batch 1

This file is the evidence that the set's contents did not move after they were
written down. `scripts/check_lock.py` recomputes each hash below against the
file on disk and fails closed on any disagreement.

The commit order at `SCHEMA.md:14-20` exists so that blindness is **provable
rather than promised**: item content is committed first and hashed here, and
only then may labels be written, in a separate file, with their own entry
appended below. Git history is what proves the order; that is why each entry
carries the commit that recorded the file, and why this file is extended and
never rewritten.

## Step 2 — `items.json`

Recorded 2026-09-13 under Ruling 3(i) of the council's rulings session of that
date. The hash is over the file's **bytes** as committed, not over re-serialised
JSON.

| File | SHA-256 | Commit |
|---|---|---|
| `items.json` | `90fc9c07b6bf834481b5bf39e4a4bcf4fa4b6d75e0731166a38222160e5f6f56` | `5c2407721cf57cd0514116c6cbc0f88c8764fdf0` |

Verify:

```
shasum -a 256 analytics/locked_set/items.json
git log --format='%H %s' -1 5c2407721cf57cd0514116c6cbc0f88c8764fdf0
python3 scripts/check_lock.py
```

## Steps 3 and 4 — not yet taken, and that is the designed state

Nothing is locked here but item content, because nothing else exists yet. Under
Ruling 3(ii) the coding is reserved to the operator: the set's validity rests on
a single coder whose judgment is independent of the classifier's model family,
and a seat that coded the labels would convert the only independent measurement
this instrument will ever get into model-to-model agreement. **No seat has
authored, proposed, pre-filled or suggested a label, a score or a band for any
item in `items.json`, in any field, comment or report.**

Step 3 commits the labels, in their own file. Step 4 appends that file's hash
below this entry — it does not touch the entry above. Only after step 4 may any
scorer be run against the set.

## What this file cannot tell you

It cannot tell you the labels are right; that is a human question. It cannot by
itself tell you the entry above was written before the labels rather than after
— `git log` answers that, which is why the commit SHA is recorded and printed.

And it says nothing about what six items are worth. Per Ruling 3(iv), binding on
every seat: **six items measure grammar fidelity and whether any tier-S item
surfaces at all. They are not precision, they are not recall, and no seat may
report batch 1 as validation** — a Clopper-Pearson interval on 6/6 is
[0.54, 1.00].
