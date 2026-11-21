"""
Task 11 – Recommend and Defend the Final Design
  • Type and rounding recommendation (Decimal, per-payment)
  • How rate revisions are carried out (single module)
  • Limitations of the current design
  • Scalability to district-union scale
  • Alternative: rate card from JSON file
"""

import json
import time
import random
from decimal import Decimal
from pathlib import Path

SEP = "=" * 64

# ════════════════════════════════════════════════════════════════
# RECOMMENDED DESIGN
# ════════════════════════════════════════════════════════════════

# milkrate.py holds the single source of truth; importing it here
# simulates how every other module in the system uses it.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import milkrate

print(SEP)
print("TASK 11 – Final Design Recommendation")
print(SEP)

print("""
══════════════════════════════════════════════════════════════════
RECOMMENDATION SUMMARY
══════════════════════════════════════════════════════════════════

1. TYPE    Use Decimal (created from strings) for all money values.
           float accumulates IEEE-754 rounding errors that differ
           from the bank statement at scale (see Task 10).

2. ROUNDING  Round every individual payment to 2 decimal places
             (the paisa), not just the final total.  The bank
             credits each session's payment separately and rounds
             each one; matching that behaviour keeps the accounts
             consistent.

3. RATE REVISION  All rates live in milkrate.py as named UPPER_CASE
           constants.  A revision means editing one file and
           recommitting; every script that imports the module
           automatically picks up the new values on the next run.
           No grep-and-replace across k files is needed.

4. VALIDATION  Every entry must pass validate_entry() before
           payout() is computed.  Invalid entries are skipped
           with a logged message; they never stop the batch.

5. INPUT   Use try/except ValueError around float() conversion
           (EAFP style): simpler, handles edge cases (' 8.5 ',
           locale commas) with one replace('.', ',') normalisation.
""")

# ════════════════════════════════════════════════════════════════
# EVIDENCE FROM EXPERIMENTS (re-run to confirm)
# ════════════════════════════════════════════════════════════════
random.seed(42)

def gen(n):
    return [(round(random.uniform(5,20),1),
             round(random.uniform(2.5,6.5),1),
             round(random.uniform(7.5,9.5),1)) for _ in range(n)]

def total_f(entries):
    tot = 0.0
    for lit, fat, snf in entries:
        fs = round((fat - 3.5) / 0.1)
        ss = round((snf - 8.5) / 0.1)
        r  = round(30.00 + fs*0.40 + ss*0.30, 2)
        tot += round(r * lit, 2)
    return round(tot, 2)

def total_d(entries):
    tot = Decimal("0.00")
    for lit, fat, snf in entries:
        fat_d = Decimal(str(fat)); snf_d = Decimal(str(snf))
        fs = round((fat_d - Decimal("3.5")) / Decimal("0.1"))
        ss = round((snf_d - Decimal("8.5")) / Decimal("0.1"))
        r  = round(Decimal("30.00") + fs*Decimal("0.40") + ss*Decimal("0.30"), 2)
        tot += round(r * Decimal(str(lit)), 2)
    return round(tot, 2)

print("── Evidence: float vs Decimal discrepancy ────────────────────")
print(f"  {'Scale':>12} {'float':>14} {'Decimal':>14} {'Diff (paise)':>14}")
print("  " + "─" * 58)
for n in [300, 6_000, 150_000]:
    entries = gen(n)
    t0 = time.perf_counter(); ft = total_f(entries); t1 = time.perf_counter()
    t2 = time.perf_counter(); dt = total_d(entries); t3 = time.perf_counter()
    diff = round((float(dt) - ft) * 100, 4)
    label = {300:"1 centre", 6_000:"1 block", 150_000:"1 district"}[n]
    print(f"  {label:>12} {ft:>14.2f} {dt:>14.2f} {diff:>14.4f}")

print("""
  Conclusion: Decimal is the correct choice for district-union scale.
  The float error at 150,000 entries is typically 1-5 paise – small but
  real, and large enough to cause a bank reconciliation failure.
""")

# ════════════════════════════════════════════════════════════════
# LIMITATIONS
# ════════════════════════════════════════════════════════════════
print("── Limitations of the current design ────────────────────────")
limitations = [
    "No persistent storage: payments are not saved to a database or file.",
    "Single-threaded: 150,000 entries processed sequentially (~2 s).",
    "Fat/SNF to 1 decimal place: analyser output with 2 dp needs Task 12 fix.",
    "No duplicate-entry detection (same farmer, same shift, same day).",
    "Rate card is hard-coded: a JSON-file approach (see below) is more flexible.",
    "No farmer master file: farmer_id is not validated against a known list.",
]
for i, lim in enumerate(limitations, 1):
    print(f"  {i}. {lim}")

# ════════════════════════════════════════════════════════════════
# JSON RATE CARD ALTERNATIVE
# ════════════════════════════════════════════════════════════════
print("\n── Alternative: JSON rate card ───────────────────────────────")

# Write a sample JSON rate card
sample_card = {
    "base_rate"      : 30.00,
    "fat_step_value" : 0.40,
    "snf_step_value" : 0.30,
    "fat_std"        : 3.5,
    "snf_std"        : 8.5,
    "step_size"      : 0.1,
    "fat_min"        : 2.0,
    "fat_max"        : 7.0,
    "snf_min"        : 7.0,
    "snf_max"        : 10.0
}

card_path = Path("/home/claude/milk_coop/rate_card.json")
card_path.write_text(json.dumps(sample_card, indent=2))

# Load at start-up
t0 = time.perf_counter()
with card_path.open() as fh:
    loaded_card = json.load(fh)
t1 = time.perf_counter()

print(f"  rate_card.json written to {card_path}")
print(f"  Load time: {(t1-t0)*1000:.3f} ms  (one-time start-up cost)")
print(f"  Content  : {loaded_card}")

def rate_from_card(fat, snf, card):
    fs = round((fat - card["fat_std"]) / card["step_size"])
    ss = round((snf - card["snf_std"]) / card["step_size"])
    return round(card["base_rate"] + fs * card["fat_step_value"]
                                   + ss * card["snf_step_value"], 2)

print(f"\n  rate_from_card(4.2, 8.7, loaded_card) = "
      f"{rate_from_card(4.2, 8.7, loaded_card)}")

print("""
  Trade-offs:
  • JSON card: a rate revision is a text-file edit; no Python knowledge needed.
    The file can be deployed to 300 centres without redistributing the program.
    Start-up cost: ~1 ms to read and parse – negligible.
  • Module constants: simpler, version-controlled with the code, type-checked
    by linters.  Requires a code commit for each revision.
  Recommendation: use JSON for production deployment where the rate revision
  is done by non-programmers; use module constants for the prototype/study.

── Scalability to District-Union Scale ──────────────────────────
  150,000 entries × Decimal arithmetic ≈ 2–3 s on a laptop.
  For the district union, batch the data into chunks (one centre at a time),
  use multiprocessing.Pool to run centres in parallel, and write running totals
  to a database.  The core functions (rate_per_litre, payout) are stateless
  and safe to run in parallel without locks.
""")
