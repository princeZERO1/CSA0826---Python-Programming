"""
Task 8 – Plan the Algorithm Before Coding
  • Pseudocode for one payment and ten-day total
  • Hand trace for three entries
  • Algorithmic problem-solving steps: Understand → Plan → Write → Test
  • Complexity: list accumulation O(n) space vs running total O(1) space
"""

SEP = "=" * 64

print(SEP)
print("TASK 8 – Algorithmic Problem Solving")
print(SEP)

PSEUDOCODE = """
══════════════════════════════════════════════════════════════════
SIMATS Engineering – Standard Algorithmic Pseudocode

PROGRAM: MilkPaymentCalculator
══════════════════════════════════════════════════════════════════

CONSTANTS:
    BASE_RATE      ← 30.00
    FAT_STEP_VALUE ← 0.40
    SNF_STEP_VALUE ← 0.30
    FAT_STD        ← 3.5
    SNF_STD        ← 8.5
    STEP_SIZE      ← 0.1
    FAT_MIN        ← 2.0,  FAT_MAX ← 7.0
    SNF_MIN        ← 7.0,  SNF_MAX ← 10.0

──────────────────────────────────────────────────────────────────
MODULE: VALIDATE(litres, fat, snf)
──────────────────────────────────────────────────────────────────
BEGIN
    IF litres ≤ 0 THEN
        RETURN FALSE, "Litres must be positive"
    END IF
    IF fat < FAT_MIN OR fat > FAT_MAX THEN
        RETURN FALSE, "Fat out of range"
    END IF
    IF snf < SNF_MIN OR snf > SNF_MAX THEN
        RETURN FALSE, "SNF out of range"
    END IF
    RETURN TRUE, "OK"
END MODULE

──────────────────────────────────────────────────────────────────
MODULE: RATE_PER_LITRE(fat, snf)
──────────────────────────────────────────────────────────────────
BEGIN
    fat_steps ← ROUND((fat - FAT_STD) / STEP_SIZE)
    snf_steps ← ROUND((snf - SNF_STD) / STEP_SIZE)
    rate      ← BASE_RATE
                + fat_steps × FAT_STEP_VALUE
                + snf_steps × SNF_STEP_VALUE
    RETURN ROUND(rate, 2)
END MODULE

──────────────────────────────────────────────────────────────────
MODULE: PAYOUT(litres, fat, snf)
──────────────────────────────────────────────────────────────────
BEGIN
    (valid, reason) ← VALIDATE(litres, fat, snf)
    IF NOT valid THEN
        RAISE ERROR reason
    END IF
    rate   ← RATE_PER_LITRE(fat, snf)
    amount ← ROUND(rate × litres, 2)
    RETURN amount
END MODULE

──────────────────────────────────────────────────────────────────
MODULE: TEN_DAY_TOTAL(entries)
──────────────────────────────────────────────────────────────────
BEGIN
    total ← 0.00
    FOR EACH (litres, fat, snf) IN entries DO
        TRY
            amount ← PAYOUT(litres, fat, snf)
            total  ← total + amount
        CATCH error
            PRINT "Skipping invalid entry: " + error
        END TRY
    END FOR
    RETURN ROUND(total, 2)
END MODULE

──────────────────────────────────────────────────────────────────
MAIN
──────────────────────────────────────────────────────────────────
BEGIN
    entries ← empty list
    PRINT header
    FOR i FROM 1 TO number_of_entries DO
        READ farmer_id, litres, fat, snf, shift
        APPEND (litres, fat, snf) TO entries
    END FOR
    total ← TEN_DAY_TOTAL(entries)
    PRINT "Ten-day total: Rs " + total
END
══════════════════════════════════════════════════════════════════
"""
print(PSEUDOCODE)

# ════════════════════════════════════════════════════════════════
# FLOWCHART (text representation)
# ════════════════════════════════════════════════════════════════
FLOWCHART = """
── Flowchart: Validating One Entry ──────────────────────────────

     ┌─────────────────────┐
     │       START         │
     └──────────┬──────────┘
                │
                ▼
     ┌─────────────────────┐
     │  Read litres, fat,  │
     │  snf from clerk     │
     └──────────┬──────────┘
                │
                ▼
     ◇─────────────────────◇
     │   litres > 0 ?       │──── NO ──► Print "Litres must be positive" ─┐
     ◇─────────────────────◇                                               │
          │ YES                                                             │
          ▼                                                                 │
     ◇───────────────────────◇                                             │
     │  2.0 ≤ fat ≤ 7.0 ?    │── NO ──► Print "Fat out of range" ─────────┤
     ◇───────────────────────◇                                             │
          │ YES                                                             │
          ▼                                                                 │
     ◇───────────────────────◇                                             │
     │  7.0 ≤ snf ≤ 10.0 ?   │── NO ──► Print "SNF out of range" ─────────┤
     ◇───────────────────────◇                                             │
          │ YES                                                             │
          ▼                                                                 │
     ┌─────────────────────┐                                               │
     │  Compute rate and   │      ◄────────────────────────────────────────┘
     │  payout; add to     │      (loop back to Read next entry)
     │  ten-day total      │
     └──────────┬──────────┘
                │
                ▼
     ◇─────────────────────◇
     │  More entries ?      │──── YES ──► (back to Read)
     ◇─────────────────────◇
          │ NO
          ▼
     ┌─────────────────────┐
     │  Print ten-day      │
     │  total              │
     └──────────┬──────────┘
                │
                ▼
     ┌─────────────────────┐
     │        END          │
     └─────────────────────┘
"""
print(FLOWCHART)

# ════════════════════════════════════════════════════════════════
# HAND TRACE
# ════════════════════════════════════════════════════════════════
print("── Hand Trace for Three Entries ─────────────────────────────\n")

BASE_RATE      = 30.00
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30
FAT_STD        = 3.5
SNF_STD        = 8.5
STEP_SIZE      = 0.1

entries = [
    (10.0, 3.5, 8.5),
    (8.5,  4.2, 8.7),
    (12.0, 3.1, 8.3),
]

total = 0.0
for i, (litres, fat, snf) in enumerate(entries, 1):
    fat_steps = round((fat - FAT_STD) / STEP_SIZE)
    snf_steps = round((snf - SNF_STD) / STEP_SIZE)
    rate  = round(BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE, 2)
    amount = round(rate * litres, 2)
    total += amount

    print(f"  Entry {i}: litres={litres}, fat={fat}, snf={snf}")
    print(f"    fat_steps = round(({fat} - {FAT_STD}) / {STEP_SIZE}) = {fat_steps}")
    print(f"    snf_steps = round(({snf} - {SNF_STD}) / {STEP_SIZE}) = {snf_steps}")
    print(f"    rate  = {BASE_RATE} + {fat_steps}×{FAT_STEP_VALUE} "
          f"+ {snf_steps}×{SNF_STEP_VALUE} = {rate}")
    print(f"    amount = {rate} × {litres} = {amount}")
    print(f"    running total so far = {round(total, 2)}\n")

print(f"  Final ten-day total = Rs {round(total, 2)}")

# ════════════════════════════════════════════════════════════════
# COMPLEXITY ANALYSIS
# ════════════════════════════════════════════════════════════════
print("""
── Complexity Analysis: list vs running total ─────────────────────

  Approach A – Store ALL entries, sum at end:
    entries = []
    for each entry: entries.append(...)      # O(1) amortised
    total = sum(payout(*e) for e in entries) # O(n)
    Time:  O(n)   Space: O(n) – stores every entry in RAM

  Approach B – Running total (stream processing):
    total = 0
    for each entry: total += payout(...)     # O(n) total, O(1) space
    Time:  O(n)   Space: O(1) – stores only the running sum

  For 150,000 entries × 3 floats × 8 bytes each ≈ 3.6 MB for Approach A.
  Approach B uses a few dozen bytes regardless of n.

  When is storing the list necessary?
    • To re-print the full ledger after all entries are read.
    • To sort by farmer ID or by amount.
    • To detect duplicates or recompute if the rate card changes.
  If only the total is needed, Approach B (running total) is preferable.
""")
