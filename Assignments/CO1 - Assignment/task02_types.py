"""
Task 2 – Explore Values and Types in the Interpreter
  • type() of common values
  • Division operators: /, //, %
  • Floating-point surprise: 0.1 + 0.2 == 0.3
  • Money and Decimal vs float
  • Complete the Code – TODO 1
"""

import sys
from decimal import Decimal

SEP = "=" * 64

# ════════════════════════════════════════════════════════════════
# INTERACTIVE-MODE EXPLORATION (shown as >>> session)
# ════════════════════════════════════════════════════════════════
print(SEP)
print("TASK 2 – Values and Types")
print(SEP)

print("\n── Simulated interactive session (>>> prompts) ──────────────")
session = [
    ("type(10)",           type(10)),
    ("type(10.0)",         type(10.0)),
    ('type("10")',         type("10")),
    ("type(True)",         type(True)),
    ("type([10, 8.5])",    type([10, 8.5])),
    ("7 / 2",              7 / 2),
    ("7 // 2",             7 // 2),
    ("7 % 2",              7 % 2),
    ("-7 // 2",            -7 // 2),
    ("0.1 + 0.2 == 0.3",   0.1 + 0.2 == 0.3),
    ("repr(0.1 + 0.2)",    repr(0.1 + 0.2)),
]
for expr, result in session:
    print(f"  >>> {expr}")
    print(f"  {result!r}")

print("""
  EXPLANATIONS
  7 / 2   → 3.5    true division always returns float.
  7 // 2  → 3      floor division truncates toward −∞ (here same as truncation).
  7 % 2   → 1      remainder after floor division.
  -7 // 2 → -4     floor(-3.5) = -4, NOT -3 (floor goes toward −∞, not toward 0).
  0.1+0.2 → False  0.1 and 0.2 have no exact binary representation.
                   The IEEE 754 sum is 0.30000000000000004, not 0.3.
  repr(…) → shows the full imprecise value stored in the float.
""")

print("── Memory size of numeric types ─────────────────────────────")
for val in [0, 1_000_000, 0.0, Decimal("0.00")]:
    print(f"  sys.getsizeof({val!r:>14}) = {sys.getsizeof(val)} bytes  "
          f"({type(val).__name__})")

# ════════════════════════════════════════════════════════════════
# COMPLETE THE CODE – TODO 1
# ════════════════════════════════════════════════════════════════

# 1,000 payments of Rs 33.40 and three small adjustments of Rs 0.10
payments = ["33.40"] * 1000 + ["0.10"] * 3


def total_float(items):
    """Sum amounts using float – accumulates IEEE-754 rounding errors."""
    total = 0.0
    for amount in items:
        total += float(amount)
    return total


def total_decimal(items):
    """
    Sum amounts exactly using Decimal created from each string.
    TODO 1: Add the amounts exactly by creating a Decimal from each string,
            and return the Decimal total.
    """
    total = Decimal("0")          # exact zero
    for amount in items:
        total += Decimal(amount)  # Decimal(string) is exact
    return total


print("\n── Complete the Code output ──────────────────────────────────")
print(f"float  : {total_float(payments)}")
print(f"Decimal: {total_decimal(payments)}")
print(0.1 + 0.2 == 0.3, Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))

# ════════════════════════════════════════════════════════════════
# EFFECT OF Decimal(float(amount))
# ════════════════════════════════════════════════════════════════

def total_decimal_via_float(items):
    """Wraps float in Decimal – the float error is imported first."""
    total = Decimal("0")
    for amount in items:
        total += Decimal(float(amount))   # float conversion loses precision
    return total

print(f"\n── Effect of Decimal(float(amount)) ─────────────────────────")
print(f"Decimal(float(amount)): {total_decimal_via_float(payments)}")
print("""
  EXPLANATION:
  Decimal(float("33.40")) does NOT stay at 33.40.
  Python first creates the float 33.39999999999999857891452847979962825775…
  then wraps that inexact value inside a Decimal, so the error is re-introduced.
  Moral: always pass the original string directly to Decimal(), never the float.
""")

# ════════════════════════════════════════════════════════════════
# ALTERNATIVE – integer paise
# ════════════════════════════════════════════════════════════════

def total_paise(items):
    """Keep running total as integer paise; convert to rupees only for display."""
    total_p = 0          # int – no rounding error possible
    for amount in items:
        total_p += round(float(amount) * 100)   # one round per entry
    return total_p / 100  # rupees for display

print("── Alternative: integer paise ───────────────────────────────")
print(f"integer paise method: {total_paise(payments):.2f}")
print("""
  COMPARISON (time and space per addition, n payments):
  ─────────────────────────────────────────────────────
  float          O(1) time, 24 bytes, accumulates error → wrong for large n
  Decimal(str)   O(1) time, ~200 bytes, exact            → recommended
  Decimal(float) O(1) time, ~200 bytes, re-imports error → wrong
  int paise      O(1) time, 28 bytes, exact              → acceptable
  round(float)   O(1) time, 24 bytes, error after many   → risky for 150k entries
""")
