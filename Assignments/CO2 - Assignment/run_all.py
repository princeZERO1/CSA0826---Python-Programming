"""
Master runner – runs all Q1–Q7 and prints a summary.
Run: python3 run_all.py
"""
import subprocess, sys, time

questions = [
    ("Q1 – Subsidy Decisions",             "Q1/q1_subsidy.py"),
    ("Q2 – OTP Loop Verification",         "Q2/q2_otp.py"),
    ("Q3 – Vehicle Registration Validator","Q3/q3_vehicle.py"),
    ("Q4 – String Building Performance",   "Q4/q4_string_build.py"),
    ("Q5 – Canteen Order / Scope",         "Q5/q5_canteen.py"),
    ("Q6 – Temple Steps Recursion",        "Q6/q6_steps.py"),
    ("Q7 – Design Challenge",              "Q7/q7_design_challenge.py"),
]

print("=" * 65)
print("ASSIGNMENT 2 – CO2  MASTER RUNNER")
print("=" * 65)

all_ok = True
for label, path in questions:
    t0 = time.perf_counter()
    result = subprocess.run([sys.executable, path], capture_output=True, text=True)
    elapsed = time.perf_counter() - t0
    status = "✓ PASS" if result.returncode == 0 else "✗ FAIL"
    if result.returncode != 0:
        all_ok = False
    print(f"\n{'─'*65}")
    print(f"{status}  {label}  ({elapsed:.2f}s)")
    if result.returncode != 0:
        print("STDERR:", result.stderr[:300])

print("\n" + "=" * 65)
print("ALL QUESTIONS PASSED ✓" if all_ok else "SOME QUESTIONS FAILED ✗")
print("=" * 65)
