"""
run_all.py  –  Runs every task in order and prints a summary.
Usage:  python run_all.py
"""

import subprocess, sys, os, time

TASKS = [
    ("Q1",  "task01_analysis.py",       "Problem Analysis"),
    ("Q2",  "task02_types.py",          "Values and Types"),
    ("Q3",  "task03_constants.py",      "Variables and Constants"),
    ("Q4",  "task04_expressions.py",    "Expressions"),
    ("Q5",  "task05_input.py",          "Input and Type Conversion"),
    ("Q6",  "task06_functions.py",      "Functions"),
    ("Q7",  "milkrate.py",              "Module – self-test"),
    ("Q7",  "task07_use_module.py",     "Module – usage script"),
    ("Q8",  "task08_algorithm.py",      "Algorithm Design"),
    ("Q9",  "task09_calculator.py",     "Complete Calculator + Tests"),
    ("Q10", "task10_comparison.py",     "Expectation vs Execution"),
    ("Q11", "task11_recommendation.py", "Final Recommendation"),
    ("Q12", "task12_design_challenge.py","Design Challenge"),
]

BASE = os.path.dirname(os.path.abspath(__file__))
SEP  = "=" * 70

passed = failed = 0

print(SEP)
print("  CSA08 Assignment 1 – Ksheera Milk Co-operative Payment Calculator")
print("  Running all tasks …")
print(SEP)

for folder, script, title in TASKS:
    cwd = os.path.join(BASE, folder)
    t0  = time.perf_counter()
    res = subprocess.run(
        [sys.executable, script],
        capture_output=True, text=True, cwd=cwd
    )
    elapsed = time.perf_counter() - t0
    ok = res.returncode == 0
    status = "PASS" if ok else "FAIL"
    if ok: passed += 1
    else:  failed += 1
    print(f"  [{status}] {folder}/{script:<35} {title}  ({elapsed:.3f}s)")
    if not ok:
        print("         STDERR:", res.stderr[:200])

print(SEP)
print(f"  Results: {passed} passed, {failed} failed out of {passed+failed} tasks")
print(SEP)
