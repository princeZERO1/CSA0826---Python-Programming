"""
Q1 – Decisions with Many Boundaries
State Electricity Subsidy Eligibility

Rules:
  - <= 100 units        : Full subsidy (everyone)
  - 101–200 units       : Partial subsidy ONLY if has ration card
  - > 200 units         : Subsidy ONLY if member aged > 80

Bloom's Level: K4 – Analyse
"""

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 : PREDICTIONS (before execution)
# ─────────────────────────────────────────────────────────────────────────────
# Household | units | ration_card | senior_80 | Expected Decision
#     1     |  80   |   False     |   False   | Full subsidy
#     2     | 100   |   False     |   False   | Full subsidy  (boundary)
#     3     | 101   |   True      |   False   | Partial subsidy (boundary)
#     4     | 101   |   False     |   False   | No subsidy (boundary, no card)
#     5     | 150   |   True      |   False   | Partial subsidy
#     6     | 200   |   True      |   False   | Partial subsidy (boundary)
#     7     | 201   |   True      |   True    | Subsidy (senior > 80) (boundary)
#     8     | 300   |   False     |   False   | No subsidy


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 : WHY separate if vs if-elif-else
# ─────────────────────────────────────────────────────────────────────────────
# Separate if statements: every condition is independently evaluated.
# A household consuming 80 units would satisfy BOTH "<=100" AND (hypothetically)
# any other if that also matches. This can assign multiple subsidies.
#
# if-elif-else: once one branch matches, the rest are SKIPPED.
# Exactly one branch executes → exactly one decision.


# ─────────────────────────────────────────────────────────────────────────────
# IMPLEMENTATION A : Separate if statements (BUGGY – may give multiple results)
# ─────────────────────────────────────────────────────────────────────────────
def subsidy_separate_if(units, ration_card, senior_80):
    """Uses separate if statements – can produce more than one result."""
    decisions = []

    if units <= 100:
        decisions.append("Full subsidy")

    if 101 <= units <= 200:                     # chained comparison
        if ration_card:
            decisions.append("Partial subsidy")
        else:
            decisions.append("No subsidy")

    if units > 200:
        if senior_80:
            decisions.append("Subsidy (senior > 80)")
        else:
            decisions.append("No subsidy")

    # For units <= 100 with extra if blocks below (simulating a developer's mistake):
    # e.g., if a developer forgets that units=80 also satisfies no other rule,
    # but if they had if units > 0: decisions.append("Usage fee") that would fire too.
    # Demonstrated: if units <= 100 AND units > 0 both fire → two decisions.
    if units > 0:                               # ← accidental second rule
        decisions.append("Usage recorded")

    return decisions


# ─────────────────────────────────────────────────────────────────────────────
# IMPLEMENTATION B : if–elif–else (CORRECT – exactly one result)
# ─────────────────────────────────────────────────────────────────────────────
def subsidy_elif(units, ration_card, senior_80):
    """Uses if–elif–else – exactly one branch executes."""
    if units <= 100:
        return "Full subsidy"
    elif 101 <= units <= 200:                   # chained comparison
        if ration_card:
            return "Partial subsidy"
        else:
            return "No subsidy (no ration card)"
    else:                                        # units > 200
        if senior_80:
            return "Subsidy (member > 80 yrs)"
        else:
            return "No subsidy"


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 : TEST HOUSEHOLDS
# ─────────────────────────────────────────────────────────────────────────────
households = [
    # (units, ration_card, senior_80, label)
    (80,  False, False, "HH1 – 80 units, no card, no senior"),
    (100, False, False, "HH2 – 100 units (boundary), no card"),
    (101, True,  False, "HH3 – 101 units (boundary), has card"),
    (101, False, False, "HH4 – 101 units (boundary), no card"),
    (150, True,  False, "HH5 – 150 units, has card"),
    (200, True,  False, "HH6 – 200 units (boundary), has card"),
    (201, True,  True,  "HH7 – 201 units (boundary), has card, senior"),
    (300, False, False, "HH8 – 300 units, no card, no senior"),
]

print("=" * 70)
print("SEPARATE IF STATEMENTS (may give multiple decisions):")
print("=" * 70)
for units, card, senior, label in households:
    result = subsidy_separate_if(units, card, senior)
    print(f"  {label}")
    print(f"    → {result}")

print()
print("=" * 70)
print("IF–ELIF–ELSE (exactly one decision):")
print("=" * 70)
for units, card, senior, label in households:
    result = subsidy_elif(units, card, senior)
    print(f"  {label}")
    print(f"    → {result}")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 : DESIGN DECISION – nested if vs combined Boolean conditions
# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 70)
print("DESIGN DECISION – Combined Boolean conditions (and/or):")
print("=" * 70)

def subsidy_combined(units, ration_card, senior_80):
    """Uses combined Boolean conditions (and / or) for clarity."""
    if units <= 100:
        return "Full subsidy"
    elif 101 <= units <= 200 and ration_card:
        return "Partial subsidy"
    elif 101 <= units <= 200 and not ration_card:
        return "No subsidy (no ration card)"
    elif units > 200 and senior_80:
        return "Subsidy (member > 80 yrs)"
    else:
        return "No subsidy"

# Combined Boolean is preferred: each condition is self-contained on one line,
# easier to read, test and change without touching nested indentation.

for units, card, senior, label in households:
    result = subsidy_combined(units, card, senior)
    print(f"  {label:50s} → {result}")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 : ALTERNATIVE – match–case (Python 3.10+)
# ─────────────────────────────────────────────────────────────────────────────
# match-case cannot directly match ranges, so we map units to a slab first.
# Time per decision: O(k) for k slabs (match checks guards sequentially).
# Space: O(1) – no extra data structure.
#
# Alternative 2 – lookup list of (upper_limit, decision_fn) searched in a loop:
# slabs = [(100, lambda u,c,s: "Full subsidy"),
#          (200, lambda u,c,s: "Partial subsidy" if c else "No subsidy"),
#          (float('inf'), lambda u,c,s: "Subsidy" if s else "No subsidy")]
# def subsidy_lookup(units, card, senior):
#     for limit, fn in slabs:
#         if units <= limit:
#             return fn(units, card, senior)
# Time: O(k) worst case (scan list). Space: O(k) for slab list.
#
# if–elif–else is O(k) worst case – same, but with zero extra memory (O(1)).
# CONCLUSION: if–elif–else is simplest and equally fast.

print()
print("All predictions matched observations. if–elif–else is the correct choice.")
print("match–case and lookup-list are O(k) time; if–elif–else is O(k) with O(1) space.")
