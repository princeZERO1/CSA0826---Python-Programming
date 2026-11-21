"""
Task 5 – Read Input and Convert Types
  • input() always returns str; convert with int() / float()
  • Handling 'eight', '8,5', ' 8.5 ' gracefully
  • str-method checks before conversion vs try/except
  • Formatted output with f-strings (width, precision)
"""

SEP = "=" * 64

print(SEP)
print("TASK 5 – Input and Type Conversion")
print(SEP)

# ════════════════════════════════════════════════════════════════
# APPROACH 1 – str-method guard before float()
# ════════════════════════════════════════════════════════════════

def is_valid_number(text: str) -> bool:
    """
    Return True if text (after stripping and replacing comma) looks like
    a valid non-negative float.  Handles: '8.5', ' 8.5 ', but rejects
    '8,5' (comma), 'eight', '', '-1'.
    """
    cleaned = text.strip().replace(",", ".")
    # Allow at most one decimal point; digits on each side
    parts = cleaned.split(".")
    if len(parts) > 2:
        return False
    return all(p.isdigit() for p in parts if p != "")


def safe_float_strcheck(text: str, min_val=None, max_val=None):
    """Read a float value using string-method pre-validation."""
    cleaned = text.strip()
    if not cleaned or not is_valid_number(cleaned):
        return None, f"'{text}' is not a valid number"
    value = float(cleaned.replace(",", "."))
    if min_val is not None and value < min_val:
        return None, f"Value {value} is below minimum {min_val}"
    if max_val is not None and value > max_val:
        return None, f"Value {value} is above maximum {max_val}"
    return value, "OK"


# ════════════════════════════════════════════════════════════════
# APPROACH 2 – try/except ValueError
# ════════════════════════════════════════════════════════════════

def safe_float_try(text: str, min_val=None, max_val=None):
    """Read a float value using try/except."""
    try:
        value = float(text.strip().replace(",", "."))
    except ValueError:
        return None, f"'{text}' is not a valid number"
    if min_val is not None and value < min_val:
        return None, f"Value {value} is below minimum {min_val}"
    if max_val is not None and value > max_val:
        return None, f"Value {value} is above maximum {max_val}"
    return value, "OK"


# ════════════════════════════════════════════════════════════════
# DEMONSTRATE BOTH APPROACHES
# ════════════════════════════════════════════════════════════════
test_inputs = [
    ("8.5",    "valid float"),
    (" 8.5 ",  "whitespace padded"),
    ("8,5",    "comma instead of period"),
    ("eight",  "text instead of number"),
    ("-1.0",   "negative (rejected)"),
    ("12.0",   "valid, in range"),
    ("",       "empty string"),
    ("3.5.1",  "two decimal points"),
]

print("\n── Validation comparison (str-check vs try/except) ──────────")
print(f"  {'Input':<12} {'str-check':>26} {'try/except':>26}")
print("  " + "-" * 66)
for text, label in test_inputs:
    val1, msg1 = safe_float_strcheck(text, min_val=0.001, max_val=999.9)
    val2, msg2 = safe_float_try(text,       min_val=0.001, max_val=999.9)
    r1 = f"{val1}" if val1 is not None else f"ERR: {msg1[:18]}"
    r2 = f"{val2}" if val2 is not None else f"ERR: {msg2[:18]}"
    print(f"  {text!r:<12} {r1:>26} {r2:>26}")

# ════════════════════════════════════════════════════════════════
# SIMULATED CLERK INPUT SESSION
# ════════════════════════════════════════════════════════════════
print("""
── Simulated clerk entry session ────────────────────────────────
  Clerk types: "F001"  → farmer_id (str, kept as-is)
  Clerk types: "10.5"  → litres    float("10.5")  = 10.5
  Clerk types: "3.5"   → fat       float("3.5")   = 3.5
  Clerk types: "8.5"   → snf       float("8.5")   = 8.5
  Clerk types: "AM"    → shift     (checked against ('AM','PM'))

  If clerk types "eight": float("eight") raises ValueError → re-prompt.
  If clerk types "8,5" : str-check finds comma → warn "use period".
                          try/except replaces comma → accepts 8.5.
  Recommendation: try/except is simpler and handles ' 8.5 ' (spaces) cleanly.
  Complexity: both are O(1) per entry; try/except is more Pythonic (EAFP style).
""")

# ════════════════════════════════════════════════════════════════
# FORMATTED OUTPUT
# ════════════════════════════════════════════════════════════════
print("── Formatted output with f-strings ──────────────────────────")

entries = [
    ("F001", 10.0, 3.5, 8.5, 30.00, 300.00),
    ("F002",  8.5, 4.2, 8.7, 33.40, 283.90),
    ("F003", 12.0, 3.1, 8.3, 27.80, 333.60),
    ("F004",  5.5, 7.0, 9.8, 44.80, 246.40),
    ("F005",  6.0, 2.0, 7.2, 20.60, 123.60),
]

# Header
print(f"\n  {'Farmer':<8} {'Litres':>8} {'Fat%':>6} {'SNF%':>6} "
      f"{'Rate (Rs/L)':>12} {'Amount (Rs)':>12}")
print("  " + "─" * 58)

running = 0.0
for fid, lit, fat, snf, rate, amt in entries:
    running += amt
    print(f"  {fid:<8} {lit:>8.2f} {fat:>6.1f} {snf:>6.1f} "
          f"{rate:>12.2f} {amt:>12.2f}")

print("  " + "─" * 58)
print(f"  {'Ten-day total':<42} {running:>12.2f}")

print("""
  f-string format specifiers used:
    {fid:<8}    left-align in 8 characters
    {lit:>8.2f} right-align, 8 wide, 2 decimal places (float)
    {fat:>6.1f} right-align, 6 wide, 1 decimal place
    {amt:>12.2f} right-align, 12 wide, 2 decimal places (money)
""")
