#!/usr/bin/env python3
"""
verify.py — reproduces every number quoted in this repository.

Nothing here is asserted on trust. The script pulls the live grammar banks
from the public Eyelingo repository and recomputes the figures in RESULTS.md
from scratch. If a number in this repo is wrong, this script will say so.

Usage:
    python3 verify.py

Requires: Python 3.8+, internet access. No third-party packages.
"""

import json
import re
import sys
import urllib.request
from collections import Counter

RAW = "https://raw.githubusercontent.com/FabianAdrianW/eyelingo/main"
LANGS = ["ar", "de", "en", "es", "fr", "it", "jp",
         "ko", "nl", "no", "pt", "ru", "uk", "zh"]

# Languages whose convention requires exponents written in Latin
# transliteration rather than the native script.
TRANSLIT_REQUIRED = {"ar", "jp", "ko", "zh"}

NON_LATIN = re.compile(
    r"[\u0400-\u04FF"      # Cyrillic
    r"\u0600-\u06FF"       # Arabic
    r"\u3040-\u30FF"       # Kana
    r"\u3400-\u9FFF"       # CJK
    r"\uAC00-\uD7AF]"      # Hangul
)


def fetch(path):
    with urllib.request.urlopen(f"{RAW}/{path}", timeout=30) as r:
        return r.read().decode("utf-8")


def sieve_threshold_passes(exponent):
    """Mirrors the length guard in sieveHit() — grammar-engine.js:641.

        if (e.length < (e.indexOf(' ') > 0 ? 5 : 6)) continue;

    Exponents shorter than the guard are never tested against lesson text.
    """
    e = str(exponent).strip().lower()
    return len(e) >= (5 if " " in e else 6)


def main():
    banks = {}
    print("Fetching grammar banks from the public repository...")
    for code in LANGS:
        try:
            banks[code] = json.loads(
                fetch(f"data/grammar/grammar-bank.{code}.json"))["points"]
        except Exception as exc:                       # noqa: BLE001
            print(f"  {code}: FAILED ({exc})")
    if not banks:
        sys.exit("No banks could be fetched. Check your connection.")
    print(f"  fetched {len(banks)} banks\n")

    all_ids = {p["id"] for pts in banks.values() for p in pts}
    total = sum(len(p) for p in banks.values())

    # ---- size and level distribution -------------------------------------
    levels = Counter(p.get("level")
                     for pts in banks.values() for p in pts)
    print("=" * 62)
    print("BANK SIZE")
    print("=" * 62)
    print(f"{'lang':6}{'points':>8}   levels")
    for code in sorted(banks):
        lv = Counter(p.get("level") for p in banks[code])
        print(f"{code:6}{len(banks[code]):>8}   {dict(sorted(lv.items()))}")
    print(f"\n  TOTAL: {total} points across {len(banks)} languages")
    print(f"  by level: {dict(sorted(levels.items()))}")

    # ---- prerequisite graph integrity ------------------------------------
    refs, broken = 0, []
    for pts in banks.values():
        for p in pts:
            for pr in (p.get("prereq") or []):
                refs += 1
                if pr not in all_ids:
                    broken.append((p["id"], pr))
    print("\n" + "=" * 62)
    print("PREREQUISITE GRAPH")
    print("=" * 62)
    print(f"  references: {refs}")
    print(f"  broken:     {len(broken)}")
    for b in broken[:20]:
        print(f"    {b[0]} -> {b[1]}  (target does not exist)")

    # ---- SM-2 calibration -------------------------------------------------
    missing_ease = sum(
        1 for pts in banks.values() for p in pts
        if not ((p.get("srs") or {}).get("initial_ease")))
    print("\n" + "=" * 62)
    print("SM-2 CALIBRATION")
    print("=" * 62)
    print(f"  points with initial_ease: {total - missing_ease}/{total}")

    # ---- transliteration convention ---------------------------------------
    print("\n" + "=" * 62)
    print("EXPONENT SCRIPT CONVENTION")
    print("=" * 62)
    print(f"{'lang':6}{'exponents':>11}{'native script':>15}   required")
    for code in sorted(banks):
        exps = [e for p in banks[code] for e in (p.get("exponents") or [])]
        native = sum(1 for e in exps if NON_LATIN.search(str(e)))
        req = "translit" if code in TRANSLIT_REQUIRED else "-"
        print(f"{code:6}{len(exps):>11}{native:>15}   {req}")

    # ---- sieve coverage ---------------------------------------------------
    sieve_pts = [p for pts in banks.values() for p in pts
                 if p.get("sieve") is True]
    covered = [p for p in sieve_pts
               if any(sieve_threshold_passes(e)
                      for e in (p.get("exponents") or []))]
    print("\n" + "=" * 62)
    print("SIEVE COVERAGE  (see 05-limits.md)")
    print("=" * 62)
    print(f"  points with sieve:true          {len(sieve_pts)}/{total}")
    print(f"  of those, reachable by sieve    {len(covered)}/{len(sieve_pts)}"
          f"  ({100 * len(covered) // max(1, len(sieve_pts))}%)")
    print(f"  never tested, all exponents     {len(sieve_pts) - len(covered)}")
    print(f"  below the length guard")
    print()
    print(f"  {'lang':6}{'reachable':>12}{'':4}coverage")
    for code in sorted(banks):
        sp = [p for p in banks[code] if p.get("sieve") is True]
        cv = [p for p in sp if any(sieve_threshold_passes(e)
                                   for e in (p.get("exponents") or []))]
        pct = f"{100 * len(cv) // len(sp)}%" if sp else "-"
        print(f"  {code:6}{f'{len(cv)}/{len(sp)}':>12}{'':4}{pct}")

    # ---- stated conventions that do NOT hold ------------------------------
    ex_counts = Counter()
    row_counts = Counter()
    for pts in banks.values():
        for p in pts:
            teach = p.get("teach") or {}
            ex_counts[len(teach.get("examples") or [])] += 1
            rows = (teach.get("paradigm") or {}).get("rows")
            if rows is not None:
                row_counts[len(rows)] += 1
    print("\n" + "=" * 62)
    print("CONVENTIONS THAT DO NOT HOLD  (see 05-limits.md)")
    print("=" * 62)
    print(f"  examples per point:   {dict(sorted(ex_counts.items()))}")
    print(f"    convention says exactly 3 -> "
          f"{total - ex_counts[3]}/{total} deviate")
    print(f"  paradigm rows:        {dict(sorted(row_counts.items()))}")
    off = sum(v for k, v in row_counts.items() if not 4 <= k <= 6)
    print(f"    convention says 4-6 -> {off}/{sum(row_counts.values())} "
          f"outside range")

    print("\n" + "=" * 62)
    print("Done. Compare against RESULTS.md.")
    print("=" * 62)


if __name__ == "__main__":
    main()
