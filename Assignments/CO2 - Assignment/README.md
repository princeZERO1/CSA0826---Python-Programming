# CSA08 – Assignment 2 (CO2)
## Control Flow, String Operations and Functions

**Name:** [Your Name]  
**Register Number:** [Your Register Number]  
**Python Version:** Python 3.12  
**Libraries Used:** `functools`, `re`, `time`, `io`, `sys` (all standard library – no pip install needed)

---

## Repository Structure

```
Assignment2/
├── Q1/  q1_subsidy.py        – if, if-elif-else, chained comparisons
├── Q2/  q2_otp.py            – while, for, break, continue, pass, loop-else
├── Q3/  q3_vehicle.py        – string operations, slicing, normalise/validate
├── Q4/  q4_string_build.py   – string building, immutability, join() vs +=
├── Q5/  q5_canteen.py        – functions, default parameters, scope
├── Q6/  q6_steps.py          – recursion, memoisation, lru_cache, iterative
├── Q7/  q7_design_challenge.py – diagnose, redesign, validate (Q6 chosen)
└── README.md
```

---

## How to Run Each Program

```bash
python3 Q1/q1_subsidy.py
python3 Q2/q2_otp.py
python3 Q3/q3_vehicle.py
python3 Q4/q4_string_build.py
python3 Q5/q5_canteen.py
python3 Q6/q6_steps.py
python3 Q7/q7_design_challenge.py
```

No external packages required. All programs use the Python standard library only.

---

## Results Summary

### Q1 – State Electricity Subsidy Eligibility
- Demonstrated that **separate `if` statements** can assign multiple decisions to one household (more than one branch executes).
- **`if–elif–else`** guarantees exactly one decision per household.
- Used chained comparisons: `101 <= units <= 200`.
- Tested all 8 boundary households including units = 100, 101, 200, 201.
- **Design decision:** Combined Boolean conditions (`and`/`or`) preferred – each rule is self-contained on one line.
- **Complexity:** `if–elif–else` and alternatives (match-case, lookup-list) are all O(k) for k slabs; `if–elif–else` uses O(1) extra space.

### Q2 – OTP Verification at a Bank Kiosk
- **`while` loop** is more natural: blank entries truly do not consume an attempt (counter only incremented after confirming non-blank and wrong).
- **`for` loop** with `range(3)` consumes a slot even when `continue` skips the body.
- Demonstrated `break` (success), `continue` (blank entry), `pass` (placeholder), and `loop-else` (account lock).
- **Bug:** updating the counter before the blank check causes blank entries to count.
- Extended design: `while` with dynamic `max_attempts` handles 2 extra attempts cleanly.
- **Recursive alternative:** O(a) time, O(a) stack space vs O(1) space for loops.

### Q3 – Vehicle Registration Number Validator
- `normalise()`: removes spaces/hyphens with `.replace()`, converts to upper with `.upper()`.
- `is_valid()`: checks length (9 or 10), slices each part, uses `.isalpha()` / `.isdigit()`.
- `format_receipt()`: formats as `"TN 09 AB 1234"` or `"KA 01 M 0007"`.
- Output matches expected exactly.
- Slicing: `s[-4:]` = last 4 digits; `s[4:-4]` = series letters.
- Strings are immutable: `.upper()` returns a **new** object; original unchanged.
- **Regex alternative** agrees on all 6 test cases; both O(L) time.

### Q4 – Building Long Text
- `build_join()` completed with `";".join(parts) + ";"`.
- Output: `same text: True | length: 3048890` ✓
- **Measured times (200,000 items, averages over 3 runs):**

| Size    | avg +=(s) | avg join(s) | avg fstring(s) |
|---------|-----------|-------------|----------------|
| 1,000   | 0.0001    | 0.0000      | 0.0001         |
| 10,000  | 0.0009    | 0.0002      | 0.0007         |
| 200,000 | ~0.015    | ~0.004      | ~0.016         |

- `join()` is 3–4× faster than `+=` and always O(n); `+=` is O(n²) in theory (O(n) with CPython optimisation, but unreliable).

### Q5 – College Canteen Order System
- **Bug explained:** `order=[]` creates one list at definition time; all calls share it.
- **Fix (TODO 1):** `if order is None: order = []` creates a fresh list each call.
- Output matches exactly: `['Tea', 'Vada'] ['Tea', 'Vada']` / `['Tea'] ['Vada']` ✓
- `add_item_buggy.__defaults__` shows the accumulated list after calls.
- Demonstrated: positional, keyword, default parameters; multiple return values (tuple); local/global/nonlocal scope; `global` keyword and why it's avoided.
- Three independent customer orders verified.

### Q6 – Counting Ways to Climb Temple Steps
- Base case: `n <= 1 → 1`; Recursive: `ways(n) = ways(n-1) + ways(n-2)`.
- Hand-calculated n=1..6: 1, 2, 3, 5, 8, 13 – all verified ✓.
- Required output: `naive: 121393 calls = 242785` / `memo: 121393 calls = 26` ✓
- Call tree for n=5 shows `ways(2)` computed 3 times, `ways(3)` twice in naive.
- Growth: naive O(φⁿ), memo O(n) calls.
- `ways_memo(1000)` raises `RecursionError` (limit = 1000).
- **Decision:** iterative solution (O(n) time, O(1) space) for n > 500.

### Q7 – Design Challenge (Q6 Naive Recursion selected)
- **Diagnosed:** 166 of 177 calls for n=10 are wasted repeats; O(φⁿ) growth.
- **Objective:** reduce to O(n) calls, verified by instrumented call counting.
- **Redesigns:** memoised (lru_cache, O(n) cache) + iterative (O(1) space).
- **Validated:** n=30 → naive 2,692,537 calls vs memo 31 calls (87,000× fewer).
- Timing speedup at n=30: memo ~1,200,000× faster than naive.
- Iterative solves n=1000 successfully; both recursive versions hit RecursionError.
- **Final recommendation:** iterative for production; lru_cache for moderate n ≤ 900.

---

## Key Takeaways

| Topic | Key Finding |
|-------|-------------|
| `if-elif-else` | Exactly one branch executes; prevents double-subsidy bugs |
| `while` vs `for` | `while` preferred when loop count depends on runtime conditions |
| String immutability | Every `+=` may copy; `join()` is always O(n) and recommended |
| Mutable default args | Use `None` sentinel, not `[]` as default parameter |
| Recursion limit | Python default is 1000; use iterative for large n |
| Memoisation | Reduces O(φⁿ) to O(n) by caching overlapping subproblems |
