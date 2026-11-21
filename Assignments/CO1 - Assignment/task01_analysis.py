"""
Task 1 – Understand the Problem and Identify the Data
Ksheera Village Milk Producers' Co-operative – Payment Calculator
"""

# ════════════════════════════════════════════════════════════════
# CONSTANTS  (never change during one run)
# ════════════════════════════════════════════════════════════════
BASE_RATE      = 30.00   # Rs/litre at standard 3.5 % fat & 8.5 % SNF
FAT_STD        = 3.5     # standard fat %
SNF_STD        = 8.5     # standard SNF %
FAT_STEP_VALUE = 0.40    # Rs/litre per 0.1 % fat deviation
SNF_STEP_VALUE = 0.30    # Rs/litre per 0.1 % SNF deviation
STEP_SIZE      = 0.1     # one step = 0.1 %

FAT_MIN, FAT_MAX = 2.0, 7.0    # acceptable fat range %
SNF_MIN, SNF_MAX = 7.0, 10.0   # acceptable SNF range %
LITRES_MIN      = 0.001         # must be strictly positive
LITRES_MAX      = 999.9         # realistic max per session
DAYS_IN_PERIOD  = 10            # payment cycle

VALID_SHIFTS = ("AM", "PM")  # two collection shifts per day

# ════════════════════════════════════════════════════════════════
# SAMPLE DATA  – each delivery stored as one tuple (scales to
#               300 or 150,000 farmers without code changes)
# ════════════════════════════════════════════════════════════════
entries = [
    # (farmer_id, litres, fat_pct, snf_pct, shift)
    ("F001", 10.0, 3.5, 8.5, "AM"),
    ("F002",  8.5, 4.2, 8.7, "PM"),
    ("F003", 12.0, 3.1, 8.3, "AM"),
    ("F004",  5.5, 7.0, 9.8, "AM"),   # fat at upper limit
    ("F005",  6.0, 2.0, 7.2, "PM"),   # fat at lower limit
]

# ════════════════════════════════════════════════════════════════
# ANALYSIS OUTPUT
# ════════════════════════════════════════════════════════════════
SEP = "=" * 64

print(SEP)
print("TASK 1 – Problem Analysis: Ksheera Milk Co-operative")
print(SEP)

print("""
BACKGROUND
  About 300 farmers deliver milk twice a day (AM and PM shifts).
  Payments are made every 10 days based on quantity, fat % and SNF %.
""")

print("── INPUTS (what the clerk records per delivery) ──────────────")
inputs = [
    ("farmer_id", "str",   "Unique farmer code, e.g. 'F001'"),
    ("litres",    "float", "Quantity delivered in one session (> 0)"),
    ("fat",       "float", "Fat percentage, 1 decimal place from analyser"),
    ("snf",       "float", "SNF percentage, 1 decimal place from analyser"),
    ("shift",     "str",   "'AM' or 'PM'"),
]
for name, typ, desc in inputs:
    print(f"  {name:<12} {typ:<8} {desc}")

print("\n── OUTPUTS (what the program computes) ──────────────────────")
outputs = [
    ("rate",          "float/Decimal", "Rs per litre for this delivery"),
    ("amount",        "float/Decimal", "Payment = rate × litres"),
    ("ten_day_total", "float/Decimal", "Cumulative payment over 10 days"),
]
for name, typ, desc in outputs:
    print(f"  {name:<16} {typ:<16} {desc}")

print("\n── CONSTANTS (typed once, never altered during a run) ────────")
consts = [
    ("BASE_RATE",       BASE_RATE,       "float", "Rs/L at 3.5% fat & 8.5% SNF"),
    ("FAT_STD",         FAT_STD,         "float", "Standard fat %"),
    ("SNF_STD",         SNF_STD,         "float", "Standard SNF %"),
    ("FAT_STEP_VALUE",  FAT_STEP_VALUE,  "float", "Rs/L per 0.1% fat step"),
    ("SNF_STEP_VALUE",  SNF_STEP_VALUE,  "float", "Rs/L per 0.1% SNF step"),
    ("STEP_SIZE",       STEP_SIZE,       "float", "Size of one step (0.1%)"),
    ("DAYS_IN_PERIOD",  DAYS_IN_PERIOD,  "int",   "Payment cycle = 10 days"),
]
for name, val, typ, desc in consts:
    print(f"  {name:<20} = {str(val):<6}  ({typ})  {desc}")

print("\n── DATA TYPES ───────────────────────────────────────────────")
print("  Whole numbers (int)   : DAYS_IN_PERIOD, step counts (computed)")
print("  Fractional (float)    : litres, fat, snf, rate, amount")
print("  Text (str)            : farmer_id, shift")
print("  Best-practice money   : Decimal (avoids float rounding errors)")

print("\n── VALIDATION RULES (every entry must pass before payment) ──")
rules = [
    ("litres > 0",                    "Cannot pay for zero or negative quantity"),
    (f"litres <= {LITRES_MAX}",       "Realistic upper bound per session"),
    (f"{FAT_MIN} <= fat <= {FAT_MAX}","Outside range means invalid / spoilt milk"),
    (f"{SNF_MIN} <= snf <= {SNF_MAX}","SNF must be physically plausible"),
    ("shift in ('AM','PM')",          "Only two defined shifts"),
    ("farmer_id is non-empty str",    "Every payment must be traceable to a farmer"),
]
for rule, reason in rules:
    print(f"  • {rule:<35} → {reason}")

print("\n── ASSUMPTIONS ──────────────────────────────────────────────")
assumptions = [
    "Fat and SNF are read to one decimal place (analyser output).",
    "Rate steps are symmetric: same Rs adjustment above or below standard.",
    "Litres are measured to two decimal places (flow-meter).",
    "Rounding to the nearest paisa (2 decimal places) is acceptable.",
    "A negative or zero litres entry is a data-entry error, not a return.",
]
for i, a in enumerate(assumptions, 1):
    print(f"  {i}. {a}")

print("\n── SAMPLE ENTRIES TABLE ─────────────────────────────────────")
print(f"  {'ID':<6} {'Litres':>8} {'Fat%':>6} {'SNF%':>6} {'Shift':>5}")
print("  " + "-" * 36)
for fid, lit, fat, snf, sh in entries:
    print(f"  {fid:<6} {lit:>8.1f} {fat:>6.1f} {snf:>6.1f} {sh:>5}")

print("""
── ALTERNATIVE CONCEPT: separate variables vs list of tuples ──
  Separate-variable approach (litres1, fat1, snf1 … litres300, fat300, snf300):
    • Requires 300 × 3 = 900 variable names.
    • A loop or function call must name every variable explicitly.
    • For 150,000 farmers: 450,000 variable names – completely unmanageable.
    • Time:  O(n) but code size grows proportionally to n.
    • Space: O(n) variables, plus the overhead of Python name look-up for each.

  List/tuple approach  [(litres, fat, snf), …]:
    • One for-loop, one function signature: scales from 1 to 150,000 entries
      without any code change.
    • Time:  O(n)  (same asymptotic complexity, far less code).
    • Space: O(n)  (compact; each tuple occupies ~72 bytes in CPython).
    • The list approach is the only design that scales.
""")
