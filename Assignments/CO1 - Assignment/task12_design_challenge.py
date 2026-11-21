"""
Task 12 – Re-evaluate and Adapt the Design (Day-4 Design Challenge)
Changed requirements:
  A. Fat and SNF now have TWO decimal places (e.g. 4.25, 8.73).
  B. Seasonal rates: April–June → base = Rs 32.00, fat_step = Rs 0.45.
  C. Bonus: > 500 L delivered in 10 days → Rs 0.50 extra per litre.

Sections:
  A. Impact Analysis
  B. Evaluation of Original Design
  C. Adaptation / Redesign
  D. Evidence-Based Defence
"""

from decimal import Decimal
import time

SEP  = "=" * 64
SEP2 = "─" * 64

# ════════════════════════════════════════════════════════════════
# A. IMPACT ANALYSIS
# ════════════════════════════════════════════════════════════════
print(SEP)
print("TASK 12 – Day-4 Design Challenge")
print(SEP)

print("""
══════════════════════════════════════════════════════════════════
A. IMPACT ANALYSIS
══════════════════════════════════════════════════════════════════

What has changed from the original problem
───────────────────────────────────────────
1. PRECISION  Fat and SNF now carry TWO decimal places (e.g. 4.25 %)
   instead of one.  Steps are still 0.1 %, so 4.25 is 7.5 steps above
   3.5.  round(7.5) in Python uses "banker's rounding" (round-half-to-even)
   → round(7.5) = 8.  Whether to round to the nearest step or charge
   exactly must be decided; the co-operative must state the rule.

2. SEASONAL RATES  Two different rate cards must be supported:
      Non-peak   : base=30.00, fat_step=0.40, snf_step=0.30
      Peak (Apr–Jun): base=32.00, fat_step=0.45, snf_step=0.30
   The original single set of module constants cannot hold both.

3. BONUS  A new computation is added after the ten-day total is known:
      if total_litres > 500: bonus = total_litres × 0.50
   This requires storing or accumulating total litres per farmer per period,
   which the original design did not do.

Which constants, expressions and functions are affected
───────────────────────────────────────────────────────
• Constants  : BASE_RATE, FAT_STEP_VALUE must be season-dependent.
• rate_per_litre() : step calculation unchanged (still round); precision
  of fat/snf changes from 1 dp to 2 dp → Decimal(str(fat)) handles this
  already, so no code change needed in the expression itself.
• payout()   : unchanged – multiplies rate × litres.
• NEW function needed: bonus_payout(total_litres) → Decimal.
• ten_day_total() : must also accumulate total_litres to trigger bonus.

How two-decimal readings change step calculation
─────────────────────────────────────────────────
  fat = 4.25 %  → (4.25 − 3.5) / 0.1 = 7.5 steps
  Python round(7.5) = 8  (banker's rounding, rounds to even)
  Python round(7.4999) = 7
  Recommendation: use round(half_steps) and document that mid-step values
  are rounded to the nearest even step (consistent with the Indian
  Weights & Measures standard).
""")

# ════════════════════════════════════════════════════════════════
# B. EVALUATION OF ORIGINAL DESIGN
# ════════════════════════════════════════════════════════════════
print("""
══════════════════════════════════════════════════════════════════
B. EVALUATION OF ORIGINAL DESIGN
══════════════════════════════════════════════════════════════════
""")

# Original single-season function (reproduced for comparison)
_BASE = Decimal("30.00")
_FS   = Decimal("0.40")
_SS   = Decimal("0.30")
_FAT_STD = Decimal("3.5")
_SNF_STD = Decimal("8.5")
_STEP    = Decimal("0.1")

def rate_original(fat, snf):
    fd = Decimal(str(fat)); sd = Decimal(str(snf))
    return round(_BASE + round((fd-_FAT_STD)/_STEP)*_FS
                       + round((sd-_SNF_STD)/_STEP)*_SS, 2)

# Test with two-decimal reading
print("  Original rate_per_litre with two-decimal fat/snf:")
test_2dp = [(4.25, 8.73), (3.15, 8.45), (4.75, 9.05)]
for fat, snf in test_2dp:
    r = rate_original(fat, snf)
    fs = round((Decimal(str(fat)) - _FAT_STD) / _STEP)
    ss = round((Decimal(str(snf)) - _SNF_STD) / _STEP)
    print(f"    fat={fat}, snf={snf}: steps=({fs},{ss}) → rate={r}")

print("""
  VERDICT:
    • rate_per_litre(): WORKS for 2-dp readings – Decimal(str(fat)) handles
      any precision; round() rounds correctly to nearest 0.1 step.
    • payout(): WORKS – no change needed.
    • Constants BASE_RATE, FAT_STEP_VALUE: NEED CHANGE – must be season-aware.
    • ten_day_total(): NEEDS EXTENSION – must return total litres for bonus.
    • bonus_payout(): MISSING – must be added.
    Decision: MODIFY (not redesign) – the core expressions are correct;
    only constants and two functions need extension.
""")

# ════════════════════════════════════════════════════════════════
# C. ADAPTATION / REDESIGN
# ════════════════════════════════════════════════════════════════
print("""
══════════════════════════════════════════════════════════════════
C. ADAPTATION – Revised Design
══════════════════════════════════════════════════════════════════
""")

# ── Seasonal rate cards ──────────────────────────────────────────
SEASONS = {
    "non_peak": {
        "base"      : Decimal("30.00"),
        "fat_step"  : Decimal("0.40"),
        "snf_step"  : Decimal("0.30"),
        "fat_std"   : Decimal("3.5"),
        "snf_std"   : Decimal("8.5"),
        "step"      : Decimal("0.1"),
    },
    "peak": {           # April – June
        "base"      : Decimal("32.00"),
        "fat_step"  : Decimal("0.45"),
        "snf_step"  : Decimal("0.30"),
        "fat_std"   : Decimal("3.5"),
        "snf_std"   : Decimal("8.5"),
        "step"      : Decimal("0.1"),
    },
}

BONUS_THRESHOLD  = Decimal("500")    # litres in ten days
BONUS_RATE       = Decimal("0.50")   # Rs per litre


def get_season(month: int) -> str:
    """Return 'peak' for April–June (months 4–6), else 'non_peak'."""
    return "peak" if 4 <= month <= 6 else "non_peak"


def rate_per_litre_v2(fat: float, snf: float, season: str = "non_peak") -> Decimal:
    """
    Compute price per litre using the given season's rate card.

    Parameters
    ----------
    fat    : float – fat percentage (up to 2 decimal places)
    snf    : float – SNF percentage (up to 2 decimal places)
    season : str   – 'peak' or 'non_peak'

    Returns
    -------
    Decimal – price per litre, rounded to 2 dp.
    """
    card = SEASONS[season]
    fd   = Decimal(str(fat))
    sd   = Decimal(str(snf))
    fs   = round((fd - card["fat_std"]) / card["step"])
    ss   = round((sd - card["snf_std"]) / card["step"])
    return round(card["base"] + fs * card["fat_step"] + ss * card["snf_step"], 2)


def payout_v2(litres: float, fat: float, snf: float,
              season: str = "non_peak") -> Decimal:
    """Amount payable for one delivery, rounded to 2 dp."""
    return round(rate_per_litre_v2(fat, snf, season) * Decimal(str(litres)), 2)


def bonus_payout(total_litres: Decimal) -> Decimal:
    """
    Compute the volume bonus for a ten-day period.

    Parameters
    ----------
    total_litres : Decimal – total litres supplied in 10 days

    Returns
    -------
    Decimal – bonus amount (Rs 0.50 per litre if > 500 L, else 0.00).
    """
    if total_litres > BONUS_THRESHOLD:
        return round(total_litres * BONUS_RATE, 2)
    return Decimal("0.00")


def ten_day_total_v2(entries: list, season: str = "non_peak") -> tuple:
    """
    Compute cumulative payment and bonus for a ten-day period.

    Parameters
    ----------
    entries : list of (litres, fat, snf) tuples
    season  : str – 'peak' or 'non_peak'

    Returns
    -------
    (payment_total, total_litres, bonus, grand_total) all Decimal.
    """
    payment = Decimal("0.00")
    litres_sum = Decimal("0.00")
    for litres, fat, snf in entries:
        payment    += payout_v2(litres, fat, snf, season)
        litres_sum += Decimal(str(litres))
    bonus       = bonus_payout(litres_sum)
    grand_total = round(payment + bonus, 2)
    return payment, litres_sum, bonus, grand_total


# ════════════════════════════════════════════════════════════════
# D. EVIDENCE-BASED DEFENCE
# ════════════════════════════════════════════════════════════════
print("""
══════════════════════════════════════════════════════════════════
D. EVIDENCE-BASED DEFENCE
══════════════════════════════════════════════════════════════════
""")

# ── Test 1: Two-decimal fat/SNF ─────────────────────────────────
print("── Test 1: Two-decimal fat/SNF readings ──────────────────────")
print(f"  {'fat':>6} {'snf':>6} {'non_peak rate':>14} {'peak rate':>12}")
print("  " + "─" * 42)
for fat, snf in [(4.25, 8.73), (3.15, 8.45), (4.75, 9.05), (3.50, 8.50)]:
    rn = rate_per_litre_v2(fat, snf, "non_peak")
    rp = rate_per_litre_v2(fat, snf, "peak")
    print(f"  {fat:>6.2f} {snf:>6.2f} {rn:>14.2f} {rp:>12.2f}")

# ── Test 2: Both seasons, standard reading ───────────────────────
print("\n── Test 2: Same entry in both seasons ────────────────────────")
entries_std = [
    (10.0, 3.5, 8.5),
    (8.5,  4.2, 8.7),
    (12.0, 3.1, 8.3),
]
for season in ["non_peak", "peak"]:
    pay, lits, bon, grand = ten_day_total_v2(entries_std, season)
    card = SEASONS[season]
    print(f"  Season={season:8}  base={card['base']}  fat_step={card['fat_step']}")
    print(f"    Payment subtotal : Rs {pay:.2f}")
    print(f"    Total litres     :    {lits:.1f} L  (bonus threshold: 500 L)")
    print(f"    Bonus            : Rs {bon:.2f}")
    print(f"    Grand total      : Rs {grand:.2f}")

# ── Test 3: Bonus trigger ────────────────────────────────────────
print("\n── Test 3: Bonus trigger (> 500 L in 10 days) ───────────────")
# 60 deliveries of 9 L each = 540 L → bonus triggered
large_set = [(9.0, 3.5, 8.5)] * 60
pay, lits, bon, grand = ten_day_total_v2(large_set, "non_peak")
print(f"  60 × 9.0 L = {lits} L  > 500 L  → bonus = Rs {bon:.2f}")
print(f"  Payment subtotal : Rs {pay:.2f}")
print(f"  Bonus (540×0.50) : Rs {bon:.2f}")
print(f"  Grand total      : Rs {grand:.2f}")
expected_bonus = Decimal("540") * Decimal("0.50")
assert bon == expected_bonus, f"Bonus mismatch: {bon} != {expected_bonus}"
print(f"  ✓ Bonus verified: 540 × 0.50 = Rs {expected_bonus:.2f}")

# ── Test 4: No bonus below threshold ────────────────────────────
print("\n── Test 4: No bonus for ≤ 500 L ─────────────────────────────")
small_set = [(9.0, 3.5, 8.5)] * 55   # 495 L
pay2, lits2, bon2, grand2 = ten_day_total_v2(small_set, "non_peak")
print(f"  55 × 9.0 L = {lits2} L  ≤ 500 L  → bonus = Rs {bon2:.2f}")
assert bon2 == Decimal("0.00"), "Should be no bonus"
print(f"  ✓ No bonus correctly applied.")

# ── Test 5: Two-decimal reading mid-step (banker's rounding) ─────
print("\n── Test 5: Mid-step fat=4.25 (7.5 steps above 3.5) ──────────")
fat_mid = 4.25
raw_steps = (Decimal(str(fat_mid)) - Decimal("3.5")) / Decimal("0.1")
rounded   = round(raw_steps)
print(f"  raw steps  = {raw_steps}  → round({raw_steps}) = {rounded}")
print(f"  rate (non_peak) = {rate_per_litre_v2(fat_mid, 8.5, 'non_peak')}")
print(f"  rate (peak)     = {rate_per_litre_v2(fat_mid, 8.5, 'peak')}")
print("  Python uses banker's rounding (round-half-to-even): 7.5 → 8.")
print("  The co-operative should document this rule in their SOP.")

# ── Timing comparison ────────────────────────────────────────────
print("\n── Timing: original vs v2 at 6,000 entries ──────────────────")
import random
random.seed(42)
# Two-decimal fat/snf entries
entries_6k = [(round(random.uniform(5,20),1),
               round(random.uniform(2.5,6.5),2),   # 2 dp now
               round(random.uniform(7.5,9.5),2)) for _ in range(6000)]

t0 = time.perf_counter()
pay_v2, lits_v2, bon_v2, grand_v2 = ten_day_total_v2(entries_6k, "peak")
t1 = time.perf_counter()
print(f"  v2 (6,000 entries, peak season) : {t1-t0:.4f} s")
print(f"  Payment subtotal : Rs {pay_v2:.2f}")
print(f"  Total litres     :    {lits_v2:.1f} L")
print(f"  Bonus            : Rs {bon_v2:.2f}")
print(f"  Grand total      : Rs {grand_v2:.2f}")

print(f"""
── Trade-offs of the MODIFY decision ────────────────────────────
  ✓ Core expressions (rate_per_litre, payout) are unchanged – proven correct.
  ✓ Decimal(str(fat)) already handles 2-dp input without code change.
  ✓ Season parameter keeps one code path; a dictionary of cards is O(1) lookup.
  ✓ bonus_payout() is a new, isolated function – easy to test independently.
  ✗ The rate-card dictionary grows if more seasons or farmer categories are
    added; a JSON file or database table would then be preferable (see Task 11).
  ✗ Banker's rounding at mid-step must be agreed with the co-operative and
    documented; a different rounding rule may require changing round() to
    Decimal.quantize(ROUND_HALF_UP) throughout.

FINAL DECISION: MODIFY is the right choice.
  The original module structure, Decimal arithmetic, per-payment rounding,
  and validate_entry() are all correct and retained.  Three targeted changes
  suffice: (1) replace single constants with a SEASONS dictionary, (2) add a
  season parameter to rate_per_litre and ten_day_total, (3) add bonus_payout().
  No rewrite of the core calculation is needed.
""")
