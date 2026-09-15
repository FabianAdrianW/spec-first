# Results

Raw output of `verify.py`, run against the live grammar banks in
[FabianAdrianW/eyelingo](https://github.com/FabianAdrianW/eyelingo).
Regenerate it yourself with `python3 verify.py` — no dependencies, no API keys.

Numbers quoted anywhere in this repository come from here. If your run
disagrees with this file, the repository is wrong and this file is stale.

```
Fetching grammar banks from the public repository...
  fetched 14 banks

==============================================================
BANK SIZE
==============================================================
lang    points   levels
ar          40   {'A1': 20, 'A2': 20}
de          40   {'A1': 20, 'A2': 20}
en          57   {'A1': 18, 'A2': 19, 'B1': 20}
es          40   {'A1': 20, 'A2': 20}
fr          40   {'A1': 20, 'A2': 20}
it          40   {'A1': 20, 'A2': 20}
jp          41   {'A1': 20, 'A2': 21}
ko          40   {'A1': 20, 'A2': 20}
nl          40   {'A1': 20, 'A2': 20}
no          40   {'A1': 20, 'A2': 20}
pt          40   {'A1': 20, 'A2': 20}
ru          40   {'A1': 20, 'A2': 20}
uk          40   {'A1': 20, 'A2': 20}
zh          40   {'A1': 20, 'A2': 20}

  TOTAL: 578 points across 14 languages
  by level: {'A1': 278, 'A2': 280, 'B1': 20}

==============================================================
PREREQUISITE GRAPH
==============================================================
  references: 601
  broken:     0

==============================================================
SM-2 CALIBRATION
==============================================================
  points with initial_ease: 578/578

==============================================================
EXPONENT SCRIPT CONVENTION
==============================================================
lang    exponents  native script   required
ar             71              0   translit
de            126              0   -
en            163              0   -
es            128              0   -
fr            135              0   -
it            136              0   -
jp             83              0   translit
ko             81              0   translit
nl            134              0   -
no             72              0   -
pt             95              0   -
ru             83             83   -
uk             83             83   -
zh             72              0   translit

==============================================================
SIEVE COVERAGE  (see 05-limits.md)
==============================================================
  points with sieve:true          293/578
  of those, reachable by sieve    254/293  (86%)
  never tested, all exponents     39
  below the length guard

  lang     reachable    coverage
  ar           16/16    100%
  de           26/34    76%
  en           36/36    100%
  es           19/27    70%
  fr           22/33    66%
  it           21/33    63%
  jp           18/18    100%
  ko           21/21    100%
  nl             2/2    100%
  no           14/14    100%
  pt           12/12    100%
  ru           15/15    100%
  uk           14/14    100%
  zh           18/18    100%

==============================================================
CONVENTIONS THAT DO NOT HOLD  (see 05-limits.md)
==============================================================
  examples per point:   {2: 577, 3: 1}
    convention says exactly 3 -> 577/578 deviate
  paradigm rows:        {2: 8, 3: 87, 4: 338, 5: 80, 6: 52, 7: 9, 8: 4}
    convention says 4-6 -> 108/578 outside range

==============================================================
Done. Compare against RESULTS.md.
==============================================================
```

---

[← README](README.md)
