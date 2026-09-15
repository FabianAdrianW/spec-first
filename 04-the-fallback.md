# 4. The fallback path

Call site: [`index.html`](https://github.com/FabianAdrianW/eyelingo/blob/main/index.html), marked in code as `GRAM-3: twarda walidacja kontraktu gramatycznego`
("hard validation of the grammar contract"). The same path exists in
[`app.html`](https://github.com/FabianAdrianW/eyelingo/blob/main/app.html) for the PWA.

A validator that returns "invalid" and stops is not a feature, it is an outage.
What follows is the part that decides what the learner actually sees.

## The full sequence

```
1  prompt → server-side proxy (AI_PROXY_URL)
2  parse JSON, stripping ``` fences
3  empty result?           → retry once with a simpler, shorter prompt
4  still empty?            → hard failure
5  normalise the portion
6  validate the contract
7  violations?
     └─ drop the bad exercises
        ├─ ≥3 survive           → ship the reduced portion
        └─ <3 survive
             ├─ first failure   → ONE re-prompt naming the violated structures
             │                    → re-validate → filter again
             │                      ├─ ≥3 survive → ship it
             │                      └─ otherwise  → ship the earlier subset
             └─ already retried → ship the earlier subset
8  nothing survives?       → hard failure
```

## The decisions

**The key never reaches the client.** Every call goes to `AI_PROXY_URL`, a
server-side edge function holding the provider credential. An earlier version
returned the API key to the frontend. That is the kind of mistake that is
invisible until it is catastrophic.

**Two different retries for two different failures.** An empty or unparseable
response is a *format* failure, and the response is a simpler, shorter prompt —
less to get wrong. A contract violation is a *content* failure, and the response
is the same prompt plus a specific prohibition:

```javascript
var _p2=prompt+' POPRZEDNIA PROBA UZYLA NIEDOZWOLONYCH STRUKTUR: '+_v.reasons.join(', ')+'. Nie uzywaj ich w ogole. ';
```

*("PREVIOUS ATTEMPT USED FORBIDDEN STRUCTURES: … Do not use them at all.")*

This is why the validator returns names rather than a boolean. A retry that only
knows *that* it failed is a coin flip; a retry that knows *what* failed is a
correction.

**Degradation is preferred to retrying.** If three exercises survive, the
portion ships short. A shortened lesson is a slightly worse lesson; a second
model call is latency the learner watches, and money. Only when the portion
would be too thin to be worth doing does the system spend that call.

Three is a product judgement, not a computed optimum: below three the portion
stops feeling like a lesson.

**Exactly one retry, enforced by a flag.**

```javascript
else if(!_gramRetry){ _gramRetry=true; ... }
```

Retry-until-valid is the obvious design and the dangerous one. A model that
cannot satisfy a contract on attempt two usually cannot satisfy it on attempt
five either — most often because the contract is genuinely unsatisfiable for
that topic and that learner state. Unbounded retries turn a content bug into a
cost incident with a spinner on top.

**The retry can lose.** If the second attempt validates worse than the first,
the first attempt's surviving exercises are shipped instead:

```javascript
if(_d2.exercises.length>=3) data=_d2; else data.exercises=_keep;
```

A retry is an attempt at improvement, not an authority. Keeping `_keep` alive
across the retry is what makes it safe to try at all.

## A bug this path caused, and the fix

```javascript
// Karta „Nowa struktura" ma prawo sie pokazac WYLACZNIE wtedy, gdy
// struktura faktycznie pracuje w tej porcji. Wczesniej _teachable
// ustawialo sie bezwarunkowo i uczen dostawal regule bez zwiazku
// z lekcja — kategoria „Do widzenia" plus przypadkowa gramatyka.
var _uzyta=false;
try{ _uzyta=!!_tid && (data.exercises||[]).some(function(_x){
  return [].concat((_x&&_x.uses_grammar)||[]).indexOf(_tid)>=0; }); }catch(e){}
try{ if(_uzyta) gramMarkTaught(_tid); }catch(e){}
```

*("The 'New structure' card may appear ONLY when the structure actually works in
this portion. Previously `_teachable` was set unconditionally and the learner
got a rule unrelated to the lesson — a 'Goodbyes' category plus random
grammar.")*

The system used to mark a structure as taught because it had been *selected*,
not because it had been *used*. The filtering step above makes those two facts
diverge: the exercise carrying the new structure can be exactly the one the
validator discards. The structure was then recorded as taught, its
prerequisites unlocked downstream, and the learner was shown a grammar card for
something the lesson never contained.

The fix reads the actual shipped exercises and marks the structure taught only
if it survived. Two consequences follow from getting this right: the graph
stays honest, and the learner stops receiving explanations for grammar they did
not meet.

This is the class of bug that only appears once validation and state-writing
coexist — and the reason I treat "what does the system believe happened" as a
separate question from "what did the model return".

---

[← The validator](03-the-validator.md) · [Next: limits →](05-limits.md)
