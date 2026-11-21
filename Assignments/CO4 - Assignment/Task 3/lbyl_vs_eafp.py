"""Alternative: EAFP (try/except) vs LBYL (if checks), rare and common bad lines."""
import timeit
def eafp(line):
    try:
        reg, date, status = line.split(",")
        if status not in ("P", "A"):
            raise ValueError
        return True
    except ValueError:
        return False
def lbyl(line):
    parts = line.split(",")
    if len(parts) != 3 or parts[2] not in ("P", "A"):
        return False
    return True

good, bad = "192311001,2026-10-08,P", "192311003,2026-10-08"
for name, mix in (("rare bad (0%)", [good] * 1000), ("common bad (50%)", [good, bad] * 500)):
    for fn in (eafp, lbyl):
        t = timeit.timeit(lambda: [fn(x) for x in mix], number=300) / 300
        print(f"{name:17s} {fn.__name__:6s}: {t/len(mix)*1e9:7.1f} ns per line")
