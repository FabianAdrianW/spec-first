# 5. Limits

Every number on this page is produced by [`verify.py`](verify.py) against the
live grammar banks. Run it and disagree with me if it disagrees with me.

## The sieve has a blind spot, and it is measurable

`sieveHit()` skips any exponent shorter than the length guard:

```javascript
if(e.length < (e.indexOf(' ')>0 ? 5 : 6)) continue;
```

Single-word exponents under 6 characters and multi-word ones under 5 are never
tested. The guard exists because short exponents match inside unrelated words
and produce false rejections at a rate that makes the validator useless — but
the cost is real:

```
points with sieve:true        293 / 578
of those, reachable by sieve  254 / 293   (86%)
never tested                   39
```

**39 grammar points carry `sieve: true` and are never actually scanned.** Their
exponents all sit below the guard. The flag is set, the intent is recorded, and
the check silently does nothing.

This hits inflected languages hardest, because their exponents are short
suffixes. Coverage by language:

| Language | Reachable | Language | Reachable |
|---|---|---|---|
| ar, en, jp, ko, nl, no, pt, ru, uk, zh | 100% | de | 76% |
| es | 70% | fr | 66% |
| it | 63% | | |

Romance languages lose the most: the Italian and French exponents that mark
tense and agreement are frequently 3–4 characters.

**What actually protects those 39 points** is the declaration check, which has
no length guard. The sieve is the second line, not the only one — but for these
points there is effectively one line of defence, and a model that declares
dishonestly gets through.

**Why it is not fixed by lowering the guard:** the false-positive rate is the
binding constraint. A word-boundary regex helps for space-delimited languages
and does nothing for Japanese or Chinese. The honest fix is per-language
thresholds with per-language tokenisation, which is a larger piece of work than
it looks and is not done.

## Two stated conventions that the data does not obey

The grammar bank has written authoring conventions. Two of them do not hold:

```
examples per point:  {2: 577, 3: 1}
  convention says exactly 3  →  577/578 deviate

paradigm rows:       {2: 8, 3: 87, 4: 338, 5: 80, 6: 52, 7: 9, 8: 4}
  convention says 4–6        →  108/578 outside range
```

The "exactly 3 examples" rule is effectively fictional — one point in 578
follows it. The paradigm-row rule holds for 81% of points.

I am including this because it is the most useful thing on the page. A
specification that is never checked degrades into decoration, and these two
degraded without anyone noticing, including me, until this script was written.
The rules that *are* enforced by code — the prerequisite graph, the allowed-set
check — hold at 100%. The rules enforced only by intention hold at 0.2% and 81%.

That is the actual lesson: **a rule is worth exactly as much as the check that
enforces it.** The validator in this repository is not evidence that I write
good rules. It is evidence of the difference between a rule with a check and a
rule without one.

## Other bounds

**Coverage.** B1 exists for English only (20 points). Everything else is A1 +
A2. The machinery is level-agnostic; the content is not there yet.

**Exponent script.** For Arabic, Japanese, Korean and Chinese the convention
requires Latin transliteration, and it holds exactly — 0 native-script exponents
across all four. Russian and Ukrainian use Cyrillic exponents (83 each), which
is consistent with the convention as written, since it names only the other
four. The same reasoning arguably applies to Cyrillic and the convention should
be widened; it has not been.

**Level headroom.** The sieve scans structures at most one CEFR level above the
learner. Overreach by two or more levels is not caught by the sieve, only by the
declaration check.

**No offline eval suite.** There is no fixture set of recorded model outputs
scored in CI. Validation is a runtime guard, not a regression test. Failure
rates in production are not currently logged in a form I can quote, so this
repository quotes no accuracy figure — I would rather publish the gap than a
number I cannot source.

---

[← The fallback path](04-the-fallback.md) · [Next: spec vs shipped →](06-spec-vs-shipped.md)
