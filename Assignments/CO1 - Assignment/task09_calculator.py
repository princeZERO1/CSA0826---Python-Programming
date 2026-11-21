"""
Task 9 – Implement and Test the Complete Calculator
  Full payment calculator for Ksheera Village Milk Co-operative.
  Includes structured assert-based tests covering:
    • Normal entries (fat/SNF above and below standard)
    • Boundary entries (exactly at standard; at limits)
    • Invalid entries (text, negative, out-of-range)
    • Five-entry set with hand-verified total
"""

from decimal import Decimal

SEP = "=" * 64

# ════════════════════════════════════════════════════════════════
# CONSTANTS
# ════════════════════════════════════════════════════════════════
BASE_RATE      = Decimal("30.00")
FAT_STEP_VALUE = Decimal("0.40")
SNF_STEP_VALUE = Decimal("0.30")
FAT_STD        = Decimal("3.5")
SNF_STD        = Decimal("8.5")
STEP_SIZE      = Decimal("0.1")
FAT_MIN, FAT_MAX = 2.0, 7.0
SNF_MIN, SNF_MAX = 7.0, 10.0

# ════════════════════════════════════════════════════════════════
# CALCULATOR FUNCTIONS
# ════════════════════════════════════════════════════════════════
def validate_entry(litres, fat, snf):
    """Return (True, 'OK') or (False, reason_string)."""
    if not isinstance(litres, (int, float)) or not isinstance(fat, (int, float)) \
            or not isinstance(snf, (int, float)):
        return False, "All values must be numeric"
    if litres <= 0:
        return False, f"Litres must be > 0 (got {litres})"
    if not (FAT_MIN <= fat <= FAT_MAX):
        return False, f"Fat {fat}% outside [{FAT_MIN}, {FAT_MAX}]"
    if not (SNF_MIN <= snf <= SNF_MAX):
        return False, f"SNF {snf}% outside [{SNF_MIN}, {SNF_MAX}]"
    return True, "OK"


def rate_per_litre(fat, snf):
    """Price per litre (Decimal, 2 dp) for given fat & SNF %."""
    fat_d = Decimal(str(fat))
    snf_d = Decimal(str(snf))
    fs = round((fat_d - FAT_STD) / STEP_SIZE)
    ss = round((snf_d - SNF_STD) / STEP_SIZE)
    return round(BASE_RATE + fs * FAT_STEP_VALUE + ss * SNF_STEP_VALUE, 2)


def payout(litres, fat, snf):
    """Amount payable (Decimal, 2 dp); raises ValueError if invalid."""
    ok, reason = validate_entry(litres, fat, snf)
    if not ok:
        raise ValueError(reason)
    return round(rate_per_litre(fat, snf) * Decimal(str(litres)), 2)


def ten_day_total(entries):
    """Cumulative payment for a list of (litres, fat, snf) tuples."""
    total   = Decimal("0.00")
    skipped = 0
    for entry in entries:
        try:
            litres, fat, snf = entry
            total += payout(litres, fat, snf)
        except (ValueError, TypeError) as err:
            skipped += 1
            print(f"    [SKIP] {err}")
    return round(total, 2), skipped


# ════════════════════════════════════════════════════════════════
# TEST SUITE
# ════════════════════════════════════════════════════════════════

passed = 0
failed = 0

def check(label, actual, expected):
    global passed, failed
    ok = (actual == expected)
    status = "PASS" if ok else "FAIL"
    if ok:
        passed += 1
    else:
        failed += 1
    print(f"  [{status}] {label}")
    if not ok:
        print(f"         expected {expected}, got {actual}")


print(SEP)
print("TASK 9 – Complete Calculator & Tests")
print(SEP)

# ── GROUP 1: Normal entries ──────────────────────────────────────
print("\n── Group 1: Normal entries ───────────────────────────────────")

# fat above standard → higher rate
check("fat=4.2, snf=8.5 → rate",
      rate_per_litre(4.2, 8.5), Decimal("32.80"))
check("fat=4.2, snf=8.5 → payout(10L)",
      payout(10, 4.2, 8.5), Decimal("328.00"))

# fat below standard → lower rate
check("fat=3.0, snf=8.5 → rate",
      rate_per_litre(3.0, 8.5), Decimal("28.00"))
check("fat=3.0, snf=8.5 → payout(10L)",
      payout(10, 3.0, 8.5), Decimal("280.00"))

# snf above standard
check("fat=3.5, snf=9.0 → rate",
      rate_per_litre(3.5, 9.0), Decimal("31.50"))

# snf below standard
check("fat=3.5, snf=8.0 → rate",
      rate_per_litre(3.5, 8.0), Decimal("28.50"))

# both above standard
check("fat=4.2, snf=8.7 → rate",
      rate_per_litre(4.2, 8.7), Decimal("33.40"))
check("fat=4.2, snf=8.7 → payout(8.5L)",
      payout(8.5, 4.2, 8.7), Decimal("283.90"))

# both below standard
check("fat=3.1, snf=8.3 → rate",
      rate_per_litre(3.1, 8.3), Decimal("27.80"))
check("fat=3.1, snf=8.3 → payout(12L)",
      payout(12, 3.1, 8.3), Decimal("333.60"))

# ── GROUP 2: Boundary entries ────────────────────────────────────
print("\n── Group 2: Boundary entries ─────────────────────────────────")

# exactly at standard
check("fat=3.5, snf=8.5 (standard) → rate",
      rate_per_litre(3.5, 8.5), Decimal("30.00"))
check("fat=3.5, snf=8.5 → payout(10L)",
      payout(10, 3.5, 8.5), Decimal("300.00"))

# minimum fat
check("fat=2.0, snf=8.5 → rate",
      rate_per_litre(2.0, 8.5), Decimal("24.00"))

# maximum fat
check("fat=7.0, snf=8.5 → rate",
      rate_per_litre(7.0, 8.5), Decimal("44.00"))

# minimum snf
check("fat=3.5, snf=7.0 → rate",
      rate_per_litre(3.5, 7.0), Decimal("25.50"))

# maximum snf
check("fat=3.5, snf=10.0 → rate",
      rate_per_litre(3.5, 10.0), Decimal("34.50"))

# fat=2.0 and snf=7.0 (double minimum)
check("fat=2.0, snf=7.0 → rate",
      rate_per_litre(2.0, 7.0), Decimal("19.50"))

# ── GROUP 3: Invalid entries ─────────────────────────────────────
print("\n── Group 3: Invalid entries ──────────────────────────────────")

def expect_error(label, litres, fat, snf):
    global passed, failed
    try:
        payout(litres, fat, snf)
        failed += 1
        print(f"  [FAIL] {label} – expected ValueError, got no error")
    except ValueError as e:
        passed += 1
        print(f"  [PASS] {label} → {e}")

expect_error("litres=0",    0,    3.5, 8.5)
expect_error("litres=-5",  -5,    3.5, 8.5)
expect_error("fat=1.9",    10,    1.9, 8.5)   # below FAT_MIN
expect_error("fat=7.1",    10,    7.1, 8.5)   # above FAT_MAX
expect_error("snf=6.9",    10,    3.5, 6.9)   # below SNF_MIN
expect_error("snf=10.1",   10,    3.5, 10.1)  # above SNF_MAX

# ── GROUP 4: Five-entry hand-verified set ────────────────────────
print("\n── Group 4: Five-entry hand-verified set ─────────────────────")

# Hand calculations:
# F001: rate=30.00, pay = 30.00 × 10.0 = 300.00
# F002: fat_steps=7, snf_steps=2 → rate=33.40, pay=33.40×8.5=283.90
# F003: fat_steps=-4,snf_steps=-2→ rate=27.80, pay=27.80×12=333.60
# F004: fat_steps=35,snf_steps=13→ rate=47.90, pay=47.90×5=239.50
# F005: fat_steps=-15,snf_steps=-13→rate=20.10, pay=20.10×7=140.70
# Total = 300.00+283.90+333.60+239.50+140.70 = 1297.70

five_entries = [
    (10.0, 3.5, 8.5),
    (8.5,  4.2, 8.7),
    (12.0, 3.1, 8.3),
    (5.0,  7.0, 9.8),
    (7.0,  2.0, 7.2),
]

print(f"\n  {'Litres':>8} {'Fat':>6} {'SNF':>6} {'Rate':>8} {'Amount':>10}")
print("  " + "─" * 44)
running = Decimal("0.00")
for lit, fat, snf in five_entries:
    rate = rate_per_litre(fat, snf)
    pay  = payout(lit, fat, snf)
    running += pay
    print(f"  {lit:>8.1f} {fat:>6.1f} {snf:>6.1f} {rate:>8.2f} {pay:>10.2f}")
print("  " + "─" * 44)
print(f"  {'Total':>30} {running:>10.2f}")

# Hand-verify: 300.00+283.90+333.60+239.50+140.70
expected_total = Decimal("300.00") + Decimal("283.90") + Decimal("333.60") \
              + Decimal("239.50") + Decimal("140.70")
check("Five-entry ten-day total", running, expected_total)

# ── SUMMARY ─────────────────────────────────────────────────────
print(f"\n{'─'*64}")
print(f"  Test results: {passed} passed, {failed} failed out of {passed+failed} tests")
print(f"{'─'*64}")

# ════════════════════════════════════════════════════════════════
# FULL PRINTED LEDGER
# ════════════════════════════════════════════════════════════════
print("""
── Full ten-day payment ledger (sample run) ─────────────────────
""")

ledger = [
    ("F001", "AM", 10.0, 3.5, 8.5),
    ("F002", "PM",  8.5, 4.2, 8.7),
    ("F003", "AM", 12.0, 3.1, 8.3),
    ("F004", "PM",  5.0, 7.0, 9.8),
    ("F005", "AM",  7.0, 2.0, 7.2),
]

print(f"  {'Farmer':<8} {'Shift':>5} {'Litres':>8} "
      f"{'Fat%':>6} {'SNF%':>6} {'Rate':>8} {'Amount (Rs)':>12}")
print("  " + "─" * 60)

grand = Decimal("0.00")
for fid, sh, lit, fat, snf in ledger:
    rate = rate_per_litre(fat, snf)
    pay  = payout(lit, fat, snf)
    grand += pay
    print(f"  {fid:<8} {sh:>5} {lit:>8.2f} {fat:>6.1f} "
          f"{snf:>6.1f} {rate:>8.2f} {pay:>12.2f}")

print("  " + "─" * 60)
print(f"  {'Grand Total':>50} {grand:>12.2f}")
