"""Alternative: re-read all files for every student  O(s*f*l)  vs one pass  O(f*l)."""
import tempfile, time
from pathlib import Path
from attendance import parse_line

S, F, L = 100, 20, 100      # students, files, lines per file (L lines each; every student has a line)
tmp = Path(tempfile.mkdtemp())
for d in range(F):
    with open(tmp / f"attendance_d{d:02d}.txt", "w", encoding="utf-8") as f:
        for i in range(L):
            f.write(f"R{i:04d},2026-10-{d+1:02d},{'P' if (i + d) % 4 else 'A'}\n")
students = [f"R{i:04d}" for i in range(S)]

def one_pass():
    counts = {}
    for p in sorted(tmp.glob("attendance_*.txt")):
        with open(p, encoding="utf-8") as f:
            for line in f:
                r, d, st = parse_line(line)
                c = counts.setdefault(r, [0, 0]); c[1] += 1; c[0] += st == "P"
    return counts

def per_student():
    out = {}
    for s in students:
        pres = tot = 0
        for p in sorted(tmp.glob("attendance_*.txt")):
            with open(p, encoding="utf-8") as f:
                for line in f:
                    r, d, st = parse_line(line)
                    if r == s:
                        tot += 1; pres += st == "P"
        out[s] = [pres, tot]
    return out

t0 = time.perf_counter(); a = one_pass(); t1 = time.perf_counter() - t0
t0 = time.perf_counter(); b = per_student(); t2 = time.perf_counter() - t0
print(f"s={S}, f={F}, l={L}: lines parsed  one-pass={F*L}  per-student={S*F*L}")
print(f"one pass     : {t1*1000:8.1f} ms")
print(f"per student  : {t2*1000:8.1f} ms   ({t2/t1:.0f}x slower)")
print("same answer  :", a == b)
