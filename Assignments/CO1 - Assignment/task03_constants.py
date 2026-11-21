"""
Task 3 – Choose Variables and Name the Constants
  • UPPER_CASE naming convention for constants
  • Python has no true constants – convention only
  • Dynamic typing demonstration
  • Multiple assignment and swapping
  • Magic numbers vs named constants vs dictionary rate card
"""

SEP = "=" * 64

# ════════════════════════════════════════════════════════════════
# NAMED CONSTANTS  (PEP 8 → UPPER_CASE_WITH_UNDERSCORES)
# ════════════════════════════════════════════════════════════════
BASE_RATE      = 30.00   # Rs / litre at standard fat & SNF
FAT_STEP_VALUE = 0.40    # Rs / litre per 0.1 % fat deviation
SNF_STEP_VALUE = 0.30    # Rs / litre per 0.1 % SNF deviation
FAT_STD        = 3.5     # standard fat %
SNF_STD        = 8.5     # standard SNF %
STEP_SIZE      = 0.1     # size of one step (0.1 %)
FAT_MIN        = 2.0
FAT_MAX        = 7.0
SNF_MIN        = 7.0
SNF_MAX        = 10.0
DAYS_IN_PERIOD = 10

print(SEP)
print("TASK 3 – Variables and Constants")
print(SEP)

# ── Naming conventions ───────────────────────────────────────────
print("\n── PEP 8 Naming Conventions ─────────────────────────────────")
conventions = [
    ("UPPER_CASE",          "Module-level constants (e.g. BASE_RATE)"),
    ("lower_case",          "Variables and function names (e.g. fat_steps)"),
    ("_leading_underscore", "Internal / private names by convention"),
    ("CamelCase",           "Class names (e.g. RateCard)"),
    ("SCREAMING_SNAKE",     "Constants shared across modules"),
]
for style, usage in conventions:
    print(f"  {style:<24} → {usage}")

# ── Python has no true constants ─────────────────────────────────
print("""
── Why Python has no true constants ─────────────────────────────
  Python does not enforce immutability for module-level names.
  Writing BASE_RATE = 30.00 is a promise to other programmers, not a lock.
  Any code that says BASE_RATE = 99 will silently succeed.
  Convention: UPPER_CASE = "do not change this"; linters (pylint, flake8)
  can warn on reassignment, and dataclasses.field(default=…, init=False)
  or typing.Final can reinforce the intent, but cannot truly prevent it.
""")

# ── Named constants vs magic numbers ─────────────────────────────
print("── Named constant vs magic number ───────────────────────────")
# BAD  – magic numbers scattered everywhere
def rate_magic(fat, snf):
    return 30.00 + round((fat - 3.5) / 0.1) * 0.40 + round((snf - 8.5) / 0.1) * 0.30

# GOOD – single source of truth
def rate_named(fat, snf):
    fat_steps = round((fat - FAT_STD) / STEP_SIZE)
    snf_steps = round((snf - SNF_STD) / STEP_SIZE)
    return round(BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE, 2)

print(f"  rate_magic(4.2, 8.7) = {rate_magic(4.2, 8.7)}")
print(f"  rate_named(4.2, 8.7) = {rate_named(4.2, 8.7)}")
print("  For a rate revision: magic numbers → k places to change (error-prone).")
print("  Named constants    → 1 place to change (FAT_STEP_VALUE = 0.45).")

# ── Dictionary alternative ────────────────────────────────────────
print("\n── Dictionary rate-card alternative ─────────────────────────")
RATE_CARD = {
    "base"   : 30.00,
    "fat"    : 0.40,
    "snf"    : 0.30,
    "fat_std": 3.5,
    "snf_std": 8.5,
    "step"   : 0.1,
}
def rate_dict(fat, snf, card=RATE_CARD):
    fs = round((fat - card["fat_std"]) / card["step"])
    ss = round((snf - card["snf_std"]) / card["step"])
    return round(card["base"] + fs * card["fat"] + ss * card["snf"], 2)

print(f"  RATE_CARD = {RATE_CARD}")
print(f"  rate_dict(4.2, 8.7) = {rate_dict(4.2, 8.7)}")
print("  Advantage: the entire card can be replaced with one assignment,")
print("  read from a JSON file, or passed to a function. Useful for Task 12.")

# ── Dynamic typing ────────────────────────────────────────────────
print("\n── Dynamic typing demonstration ─────────────────────────────")
x = 100
print(f"  x = 100         → type: {type(x).__name__}, value: {x}")
x = 100.5
print(f"  x = 100.5       → type: {type(x).__name__}, value: {x}")
x = "hundred"
print(f"  x = 'hundred'   → type: {type(x).__name__}, value: {x}")
x = [1, 2, 3]
print(f"  x = [1,2,3]     → type: {type(x).__name__}, value: {x}")
print("  The variable x is rebound; the type is a property of the object,")
print("  not of the variable. This is called dynamic (duck) typing.")

# ── Multiple assignment and swap ─────────────────────────────────
print("\n── Multiple assignment and swap ─────────────────────────────")
a, b = FAT_STD, SNF_STD
print(f"  a, b = FAT_STD, SNF_STD → a = {a}, b = {b}")
a, b = b, a
print(f"  a, b = b, a             → a = {a}, b = {b}  (swapped)")
fat, snf, shift = 4.2, 8.7, "AM"
print(f"  fat, snf, shift = 4.2, 8.7, 'AM' → {fat}, {snf}, {shift}")

# ── All named constants listed ────────────────────────────────────
print("\n── Complete constant listing ─────────────────────────────────")
consts = [
    ("BASE_RATE",       BASE_RATE),
    ("FAT_STEP_VALUE",  FAT_STEP_VALUE),
    ("SNF_STEP_VALUE",  SNF_STEP_VALUE),
    ("FAT_STD",         FAT_STD),
    ("SNF_STD",         SNF_STD),
    ("STEP_SIZE",       STEP_SIZE),
    ("FAT_MIN",         FAT_MIN),
    ("FAT_MAX",         FAT_MAX),
    ("SNF_MIN",         SNF_MIN),
    ("SNF_MAX",         SNF_MAX),
    ("DAYS_IN_PERIOD",  DAYS_IN_PERIOD),
]
for name, val in consts:
    print(f"  {name:<20} = {val}")
