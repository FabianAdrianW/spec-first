# 1. The rule

> A lesson must never require a grammatical structure the learner has not been
> taught.

## Why a graph and not a list

The obvious implementation is an ordered list: teach structure 1, then 2, then
3. It is wrong, and it was my first version.

Grammar dependency is a **partial order**, not a queue. In Japanese, the
question particle *ka* requires *desu*; the *-te* form does not. Both become
available the moment their own prerequisites are met, and which one a lesson
should use depends on what the lesson is *about*. Flattening the graph into a
single path by an `order` field produced lessons that were technically legal and
thematically absurd — a lesson on greetings taught the past tense because it was
next in line.

The fix is recorded in the code itself, above the frontier function:

> *"The frontier is ALL points ready to be introduced. The prereq graph is a
> PARTIAL order, not a queue — the choice within the frontier cannot break
> GRAM-0, but it does allow the structure to be matched to the portion's topic.
> The previous version flattened the graph into a single path by `order` and
> ignored the lesson topic."*
>
> — [`grammar-engine.js:188`](https://github.com/FabianAdrianW/eyelingo/blob/main/grammar-engine.js#L188)

## The three states that matter

`gramAllowed()` — [`grammar-engine.js:183`](https://github.com/FabianAdrianW/eyelingo/blob/main/grammar-engine.js#L183) — returns every structure the learner may encounter:

```javascript
window.gramAllowed=function(){
  var out=[]; bank().list.forEach(function(p){
    var s=gramStatus(p.id); if(s==='unlocked'||s==='stale'||s==='presumed') out.push(p.id);
  }); return out;
};
```

- **`unlocked`** — explicitly taught in a previous lesson.
- **`stale`** — taught, but its SM-2 review interval has elapsed. Still allowed,
  because the point of a lapsed structure is to *retrieve* it, not to relearn it.
- **`presumed`** — assumed known from the onboarding placement, not from a
  lesson. A beginner at B1 does not get taught *ser* vs *estar* from zero.

`gramFrontier()` — [`grammar-engine.js:192`](https://github.com/FabianAdrianW/eyelingo/blob/main/grammar-engine.js#L192) — returns everything currently
**teachable**: prerequisites satisfied, not yet taught. The lesson generator
picks from the frontier by topic fit, which is legal precisely because every
member of the frontier is legal.

## The bank

The rule is only as good as the graph underneath it. Current state, regenerated
by [`verify.py`](verify.py):

```
578 grammar points across 14 languages
  A1: 278   A2: 280   B1: 20
601 prerequisite references
  0 broken
578/578 points carry a calibrated SM-2 initial_ease
```

Zero broken references is not a boast, it is a precondition. A single dangling
`prereq` would make some structure permanently unteachable — it would sit
forever waiting on a prerequisite that cannot be satisfied, and no user-facing
symptom would ever point at the cause. The check runs before any bank ships.

## Scope, honestly

B1 exists for English only (20 points). Every other language is A1 + A2. The
graph is complete and valid for what it covers; it does not yet cover B2–C2.

Data: [`data/grammar/`](https://github.com/FabianAdrianW/eyelingo/tree/main/data/grammar) in the Eyelingo repository.

---

[← README](README.md) · [Next: the prompt contract →](02-the-prompt.md)
