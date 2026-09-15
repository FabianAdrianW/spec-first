# 6. Spec vs shipped

Everything so far is a rule that made it into code. This page is a rule that did
not, because a repository about specification discipline that only shows the
specifications which succeeded is advertising, not evidence.

## The clause

In July 2026 I specified layered script display for non-Latin writing systems.
The problem is real: showing a beginner only 日本語 blocks them completely,
while showing only *nihongo* forever builds permanent dependence on the crutch
and they never enter the target script.

The specification defines three modes, written into two governing documents:

| Mode | Shows | For |
|---|---|---|
| `SCRIPT_ORIGINAL` | native script only | higher bands |
| `SCRIPT_PAIRED` | native **+** transliteration together, furigana-style | middle bands |
| `SCRIPT_TRANSLIT` | transliteration only | absolute beginners |

With numbered normative clauses:

- **PB-SCRIPT-01** — default mode derived from the learner's band at onboarding;
  user may override.
- **PB-SCRIPT-02** — fading: as the band rises the system nudges
  `TRANSLIT → PAIRED → ORIGINAL`.
- **PB-SCRIPT-03** — transliteration is configurable per language, not
  hardcoded: Hepburn for Japanese, pinyin **with tone marks** for Chinese
  (untoned pinyin is near-useless and this is a hard requirement), Revised
  Romanization for Korean.
- **DB-SCRIPT-01** — TTS always pronounces the **original** form regardless of
  display mode. Never speak from transliteration.
- **DB-SCRIPT-02** — highlight markers must work on both forms; matching runs on
  the original lemma and maps onto the displayed surface form.
- **DB-SCRIPT-03** — modes are gated by a language property; for Latin-script
  languages they collapse to `SCRIPT_ORIGINAL` and the setting is hidden.

## What actually shipped

Grep the public repository:

| Symbol | `index.html` | `app.html` |
|---|---|---|
| `SCRIPT_ORIGINAL` | 0 | 0 |
| `SCRIPT_PAIRED` | 0 | 0 |
| `SCRIPT_TRANSLIT` | 0 | 0 |
| `nonLatinScript` | 0 | 0 |

What ships is a **binary toggle**: `_lexScript === 'romaji'`, a button reading
*"Pismo: transliteracja ↔ oryginalne"*, taking effect from the next portion.

So of six clauses: the per-language transliteration systems (PB-SCRIPT-03) exist
in a language configuration map, and TTS reading the original (DB-SCRIPT-01)
holds. The band-derived default, the fading progression, the paired mode and
the language-property gating do not exist. The middle mode — the one the
specification itself identifies as pedagogically strongest, because the learner
attempts the script and uses transliteration for self-correction — is the one
that was never built.

## Why it is still open

The binary toggle solves the blocking problem: a beginner is not locked out.
It does not solve the dependence problem, which is slower, less visible, and
only shows up in learners who have been using the product for months.

Ranked against work that had a live failure attached to it — the grammar
contract in this repository being one — a second-order pedagogical improvement
for the subset of learners studying a non-Latin language did not win. That was a
priority decision, and I would make it again. It was not an oversight, and the
clause has not been quietly dropped.

## Why this page exists at all

I could have written this repository about the script modes. The specification
is more elegant than the grammar contract and reads better. I chose the grammar
contract because it is the one you can verify.

That choice is the method. A specification is a claim about the future; only
code is a claim about the present, and the two drift unless somebody checks.
This page is the check, published rather than filed.

If a specification has never diverged from its implementation anywhere in a
system, one of three things is true: the system is trivial, the specifications
were written afterwards, or nobody has looked.

---

[← Limits](05-limits.md) · [README](README.md)
