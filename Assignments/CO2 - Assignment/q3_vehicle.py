"""
Q3 – Engineer a Vehicle Registration Number Validator
Toll Plaza Number-Plate Records

Valid format: 2 letters (state) + 2 digits (district) + 1–2 letters (series) + 4 digits
Examples: TN09AB1234, KA01M0007

Only string operations – no regular expressions.

Bloom's Level: K4 – Analyse
"""

# ─────────────────────────────────────────────────────────────────────────────
# PREDICTIONS (before execution)
# ─────────────────────────────────────────────────────────────────────────────
# Input               Normalised    Valid?   Reason if invalid
# tn 09 ab 1234    →  TN09AB1234    valid    10 chars: 2+2+2+4
# KA-01-M-0007     →  KA01M0007     valid    9 chars: 2+2+1+4
# TN9AB1234        →  TN9AB1234     INVALID  state+district part wrong
# TN 22 1234 AB    →  TN221234AB    INVALID  digits before letters at end
# MH12DE1433       →  MH12DE1433    valid    10 chars
# UP16BV (short)   →  UP16BV        INVALID  only 6 chars, missing 4-digit number


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 : normalise  (TODO 1 completed)
# ─────────────────────────────────────────────────────────────────────────────
def normalise(text):
    """'tn 09 ab 1234' -> 'TN09AB1234' (spaces and hyphens removed, upper case)."""
    # TODO 1 completed: Remove spaces and hyphens; convert to upper case
    return text.replace(" ", "").replace("-", "").upper()


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 : is_valid  (TODO 2 completed)
# ─────────────────────────────────────────────────────────────────────────────
def is_valid(reg):
    """
    Valid form: 2 letters, 2 digits, 1 or 2 letters, 4 digits.
    Lengths: 9 (2+2+1+4) or 10 (2+2+2+4).
    """
    # TODO 2 completed: Check length, then slice each part
    n = len(reg)
    if n not in (9, 10):
        return False

    # First 2 chars: state code – must be letters
    state = reg[0:2]
    if not state.isalpha():
        return False

    # Next 2 chars: district digits
    district = reg[2:4]
    if not district.isdigit():
        return False

    # Middle: 1 or 2 letters (series)
    if n == 9:
        series = reg[4:5]       # 1 letter
        number = reg[5:]        # last 4 digits  → reg[-4:]
    else:                       # n == 10
        series = reg[4:6]       # 2 letters      → reg[4:-4]
        number = reg[6:]        # last 4 digits  → reg[-4:]

    if not series.isalpha():
        return False
    if not number.isdigit() or len(number) != 4:
        return False

    return True


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 : format_receipt
# ─────────────────────────────────────────────────────────────────────────────
def format_receipt(reg):
    """Format a valid normalised number as 'TN 09 AB 1234'."""
    n = len(reg)
    if n == 10:
        # TN 09 AB 1234
        return f"{reg[0:2]} {reg[2:4]} {reg[4:6]} {reg[6:10]}"
    elif n == 9:
        # KA 01 M 0007
        return f"{reg[0:2]} {reg[2:4]} {reg[4:5]} {reg[5:9]}"
    else:
        return "INVALID"


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 : MAIN TEST  (expected output matches assignment)
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 60)
print("VEHICLE REGISTRATION VALIDATOR")
print("=" * 60)

test_inputs = ["tn 09 ab 1234", "KA-01-M-0007", "TN9AB1234", "TN 22 1234 AB"]

for raw in test_inputs:
    reg = normalise(raw)
    valid = is_valid(reg)
    status = "valid" if valid else "INVALID"
    receipt = format_receipt(reg) if valid else "—"
    print(f"{raw:15} -> {reg:11} {status:7}  receipt: {receipt}")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 : SLICING INQUIRY
# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 60)
print("SLICING INQUIRY")
print("=" * 60)

s9  = "KA01M0007"   # 9-char valid number
s10 = "TN09AB1234"  # 10-char valid number

print(f"s9  = '{s9}'  (len={len(s9)})")
print(f"  s9[-4:]   = '{s9[-4:]}'   ← last 4 digits (number part)")
print(f"  s9[4:-4]  = '{s9[4:-4]}'      ← series letter(s), mid section")

print(f"\ns10 = '{s10}'  (len={len(s10)})")
print(f"  s10[-4:]  = '{s10[-4:]}'   ← last 4 digits")
print(f"  s10[4:-4] = '{s10[4:-4]}'    ← series letters")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6 : IMMUTABILITY EXPLANATION
# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 60)
print("STRING IMMUTABILITY")
print("=" * 60)

text = "tn09ab1234"
upper = text.upper()
print(f"text        = '{text}'   (unchanged)")
print(f"text.upper()= '{upper}'  (new object)")
print(f"text is upper: {text is upper}  ← different objects in memory")
print("→ text.upper() does NOT change 'text'; it returns a NEW string.")
print("→ Strings in Python are immutable: no character can be changed in place.")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 7 : SIX PREDICTED INPUTS
# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 60)
print("SIX PREDICTED TEST CASES (including 2 rejections)")
print("=" * 60)

predicted = [
    ("MH-12-DE-1433", True,  "10-char valid"),
    ("UP 16 BV 2345", True,  "10-char valid"),
    ("KL05J9876",     True,  "9-char valid"),
    ("UP16BV",        False, "too short – missing number"),
    ("T9AB1234",      False, "state only 1 letter"),
    ("TN 22 1234 AB", False, "digits before letters at end"),
]

for raw, expected, reason in predicted:
    reg = normalise(raw)
    result = is_valid(reg)
    match = "✓" if result == expected else "✗ MISMATCH"
    print(f"  {raw:20} → {reg:12} {'valid' if result else 'INVALID':7}  [{reason}] {match}")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 8 : ALTERNATIVE – regex comparison
# ─────────────────────────────────────────────────────────────────────────────
import re

def is_valid_regex(reg):
    """Alternative: validate using re.fullmatch."""
    return bool(re.fullmatch(r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}", reg))

print()
print("=" * 60)
print("REGEX ALTERNATIVE COMPARISON")
print("=" * 60)
for raw, expected, reason in predicted:
    reg = normalise(raw)
    r1 = is_valid(reg)
    r2 = is_valid_regex(reg)
    agree = "agree" if r1 == r2 else "DIFFER"
    print(f"  {reg:12}  slicing={'valid' if r1 else 'INVALID':7}  regex={'valid' if r2 else 'INVALID':7}  → {agree}")

print("""
COMPLEXITY:
  Both: O(L) time for a number of length L.
  Slicing: more verbose, but zero extra imports; easier to adjust individual parts.
  Regex:   one compact pattern; easier to change the overall structure at a glance.
  For a toll plaza (small L), both are equally fast in practice.
""")
