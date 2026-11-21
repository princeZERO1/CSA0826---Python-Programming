"""
Q7 – Day-4 Design Challenge: Diagnose, Redesign and Validate
Selected Program: Q6 – ways_naive (plain recursive step counter)

The naive recursive solution has exponential time complexity O(φⁿ).
This challenge diagnoses the bottleneck, redesigns with memoisation AND
the iterative approach, and validates both with measurements.

Bloom's Level: K5 – Evaluate
"""

import sys
import time
from functools import lru_cache

# ═══════════════════════════════════════════════════════════════════════════
# A. DIAGNOSE THE BOTTLENECK
# ═══════════════════════════════════════════════════════════════════════════
print("=" * 65)
print("A. DIAGNOSE THE BOTTLENECK")
print("=" * 65)

call_log = {}   # n → how many times computed

def ways_naive_traced(n):
    """Naive recursion with per-subproblem call counting."""
    call_log[n] = call_log.get(n, 0) + 1
    if n <= 1:
        return 1
    return ways_naive_traced(n - 1) + ways_naive_traced(n - 2)

call_log.clear()
result = ways_naive_traced(10)
print(f"ways_naive(10) = {result}")
print(f"\nSubproblem recomputation count (how many times each n was computed):")
for k in sorted(call_log.keys(), reverse=True):
    bar = "█" * call_log[k]
    print(f"  ways({k:2d}): {call_log[k]:4d} times  {bar}")

total_calls = sum(call_log.values())
print(f"\nTotal calls: {total_calls}")
print(f"Distinct subproblems: {len(call_log)}")
print(f"Wasted calls (repeats): {total_calls - len(call_log)}")

print("""
DIAGNOSIS:
  • Most work is in re-computing already-solved subproblems.
  • For ways_naive(n), the number of calls grows as O(φⁿ) ≈ O(1.618ⁿ).
  • ways(2) is computed 34 times for n=10; ways(3) 21 times; etc.
  • The count that grows with input: total function calls = 2·ways(n+1) - 1.
  • Work IS unnecessarily repeated: the same (n-1) and (n-2) subtrees
    are recomputed independently every time they appear.
  • Bottleneck: the absence of result caching for already-solved subproblems.
""")

# ═══════════════════════════════════════════════════════════════════════════
# B. DEFINE THE DESIGN OBJECTIVE
# ═══════════════════════════════════════════════════════════════════════════
print("=" * 65)
print("B. DEFINE THE DESIGN OBJECTIVE")
print("=" * 65)
print("""
MEASURABLE OBJECTIVE:
  Reduce the number of function calls from O(φⁿ) to O(n) for the same
  output by ensuring each distinct subproblem ways(k) is computed at
  most ONCE.

  Specific target: for n=30, reduce calls from ~2,692,537 to exactly 31.
  For n=1000, produce the correct answer without a RecursionError, in
  under 1 ms (iterative target).

  Primary metric : call count (from call_log instrumentation).
  Secondary metric: wall-clock time measured with time.perf_counter().
""")

# ═══════════════════════════════════════════════════════════════════════════
# C. DESIGN THE REVISED SOLUTION
# ═══════════════════════════════════════════════════════════════════════════
print("=" * 65)
print("C. DESIGN THE REVISED SOLUTION")
print("=" * 65)
print("""
WHAT CHANGED:
  • Memoisation (lru_cache): store the result of ways(k) the first time
    it is computed; return the cached value on subsequent calls.
    Property exploited: overlapping subproblems (dynamic programming).
    Extra memory: O(n) cache entries.
    New trade-off: O(n) stack depth → RecursionError for large n.

  • Iterative (loop): eliminate recursion entirely; keep only the two
    most recent values (a, b).
    Property exploited: each result depends only on the previous two.
    Extra memory: O(1) – two variables only.
    No new trade-off beyond O(n) time.

PSEUDOCODE – Memoised:
  function ways_memo(n):
      if n in cache: return cache[n]
      if n <= 1: return 1
      result = ways_memo(n-1) + ways_memo(n-2)
      cache[n] = result
      return result

PSEUDOCODE – Iterative:
  function ways_loop(n):
      if n <= 1: return 1
      a = 1, b = 2          // ways(1), ways(2)
      for i from 3 to n:
          a, b = b, a + b   // slide window
      return b

FLOWCHART (iterative):
  START → n <= 1? → YES → return 1
              ↓ NO
         a=1, b=2, i=3
              ↓
         i <= n? → NO → return b
              ↓ YES
         a,b = b, a+b ; i++
              ↑_____________|
""")

# ═══════════════════════════════════════════════════════════════════════════
# D. PREDICT BEFORE IMPLEMENTING
# ═══════════════════════════════════════════════════════════════════════════
print("=" * 65)
print("D. PREDICT BEFORE IMPLEMENTING")
print("=" * 65)
print("""
PREDICTION:
  For n=30:
    Naive   : ~2,692,537 calls, ~several seconds for 10,000 repetitions.
    Memoised: exactly 31 calls (first call), 1 call (cached thereafter).
    Iterative: 0 recursive calls; O(n) loop iterations; fastest wall time.

  Speedup memo vs naive for n=30: approximately 10,000× – 100,000×.
  Speedup loop vs naive for n=30: approximately same order as memo.

  For n=1000:
    Naive & Memo (recursive): RecursionError (stack limit ~1000).
    Iterative: succeeds in O(n) time, O(1) space, no error.
""")

# ═══════════════════════════════════════════════════════════════════════════
# E. IMPLEMENT AND VALIDATE
# ═══════════════════════════════════════════════════════════════════════════
print("=" * 65)
print("E. IMPLEMENT AND VALIDATE")
print("=" * 65)

# ── Redesigned solution 1: Memoised ──────────────────────────────────────
memo_calls_log = {}

@lru_cache(maxsize=None)
def ways_memo(n):
    memo_calls_log[n] = memo_calls_log.get(n, 0) + 1
    if n <= 1:
        return 1
    return ways_memo(n - 1) + ways_memo(n - 2)

# ── Redesigned solution 2: Iterative ─────────────────────────────────────
def ways_loop(n):
    if n <= 1:
        return 1
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b

# ── Call-count comparison ─────────────────────────────────────────────────
print(f"\n{'n':>5}  {'naive calls':>14}  {'memo calls':>12}  {'loop iters':>12}  {'answer':>8}")
print("-" * 60)

naive_call_counts = {10: 177, 20: 21891, 25: 242785, 30: 2692537}  # from Q6

for n in [10, 20, 25, 30]:
    ways_memo.cache_clear()
    memo_calls_log.clear()

    naive_c = naive_call_counts[n]
    r_memo  = ways_memo(n)
    memo_c  = sum(memo_calls_log.values())
    loop_i  = max(0, n - 2)   # loop runs from 3..n → (n-2) iterations

    print(f"{n:>5}  {naive_c:>14,}  {memo_c:>12,}  {loop_i:>12,}  {r_memo:>8,}")

# ── Timing comparison at three sizes ─────────────────────────────────────
print()
print(f"{'n':>5}  {'naive(s)':>12}  {'memo(s)':>10}  {'loop(s)':>10}  {'speedup memo':>14}")
print("-" * 60)

REPS = 500

for n in [10, 20, 30]:
    # Naive timing
    t0 = time.perf_counter()
    for _ in range(REPS):
        ways_naive_traced.__wrapped__ if hasattr(ways_naive_traced, '__wrapped__') else None
        # re-use the original naive (without call_log overhead for fair timing)
        pass
    # Use a clean naive for timing
    def _naive(n):
        if n <= 1: return 1
        return _naive(n-1) + _naive(n-2)

    t0 = time.perf_counter()
    for _ in range(REPS): _naive(n)
    t_naive = time.perf_counter() - t0

    # Memo timing (cache warm)
    ways_memo.cache_clear()
    ways_memo(n)   # warm up
    t0 = time.perf_counter()
    for _ in range(REPS): ways_memo(n)
    t_memo = time.perf_counter() - t0

    # Loop timing
    t0 = time.perf_counter()
    for _ in range(REPS): ways_loop(n)
    t_loop = time.perf_counter() - t0

    speedup = t_naive / t_memo if t_memo > 0 else float('inf')
    print(f"{n:>5}  {t_naive:>12.5f}  {t_memo:>10.6f}  {t_loop:>10.6f}  {speedup:>14.1f}×")

# ── Correctness: all three must agree ─────────────────────────────────────
print()
print("CORRECTNESS CHECK (n = 1..15):")
all_match = True
for n in range(1, 16):
    ways_memo.cache_clear()
    r_naive = _naive(n)
    r_memo  = ways_memo(n)
    r_loop  = ways_loop(n)
    if not (r_naive == r_memo == r_loop):
        print(f"  MISMATCH at n={n}: naive={r_naive} memo={r_memo} loop={r_loop}")
        all_match = False
if all_match:
    print("  ✓ All three versions agree for n = 1..15.")

# ── Deployment: n=1000 ───────────────────────────────────────────────────
print()
print("DEPLOYMENT TEST – n = 1000:")
print(f"  Default sys.getrecursionlimit() = {sys.getrecursionlimit()}")

try:
    ways_memo.cache_clear()
    r = ways_memo(1000)
    print(f"  ways_memo(1000) succeeded (len={len(str(r))} digits)")
except RecursionError:
    print("  ways_memo(1000) → RecursionError (stack exhausted even with cache)")

r_loop_1000 = ways_loop(1000)
print(f"  ways_loop(1000) = ...{str(r_loop_1000)[-20:]} ({len(str(r_loop_1000))} digits) ✓")

# ═══════════════════════════════════════════════════════════════════════════
# F. DEFEND THE FINAL DESIGN
# ═══════════════════════════════════════════════════════════════════════════
print()
print("=" * 65)
print("F. DEFEND THE FINAL DESIGN")
print("=" * 65)
print("""
OBJECTIVE ACHIEVED?
  ✓ Call count reduced from O(φⁿ) to O(n) for memoised, O(n) iterations
    for the loop – both match the stated objective exactly.
  ✓ n=30: memo calls dropped from 2,692,537 to 31 (87,000× fewer).
  ✓ Wall-clock speedup: memo is thousands of times faster than naive.
  ✓ Iterative handles n=1000 (and beyond) without RecursionError.

SIZE OF IMPROVEMENT:
  For n=30: memo reduces calls by factor ~86,856×.
  Timing shows memo ≈ comparable to loop when cache is warm (both O(1)
  per call after first compute); loop is slightly faster cold-start
  for large n because it has zero function-call overhead.

NEW COSTS INTRODUCED:
  • Memoised: O(n) cache memory; still hits RecursionError for large n
    (n > ~990 on a default Python installation).
  • Iterative: loses the elegant recursive structure; slightly more code
    to understand at first glance.

WHERE ORIGINAL MAY STILL BE PREFERRED:
  • For tiny n (n ≤ 10), the naive version is readable and fast enough.
  • The recursive structure directly mirrors the mathematical definition,
    making it easier to verify correctness by inspection.

FINAL RECOMMENDATION:
  Use the ITERATIVE solution for production (n up to 1,000+):
    – O(n) time, O(1) space, no stack risk.
  Use MEMOISED (lru_cache) for moderate n (up to ~900) when code clarity
  matters more than memory.
  Avoid the NAIVE version for n > 25 in any production context.
""")
