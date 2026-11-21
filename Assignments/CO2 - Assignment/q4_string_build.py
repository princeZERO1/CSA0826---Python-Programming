"""
Q4 – Building Long Text: + or join()?
Monthly SMS Bill Statement

Methods:
  (a) repeated += inside a loop
  (b) list of parts + "".join()
  (c) f-string for each line + join

Bloom's Level: K4 – Analyse
"""

import time

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 : Three implementations
# ─────────────────────────────────────────────────────────────────────────────

def build_plus(parts):
    """(a) Repeated += – O(n²) characters copied in worst case."""
    text = ""
    for p in parts:
        text += p + ";"
    return text


def build_join(parts):
    """(b) List then join – O(n) always."""
    # TODO 1 completed: build same text with one join call
    return ";".join(parts) + ";"


def build_fstring(parts):
    """(c) f-string per line, collected in list, then joined."""
    lines = [f"{p};" for p in parts]
    return "".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 : Correctness check with 200,000 items (assignment requirement)
# ─────────────────────────────────────────────────────────────────────────────
items = [f"Item{i}:Rs{i % 50}" for i in range(200_000)]

start = time.perf_counter(); a = build_plus(items);    t_plus    = time.perf_counter() - start
start = time.perf_counter(); b = build_join(items);    t_join    = time.perf_counter() - start
start = time.perf_counter(); c = build_fstring(items); t_fstring = time.perf_counter() - start

print("same text (plus vs join)   :", a == b, "| length:", len(b))
print("same text (plus vs fstring):", a == c, "| length:", len(c))
print(f"+= time:      {t_plus:.4f} s")
print(f"join time:    {t_join:.4f} s")
print(f"fstring time: {t_fstring:.4f} s")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 : Scaling experiment – 1,000 / 10,000 / 200,000 lines × 3 runs
# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 65)
print("SCALING EXPERIMENT (3 runs each, averages reported)")
print("=" * 65)
print(f"{'Size':>10}  {'avg +=(s)':>12}  {'avg join(s)':>12}  {'avg fstr(s)':>12}")
print("-" * 65)

SIZES = [1_000, 10_000, 200_000]
RUNS  = 3

for size in SIZES:
    data = [f"Item{i}:Rs{i % 50}" for i in range(size)]
    times_plus    = []
    times_join    = []
    times_fstring = []

    for _ in range(RUNS):
        t0 = time.perf_counter(); build_plus(data);    times_plus.append(time.perf_counter() - t0)
        t0 = time.perf_counter(); build_join(data);    times_join.append(time.perf_counter() - t0)
        t0 = time.perf_counter(); build_fstring(data); times_fstring.append(time.perf_counter() - t0)

    avg_p = sum(times_plus)    / RUNS
    avg_j = sum(times_join)    / RUNS
    avg_f = sum(times_fstring) / RUNS
    print(f"{size:>10}  {avg_p:>12.4f}  {avg_j:>12.4f}  {avg_f:>12.4f}")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 : EXPLANATION – string immutability and CPython optimisation
# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 65)
print("EXPLANATION")
print("=" * 65)
print("""
String immutability means every += creates a NEW string object, copying
all previous characters plus the new segment.  For n parts of average
length L:
  Total characters copied ≈ L + 2L + 3L + … + nL = O(n² · L)

CPython sometimes optimises += when the left-hand string has only ONE
reference, performing an in-place resize.  This can make += appear O(n)
in simple loops.  However, this optimisation is an implementation detail
– it may not fire when the string is referenced elsewhere, inside functions
or under other conditions.  join() is ALWAYS O(n) regardless of CPython
version or reference count.

join() pre-computes the total length, allocates once, and fills the buffer
→ recommended practice for building long strings.
""")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 : ALTERNATIVE – io.StringIO
# ─────────────────────────────────────────────────────────────────────────────
import io

def build_stringio(parts):
    """Alternative: write to StringIO buffer – O(n), O(n) memory."""
    buf = io.StringIO()
    for p in parts:
        buf.write(p)
        buf.write(";")
    return buf.getvalue()

start = time.perf_counter()
d = build_stringio(items)
t_sio = time.perf_counter() - start

print(f"io.StringIO time (200k): {t_sio:.4f} s")
print(f"same as join: {b == d}")

print("""
ALTERNATIVE ANALYSIS:
  File write (line by line): O(n) time; memory O(1) per line (streamed).
    Trade-off: requires disk I/O; slower than in-memory join.
  io.StringIO: O(n) time; O(n) memory like join but no disk.
    Good when you need incremental building + final extraction.
  join(): O(n) time; O(n) memory; simplest and fastest for in-memory use.

CONCLUSION: Use join() for in-memory statement building.
  Use file write / StringIO only when you must stream output or the
  result is too large to hold entirely in RAM.
""")
