"""
Task 6 – Organise the Logic into Functions
  • validate_entry(), rate_per_litre(), payout(), ten_day_total()
  • Parameters, return values, docstrings
  • Returning vs printing
  • Local vs global scope
  • Why constants are readable but should not be reassigned inside functions
"""

from decimal import Decimal

SEP = "=" * 64

# ════════════════════════════════════════════════════════════════
# CONSTANTS  (global – readable inside every function)
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
# FUNCTION 1 – validate_entry
# ════════════════════════════════════════════════════════════════
def validate_entry(litres: float, fat: float, snf: float) -> tuple:
    """
    Check that one delivery entry falls within acceptable limits.

    Parameters
    ----------
    litres : float  Quantity delivered (must be > 0)
    fat    : float  Fat percentage (must be 2.0 – 7.0 inclusive)
    snf    : float  SNF percentage (must be 7.0 – 10.0 inclusive)

    Returns
    -------
    (bool, str)  (True, 'OK') if valid;
                 (False, reason) if any check fails.
    """
    if litres <= 0:
        return False, f"Litres must be > 0 (got {litres})"
    if not (FAT_MIN <= fat <= FAT_MAX):
        return False, f"Fat {fat}% outside allowed range {FAT_MIN}–{FAT_MAX}%"
    if not (SNF_MIN <= snf <= SNF_MAX):
        return False, f"SNF {snf}% outside allowed range {SNF_MIN}–{SNF_MAX}%"
    return True, "OK"


# ════════════════════════════════════════════════════════════════
# FUNCTION 2 – rate_per_litre
# ════════════════════════════════════════════════════════════════
def rate_per_litre(fat: float, snf: float) -> Decimal:
    """
    Compute the price per litre for the given fat and SNF percentages.

    The price is adjusted from BASE_RATE by FAT_STEP_VALUE per 0.1 % of fat
    deviation from FAT_STD, and by SNF_STEP_VALUE per 0.1 % of SNF deviation
    from SNF_STD.  Steps are rounded to the nearest whole integer to avoid
    floating-point artefacts (e.g. 7.000000000000001 → 7).

    Parameters
    ----------
    fat : float  Fat percentage of the delivered milk
    snf : float  SNF percentage of the delivered milk

    Returns
    -------
    Decimal  Price per litre, rounded to 2 decimal places.
    """
    fat_d     = Decimal(str(fat))
    snf_d     = Decimal(str(snf))
    fat_steps = round((fat_d - FAT_STD) / STEP_SIZE)   # nearest whole step
    snf_steps = round((snf_d - SNF_STD) / STEP_SIZE)
    rate      = BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE
    return round(rate, 2)


# ════════════════════════════════════════════════════════════════
# FUNCTION 3 – payout
# ════════════════════════════════════════════════════════════════
def payout(litres: float, fat: float, snf: float) -> Decimal:
    """
    Compute the payment for one delivery.

    Validates the entry first; raises ValueError for invalid data.

    Parameters
    ----------
    litres : float  Quantity delivered
    fat    : float  Fat percentage
    snf    : float  SNF percentage

    Returns
    -------
    Decimal  Amount payable, rounded to 2 decimal places.

    Raises
    ------
    ValueError  If the entry fails validation.
    """
    ok, reason = validate_entry(litres, fat, snf)
    if not ok:
        raise ValueError(reason)
    rate = rate_per_litre(fat, snf)
    return round(rate * Decimal(str(litres)), 2)


# ════════════════════════════════════════════════════════════════
# FUNCTION 4 – ten_day_total
# ════════════════════════════════════════════════════════════════
def ten_day_total(entries: list) -> Decimal:
    """
    Compute the cumulative payment for a list of deliveries.

    Each element of entries must be a (litres, fat, snf) tuple.
    Invalid entries are skipped and reported; they do not stop processing.

    Parameters
    ----------
    entries : list of (litres, fat, snf) tuples

    Returns
    -------
    Decimal  Total payment for the period, rounded to 2 decimal places.
    """
    total   = Decimal("0.00")
    skipped = 0
    for litres, fat, snf in entries:
        try:
            total += payout(litres, fat, snf)
        except ValueError as err:
            print(f"  [SKIP] {err}")
            skipped += 1
    if skipped:
        print(f"  {skipped} invalid entr{'y' if skipped == 1 else 'ies'} skipped.")
    return round(total, 2)


# ════════════════════════════════════════════════════════════════
# SCOPE DEMONSTRATION
# ════════════════════════════════════════════════════════════════
def scope_demo():
    """Show that local variables are separate from global constants."""
    # Local variables – exist only inside this call
    rate      = Decimal("0.00")     # shadows nothing; different from global none
    fat_steps = 0
    snf_steps = 0

    # Reading a global is fine
    local_base = BASE_RATE          # read-only use of global constant
    # Uncommenting the next line would create a NEW local, not change the global:
    # BASE_RATE = Decimal("99.00")  # ← would raise UnboundLocalError
    return local_base


# ════════════════════════════════════════════════════════════════
# DEMONSTRATION
# ════════════════════════════════════════════════════════════════
print(SEP)
print("TASK 6 – Functions")
print(SEP)

test_entries = [
    (10.0, 3.5, 8.5),
    (8.5,  4.2, 8.7),
    (12.0, 3.1, 8.3),
    (5.5,  7.0, 9.8),
    (6.0,  2.0, 7.2),
]

print(f"\n  {'Litres':>8} {'Fat%':>6} {'SNF%':>6} {'Rate':>10} {'Amount':>12}")
print("  " + "─" * 48)
for lit, fat, snf in test_entries:
    rate = rate_per_litre(fat, snf)
    pay  = payout(lit, fat, snf)
    print(f"  {lit:>8.1f} {fat:>6.1f} {snf:>6.1f} {rate:>10.2f} {pay:>12.2f}")

total = ten_day_total(test_entries)
print("  " + "─" * 48)
print(f"  {'Ten-day total':>32} {total:>12.2f}")

print("\n── Invalid entry handling ────────────────────────────────────")
bad_entries = [
    (-1.0, 3.5, 8.5),   # negative litres
    (10.0, 7.5, 8.5),   # fat too high
    (10.0, 3.5, 6.5),   # SNF too low
]
ten_day_total(bad_entries)

print("\n── Scope demonstration ───────────────────────────────────────")
print(f"  scope_demo() reads BASE_RATE = {scope_demo()} without modifying it.")
print("  Local variables (rate, fat_steps, snf_steps) live only inside the call.")
print("  Assigning BASE_RATE inside a function would create a local shadow,")
print("  leaving the module-level constant unchanged – silent and dangerous.")

print("""
── Returning vs Printing ─────────────────────────────────────────
  rate_per_litre() RETURNS a Decimal – the caller can store, compare
  or accumulate it.  If it printed instead, the caller would receive None
  and ten_day_total() would crash on 'total += None'.
  Rule: functions compute and RETURN; the caller or main script PRINTS.

── Lambda alternative ────────────────────────────────────────────
  rate_lambda = lambda f, s: round(
      30.00 + round((f-3.5)/0.1)*0.40 + round((s-8.5)/0.1)*0.30, 2)
  Drawback: no docstring, no parameter type hints, no validation hook,
  hard to read – fine for a one-liner sort key, wrong for business logic.
  Function-call overhead is O(1) per entry, negligible for even 150,000 entries.
""")
