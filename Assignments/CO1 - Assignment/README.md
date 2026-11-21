# CSA08-<RegisterNumber>-Assignment1
## Ksheera Village Milk Producers' Co-operative – Payment Calculator

| Field | Detail |
|-------|--------|
| **Name** | `<Your Full Name>` |
| **Register Number** | `<Your Register Number>` |
| **Python Version** | Python 3.12 |
| **Course** | CSA08 – Python Programming |
| **Assignment** | Assignment 1 – CO1 |

---

## Libraries Used (all standard library – no pip install needed)

| Library | Purpose |
|---------|---------|
| `decimal` | Exact monetary arithmetic (Decimal from string) |
| `math` | floor(), ceil() for expression comparisons |
| `time` | perf_counter() for performance measurement |
| `timeit` | Accurate micro-benchmarks |
| `json` | JSON rate-card alternative (Task 11) |
| `random` | Synthetic test-data generation (Tasks 10, 11) |
| `sys` | sys.path, sys.getsizeof(), sys.modules |
| `pathlib` | Path handling for JSON file |
| `subprocess` | run_all.py task runner |

---

## Repository Structure

```
CSA08-<RegNo>-Assignment1/
├── README.md                        ← this file
├── run_all.py                       ← runs every task in sequence
│
├── Q1/   Task 1  – Problem Analysis
│   ├── task01_analysis.py
│   └── output.txt
│
├── Q2/   Task 2  – Values and Types
│   ├── task02_types.py              ← Complete the Code TODO 1 done
│   └── output.txt
│
├── Q3/   Task 3  – Variables and Constants
│   ├── task03_constants.py
│   └── output.txt
│
├── Q4/   Task 4  – Expressions
│   ├── task04_expressions.py
│   └── output.txt
│
├── Q5/   Task 5  – Input and Type Conversion
│   ├── task05_input.py
│   └── output.txt
│
├── Q6/   Task 6  – Functions
│   ├── task06_functions.py
│   └── output.txt
│
├── Q7/   Task 7  – Module
│   ├── milkrate.py                  ← reusable module (TODO 1 & 2 done)
│   ├── task07_use_module.py         ← imports and uses milkrate
│   └── output.txt
│
├── Q8/   Task 8  – Algorithmic Problem Solving
│   ├── task08_algorithm.py          ← pseudocode, flowchart, hand trace
│   └── output.txt
│
├── Q9/   Task 9  – Complete Calculator + Tests
│   ├── task09_calculator.py         ← 24/24 tests PASS
│   └── output.txt
│
├── Q10/  Task 10 – Expectation vs Execution
│   ├── task10_comparison.py         ← float vs Decimal, perf_counter, timeit
│   └── output.txt
│
├── Q11/  Task 11 – Final Recommendation
│   ├── task11_recommendation.py     ← JSON rate card, limitations, scalability
│   └── output.txt
│
└── Q12/  Task 12 – Day-4 Design Challenge
    ├── task12_design_challenge.py   ← seasonal rates, bonus, MODIFY decision
    └── output.txt
```

---

## How to Run

### Run every task at once
```bash
python run_all.py
```

### Run a single task
```bash
cd Q1 && python task01_analysis.py
cd Q2 && python task02_types.py
cd Q3 && python task03_constants.py
cd Q4 && python task04_expressions.py
cd Q5 && python task05_input.py
cd Q6 && python task06_functions.py
cd Q7 && python milkrate.py           # module self-test
cd Q7 && python task07_use_module.py  # module usage
cd Q8 && python task08_algorithm.py
cd Q9 && python task09_calculator.py
cd Q10 && python task10_comparison.py
cd Q11 && python task11_recommendation.py
cd Q12 && python task12_design_challenge.py
```

---

## Task Results Summary

| Task | File | Marks | Key Result |
|------|------|-------|------------|
| Q1  | task01_analysis.py | 4 | Identified inputs, outputs, constants, rules, O(n) complexity argument |
| Q2  | task02_types.py | 4 | TODO 1 complete; float=33400.300…061, Decimal=33400.30 exact |
| Q3  | task03_constants.py | 3 | UPPER_CASE constants, dynamic typing, magic-number vs dict comparison |
| Q4  | task04_expressions.py | 4 | 3 surprises documented; round() proven correct over int()/floor() |
| Q5  | task05_input.py | 3 | try/except handles "8,5","eight"," 8.5 "; aligned f-string table |
| Q6  | task06_functions.py | 4 | 4 functions with docstrings; return vs print; scope demo |
| Q7  | milkrate.py + task07_use_module.py | 4 | TODO 1 & 2 complete; exact expected output; __name__ guard explained |
| Q8  | task08_algorithm.py | 4 | SIMATS pseudocode, ASCII flowchart, hand trace, O(n)/O(1) analysis |
| Q9  | task09_calculator.py | 4 | **24/24 tests PASS** – normal, boundary, invalid, 5-entry verified |
| Q10 | task10_comparison.py | 4 | Decimal 3-5× slower but exact; per-payment rounding matches bank |
| Q11 | task11_recommendation.py | 4 | Decimal + per-payment rounding + single module recommended |
| Q12 | task12_design_challenge.py | 8 | MODIFY decision; seasonal SEASONS dict; bonus_payout(); 5 tests pass |
| **TOTAL** | | **50** | **All tasks complete and verified** |

---

## Key Design Decisions

1. **`Decimal(str(value))`** — exact monetary arithmetic; no IEEE-754 accumulation  
2. **`round()` for step counts** — prevents `7.000000000000002 → 6` bug  
3. **Single `milkrate.py` module** — rate revision = one file, all importers update  
4. **`try/except ValueError`** for input — EAFP style; handles locale commas/spaces  
5. **Task 12 decision: MODIFY** — core expressions correct; extend constants + 2 functions  

---


