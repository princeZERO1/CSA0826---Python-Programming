"""
Task 4 – Write Correct Expressions
  • Operator precedence (**, unary minus, *, /, +, -)
  • Floating-point surprise in step calculation
  • round() vs int() vs math.floor() for negative values
  • Comparison chaining and Boolean operators
"""

import math

SEP = "=" * 64

BASE_RATE      = 30.00
FAT_STD        = 3.5
SNF_STD        = 8.5
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30
STEP_SIZE      = 0.1

print(SEP)
print("TASK 4 – Expressions")
print(SEP)

# ════════════════════════════════════════════════════════════════
# CORE PAYMENT EXPRESSIONS
# ════════════════════════════════════════════════════════════════
print("\n── Core rate calculation expressions ────────────────────────")

test_cases = [
    (3.5, 8.5),
    (4.2, 8.7),
    (3.1, 8.3),
]
for fat, snf in test_cases:
    fat_steps = round((fat - FAT_STD) / STEP_SIZE)
    snf_steps = round((snf - SNF_STD) / STEP_SIZE)
    rate      = round(BASE_RATE
                      + fat_steps * FAT_STEP_VALUE
                      + snf_steps * SNF_STEP_VALUE, 2)
    print(f"  fat={fat}, snf={snf}")
    print(f"    raw fat diff / step = {(fat - FAT_STD) / STEP_SIZE!r}")
    print(f"    fat_steps (round)   = {fat_steps}")
    print(f"    snf_steps (round)   = {snf_steps}")
    print(f"    rate                = {rate}")

# ════════════════════════════════════════════════════════════════
# THREE SURPRISING RESULTS
# ════════════════════════════════════════════════════════════════
print("\n── Surprise 1: (4.2 − 3.5) / 0.1 ≠ 7 ─────────────────────")
raw = (4.2 - 3.5) / 0.1
print(f"  (4.2 - 3.5) / 0.1  = {raw!r}")
print(f"  round(...)          = {round(raw)}")
print("  Reason: 4.2 and 3.5 lack exact binary representations.")
print("  The subtraction leaves a tiny residue; division amplifies it.")
print("  round() fixes the step count; int() or floor() would give 6 (wrong).")

print("\n── Surprise 2: -7 // 2 = -4, not -3 ──────────────────────")
print(f"  -7 // 2         = {-7 // 2}   (floor division → rounds toward −∞)")
print(f"  int(-3.5)       = {int(-3.5)}   (truncation    → rounds toward 0)")
print(f"  math.floor(-3.5)= {math.floor(-3.5)}   (same as //)")
print(f"  math.ceil(-3.5) = {math.ceil(-3.5)}   (toward +∞)")
print("  For negative fat/snf deviations, int() truncates toward 0 (fewer steps)")
print("  → lower penalty. round() gives the nearest integer correctly.")

print("\n── Surprise 3: True == 1 and False == 0 ───────────────────")
print(f"  True  + 1       = {True + 1}")
print(f"  False + 1       = {False + 1}")
print(f"  True  * 30.0    = {True * 30.0}")
print(f"  isinstance(True, int) = {isinstance(True, int)}")
print("  bool is a subclass of int; guard against using boolean as a number.")

# ════════════════════════════════════════════════════════════════
# OPERATOR PRECEDENCE
# ════════════════════════════════════════════════════════════════
print("\n── Operator precedence in rate expression ───────────────────")
print("  BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE")
print("  Precedence (highest first): ** > unary-minus > * / // % > + -")
print("  * is evaluated before +, so no extra parentheses are needed.")
print("  Explicit parentheses in (fat - FAT_STD) ensure subtraction first.")
print(f"  -2 ** 2  = {-2 ** 2}   (unary minus applied AFTER **)")
print(f"  (-2)**2  = {(-2)**2}   (parentheses force base to be negative)")

# ════════════════════════════════════════════════════════════════
# COMPARISON CHAINING AND BOOLEAN OPERATORS
# ════════════════════════════════════════════════════════════════
print("\n── Comparison chaining ──────────────────────────────────────")
for fat_val in [1.9, 2.0, 3.5, 7.0, 7.1]:
    fat_ok = 2.0 <= fat_val <= 7.0
    snf_ok = 7.0 <= 8.5 <= 10.0        # always True here
    valid  = fat_ok and snf_ok
    print(f"  fat={fat_val}: 2.0 <= {fat_val} <= 7.0 → {fat_ok:<5}  valid={valid}")

# ════════════════════════════════════════════════════════════════
# int() vs math.floor() vs round() COMPARISON
# ════════════════════════════════════════════════════════════════
print("\n── round() vs int() vs math.floor() for step count ─────────")
header = f"  {'fat':>5} {'raw diff/step':>16} {'round':>7} {'int':>5} {'floor':>7}"
print(header)
print("  " + "-" * 44)
for fat_val in [4.2, 3.1, 4.05, 2.95]:
    raw   = (fat_val - FAT_STD) / STEP_SIZE
    r_val = round(raw)
    i_val = int(raw)
    f_val = math.floor(raw)
    rate_r = round(BASE_RATE + r_val * FAT_STEP_VALUE, 2)
    rate_i = round(BASE_RATE + i_val * FAT_STEP_VALUE, 2)
    rate_f = round(BASE_RATE + f_val * FAT_STEP_VALUE, 2)
    print(f"  {fat_val:>5.2f} {raw:>16.13f} {r_val:>7}  {i_val:>4}  {f_val:>6}")
    print(f"         rates → round={rate_r}  int={rate_i}  floor={rate_f}")

print("""
  CONCLUSION:
  round() is the only correct choice for step counting.
  int() truncates toward 0: fat=4.2 gives 6 steps instead of 7 → Rs 0.40 short.
  math.floor() gives wrong results for negative deviations (too harsh a penalty).
  All three methods are O(1) time and O(1) space.
""")
