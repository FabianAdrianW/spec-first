# 2. The contract

`gramPromptBlock()` — [`grammar-engine.js:522`](https://github.com/FabianAdrianW/eyelingo/blob/main/grammar-engine.js#L522)

The prompt is assembled per lesson, from live learner state. It is not a static
system prompt with variables dropped in; the *structure* of the instruction
changes depending on what the learner's graph looks like at that moment.

## What gets injected

```javascript
var head='KONTRAKT GRAMATYCZNY — BEZWZGLĘDNY. '
  +'Struktury, które uczeń ZNA i których wolno używać: '
  +(allowed.length?allowed.join('; '):'BRAK — trzymaj się absolutnych podstaw')+'. ';
```

*("GRAMMAR CONTRACT — ABSOLUTE. Structures the learner KNOWS and which may be
used: … / NONE — stay on absolute basics.")*

Three things are worth pulling out of that line.

**The allowed set is enumerated, not described.** The model is handed explicit
IDs paired with names, not a CEFR level and a hope. "A1 Japanese" is an opinion;
`jp.desu = Zdanie z „desu”: X wa Y desu; jp.particle_wa = Partykuła „wa” — temat
zdania` is a set.

**The empty case has its own branch.** A brand-new learner has an empty allowed
set. Interpolating an empty list produces `may be used: .` — an instruction that
reads as permission for anything. The fallback string closes that hole.

**The label says ABSOLUTE.** That word does no mechanical work. It is there
because the sentence is also read by a human debugging a bad lesson, and the
severity of the rule should be legible in the prompt itself.

## Three shapes, not one

```javascript
var force=_noNew>=3;
var cands=gramFrontier(force?1:6).map(...);
```

- **No candidates** → the prompt instructs the model to introduce nothing new.
- **One candidate** → the structure is fixed in advance, and the burden of
  fitting it to the lesson topic shifts entirely onto the exercises.
- **Several candidates** → the model chooses from the frontier by topic fit.

`_noNew` counts portions generated without a new structure. Once it reaches 3,
the frontier is narrowed to a single candidate and the model loses the option of
declining. Without that counter the system has a stable failure mode where the
model keeps choosing "nothing new" because nothing new is always the safest
answer, and the learner stops progressing while every individual lesson looks
fine.

## Lapsed structures re-enter as retrieval

```javascript
/* SM-2 planowal powtorki struktur, ale nikt ich nie odczytywal — interwal
   mijal i nic sie nie dzialo. Struktura po terminie wraca teraz do
   materialu porcji jako WYDOBYCIE, nie jako nowe wprowadzenie. */
```

*("SM-2 scheduled structure reviews, but nobody read them — the interval elapsed
and nothing happened.")*

This is a bug comment left in place deliberately. The spaced-repetition schedule
for grammar structures existed and was being written correctly; no consumer ever
read it. The scheduler ran into a void for as long as it took to notice.

The repair is in the prompt rather than the scheduler: a lapsed structure is
injected as **retrieval**, with an explicit instruction not to re-teach it.

```javascript
head+='DO ODŚWIEŻENIA — struktura poznana wcześniej, której termin powtórki minął: '
  +_spP.id+' = '+_spP.name_pl+'. Wpleć ją w co najmniej jedno ćwiczenie tej porcji '
  +'i zadeklaruj w "uses_grammar". Nie tłumacz jej od nowa — uczeń ma ją sobie przypomnieć, '
  +'wykonując zadanie. ';
```

The pedagogical distinction is the whole point. Re-explaining a lapsed structure
destroys the retrieval opportunity that made the review worth scheduling.

## The declaration requirement

Every exercise must carry a `uses_grammar` array naming the structures it
relies on. This is what converts an unverifiable output into a verifiable one:
without it, checking compliance means parsing generated language and inferring
grammar from it. With it, the first check is a set comparison.

The declaration is not trusted — [step 3](03-the-validator.md) covers what
happens when a model declares one thing and writes another — but it is what
makes cheap checking possible at all.

---

[← The rule](01-the-rule.md) · [Next: the validator →](03-the-validator.md)
