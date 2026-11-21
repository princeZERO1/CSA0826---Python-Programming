"""
Q6 – Recursion and Its Limits
Counting Ways to Climb Temple Steps

Base case  : n <= 1 → 1 way
Recursive  : ways(n) = ways(n-1) + ways(n-2)
(Same as Fibonacci offset by 1)

Bloom's Level: K5 – Evaluate
"""

import sys
import time
from functools import lru_cache

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 : HAND CALCULATION for n = 1..6
# ─────────────────────────────────────────────────────────────────────────────
# n=1: {1}            → 1 way
# n=2: {1+1, 2}       → 2 ways
# n=3: {1+1+1,1+2,2+1}→ 3 ways
# n=4: 5 ways
# n=5: 8 ways
# n=6: 13 ways
# Pattern: 1, 2, 3, 5, 8, 13 = Fibonacci(2..7)

EXPECTED = {1: 1, 2: 2, 3: 3, 4: 5, 5: 8, 6: 13}


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 : NAIVE RECURSIVE (Complete the Code – TODO 1 is in ways_memo)
# ─────────────────────────────────────────────────────────────────────────────
calls = 0

def ways_naive(n):
    """Plain recursion – O(φⁿ) time, O(n) stack space."""
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 : MEMOISED (TODO 1 completed)
# ─────────────────────────────────────────────────────────────────────────────
@lru_cache(maxsize=None)
def ways_memo(n):
    """Memoised recursion – O(n) time, O(n) cache + O(n) stack."""
    global calls
    calls += 1
    # TODO 1 completed: same base case and recursive case as ways_naive
    if n <= 1:
        return 1
    return ways_memo(n - 1) + ways_memo(n - 2)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 : CORRECTNESS CHECK n = 1..6
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 55)
print("CORRECTNESS CHECK  n = 1..6")
print("=" * 55)
for n, expected in EXPECTED.items():
    ways_memo.cache_clear()
    result = ways_memo(n)
    status = "✓" if result == expected else "✗"
    print(f"  ways({n}) = {result:4d}  expected {expected:4d}  {status}")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 : ASSIGNMENT REQUIRED OUTPUT (n=25)
# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 55)
print("REQUIRED OUTPUT")
print("=" * 55)
ways_memo.cache_clear()
calls = 0; result_naive = ways_naive(25); naive_calls = calls
calls = 0; result_memo  = ways_memo(25);  memo_calls  = calls

print(f"naive: {result_naive} calls = {naive_calls}")
print(f"memo : {result_memo}  calls = {memo_calls}")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6 : CALL TREE for n = 5 (illustrative)
# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 55)
print("CALL TREE for n=5 (naive – repeated work shown)")
print("=" * 55)
print("""
  ways(5)
  ├── ways(4)
  │   ├── ways(3)
  │   │   ├── ways(2)
  │   │   │   ├── ways(1) = 1
  │   │   │   └── ways(0) = 1
  │   │   └── ways(1) = 1   ← REPEATED
  │   └── ways(2)           ← REPEATED subtree
  │       ├── ways(1) = 1
  │       └── ways(0) = 1
  └── ways(3)               ← REPEATED subtree
      ├── ways(2)
      │   ├── ways(1) = 1
      │   └── ways(0) = 1
      └── ways(1) = 1

  ways(2) computed 3 times; ways(3) computed 2 times in naive version.
  Memoisation caches each subproblem → computed only ONCE.
""")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 7 : GROWTH INVESTIGATION – call counts at n=10,20,25,30
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 55)
print("GROWTH INVESTIGATION")
print("=" * 55)
print(f"{'n':>5}  {'naive calls':>14}  {'memo calls':>12}")
print("-" * 40)

for n in [10, 20, 25, 30]:
    ways_memo.cache_clear()
    calls = 0; ways_naive(n); nc = calls
    calls = 0; ways_memo(n);  mc = calls
    print(f"{n:>5}  {nc:>14,}  {mc:>12,}")

print("Naive: exponential O(φⁿ) ≈ O(1.618ⁿ)  Memo: O(n) calls each time")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 8 : ITERATIVE SOLUTION (alternative)
# ─────────────────────────────────────────────────────────────────────────────
def ways_loop(n):
    """
    Iterative – O(n) time, O(1) space.
    Keeps only the last two values.
    """
    if n <= 1:
        return 1
    a, b = 1, 2         # ways(1)=1, ways(2)=2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 9 : DEPLOYMENT DECISION – n = 1000 and RecursionError
# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 55)
print("DEPLOYMENT DECISION – n = 1000")
print("=" * 55)
print(f"Default recursion limit: {sys.getrecursionlimit()}")

# Try memoised recursive for n=1000
try:
    ways_memo.cache_clear()
    result_1000 = ways_memo(1000)
    print(f"ways_memo(1000) = {result_1000}")
except RecursionError as e:
    print(f"RecursionError for ways_memo(1000): {e}")
    print("→ Even memoised recursion hits the stack limit for large n.")

# Iterative always works
result_iter = ways_loop(1000)
print(f"ways_loop(1000) = {result_iter}")
print(f"Match: {result_iter == result_1000 if 'result_1000' in dir() else 'memo failed'}")

print("""
DECISION:
  • Raising sys.setrecursionlimit: risky – can cause segfault for very large n;
    not recommended for production.
  • Rewriting with a loop: O(n) time, O(1) space; no stack limit concern.
    PREFERRED for n > 500.
  • Both: use lru_cache for small n (simpler code), loop for large n.
  • FINAL RECOMMENDATION: iterative solution for n up to 1,000 or beyond.
""")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 10 : TIMING COMPARISON
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 55)
print("TIMING COMPARISON (n=25 each, 10,000 repetitions)")
print("=" * 55)

REPS = 10_000

t0 = time.perf_counter()
for _ in range(REPS):
    ways_naive(25)
t_naive = time.perf_counter() - t0

ways_memo.cache_clear()
t0 = time.perf_counter()
for _ in range(REPS):
    ways_memo(25)
t_memo = time.perf_counter() - t0

t0 = time.perf_counter()
for _ in range(REPS):
    ways_loop(25)
t_loop = time.perf_counter() - t0

print(f"  Naive      {REPS} calls: {t_naive:.4f} s")
print(f"  Memoised   {REPS} calls: {t_memo:.4f} s")
print(f"  Iterative  {REPS} calls: {t_loop:.4f} s")
print(f"\n  Speedup memo vs naive: {t_naive/t_memo:.1f}×")
print(f"  Speedup loop vs naive: {t_naive/t_loop:.1f}×")

print("""
COMPLEXITY SUMMARY:
  Naive      : O(φⁿ) ≈ O(1.618ⁿ) time  O(n) stack
  Memoised   : O(n)  time              O(n) cache + O(n) stack
  Iterative  : O(n)  time              O(1) space  ← best for large n
""")
