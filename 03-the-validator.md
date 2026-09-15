# 3. The validator

`gramValidatePortion()` — [`grammar-engine.js:658`](https://github.com/FabianAdrianW/eyelingo/blob/main/grammar-engine.js#L658)

The prompt asked. This decides.

```javascript
window.gramValidatePortion=function(data,teachableId){
  if(!gramBankReady()||!data) return {bad:[],reasons:[]};
  var ok={}; gramAllowed().forEach(function(id){ ok[id]=1; }); if(teachableId) ok[teachableId]=1;
  var locked=bank().list.filter(function(p){ return !ok[p.id]&&lvlIdx(p.level)<=lvlIdx(level())+1; });
  var bad=[], reasons={};
  (data.exercises||[]).forEach(function(ex,i){
    if(!ex) return;
    var used=[].concat(ex.uses_grammar||[]).filter(Boolean);
    var illegal=used.filter(function(id){ return !ok[id]; });
    if(illegal.length){ bad.push(i); illegal.forEach(function(id){ var p=gramPoint(id); reasons[p?p.name_pl:id]=1; }); return; }
    if(PRODUCTIVE.indexOf(ex.type)>=0&&!used.length){ bad.push(i); return; }
    for(var k=0;k<locked.length;k++){ if(sieveHit(ex,locked[k])){ bad.push(i); reasons[locked[k].name_pl]=1; return; } }
  });
  return {bad:bad,reasons:Object.keys(reasons)};
};
```

## Three checks, in deliberate order

**Check 1 — declared but not allowed.** The exercise names a structure outside
the permitted set. Cheapest check, catches the honest-but-wrong model.

**Check 2 — productive but declaring nothing.**

```javascript
var PRODUCTIVE=['produce','sculpt','transform','translate','scenario'];
```

These are the exercise types that require the learner to *generate* language
rather than recognise it. A productive exercise with an empty `uses_grammar` is
rejected on principle: producing language without using grammar is not possible,
so an empty declaration means the model did not declare, not that no grammar was
used. Undeclared grammar is exactly what check 3 exists to catch, and an
undeclared productive exercise is the case where it matters most.

**Check 3 — the sieve.** The expensive one, run last, only on what survived.

```javascript
function sieveHit(ex,point){
  if(point.sieve!==true) return false;
  var exps=[].concat(point.exponents||[])
    .map(function(e){ return String(e==null?'':e).trim().toLowerCase(); })
    .filter(Boolean);
  if(!exps.length) return false;
  var t=exText(ex);
  for(var i=0;i<exps.length;i++){
    var e=exps[i];
    /* Prog dlugosci zostaje rozny (wielowyrazowe >=5, pojedyncze >=6), ale
       dopasowanie idzie juz przez te sama granice warunkowa. */
    if(e.length < (e.indexOf(' ')>0 ? 5 : 6)) continue;
    var r=_wordRe(e);
    if(r ? r.test(t) : (t.indexOf(e)>=0)) return true;
  }
  return false;
}
```

Each grammar point carries **exponents** — the surface forms that betray it.
The sieve scans the exercise text for exponents belonging to structures the
learner has not unlocked. It catches the model that used the past tense and
simply did not mention it.

## Two decisions inside the sieve worth defending

**The search space is bounded.** `locked` is not every unlearned structure —
it is those at most one CEFR level above the learner:

```javascript
lvlIdx(p.level)<=lvlIdx(level())+1
```

An A1 learner cannot plausibly be handed C1 structures by a model that was told
to stay at A1, and scanning for them costs time on every exercise for a case
that does not occur. One level of headroom covers realistic overreach.

**The sieve is opt-in per point.** Only points with `sieve: true` are scanned —
**293 of 578**. The flag is set only where the exponents are unambiguous. The
Spanish exponent `es` would match inside half the words in any Spanish sentence;
flagging it would make the validator reject everything. A sieve that fires
constantly gets switched off, and then there is no sieve at all.

The cost of that decision is measured in [`05-limits.md`](05-limits.md), not
hand-waved.

## Why declaration and sieve both exist

The declaration check is cheap, precise, and trivially evaded by omission. The
sieve is expensive, fuzzy, and cannot be evaded by silence. Neither alone is
sufficient: a model that declares nothing passes check 1 completely, and a model
that declares correctly while writing prose full of unlocked grammar passes the
sieve only because the sieve is looking at the same text.

The return value is deliberately not a boolean. `{bad:[indices], reasons:[names]}`
carries **which** exercises failed and **which** structures caused it — because
the next step needs both: the indices to discard, the names to put into the
retry prompt.

---

[← The prompt](02-the-prompt.md) · [Next: the fallback path →](04-the-fallback.md)
