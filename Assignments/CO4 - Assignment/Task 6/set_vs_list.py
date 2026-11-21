"""Alternative: duplicate detection with a list (O(n^2)) versus a set (O(n) average)."""
import sys, time

def with_list(regs):
    seen, dup = [], 0
    for r in regs:
        if r in seen: dup += 1
        else: seen.append(r)
    return dup, seen
def with_set(regs):
    seen, dup = set(), 0
    for r in regs:
        if r in seen: dup += 1
        else: seen.add(r)
    return dup, seen

print(f"{'n':>7} | {'list (s)':>9} | {'set (s)':>9} | {'ratio':>7} | {'list KiB':>9} | {'set KiB':>8}")
for n in (1000, 5000, 20000):
    regs = [f"{192300000 + (i * 7) % int(n * 0.9):09d}" for i in range(n)]     # ~10% duplicates
    t0 = time.perf_counter(); d1, s1 = with_list(regs); t1 = time.perf_counter() - t0
    t0 = time.perf_counter(); d2, s2 = with_set(regs);  t2 = time.perf_counter() - t0
    assert d1 == d2
    print(f"{n:>7} | {t1:>9.4f} | {t2:>9.5f} | {t1/t2:>6.0f}x | {sys.getsizeof(s1)/1024:>9.1f} | {sys.getsizeof(s2)/1024:>8.1f}")
