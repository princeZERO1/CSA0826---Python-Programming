"""Task 2: monthly attendance processor (read every daily file once, accumulate in dicts)."""
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data" / "2026-10"
OUT_DIR = Path(__file__).parent / "reports"
THRESHOLD = 75.0


def parse_line(line):
    """'192311001,2026-10-08,P' -> (reg, date, status) or raise ValueError."""
    parts = line.strip().split(",")
    if len(parts) != 3:
        raise ValueError(f"expected 3 fields, found {len(parts)}")
    reg, date, status = (p.strip() for p in parts)
    if status not in ("P", "A"):
        raise ValueError(f"invalid status {status!r}")
    return reg, date, status


def process_month(folder):
    """Return (counts, errors). counts[reg] = [present, total]; errors = (file, line_no, text, msg)."""
    counts, errors = {}, []
    for path in sorted(Path(folder).glob("attendance_*.txt")):
        try:
            with open(path, encoding="utf-8") as f:
                for n, line in enumerate(f, start=1):
                    if not line.strip():
                        continue
                    try:
                        reg, date, status = parse_line(line)
                    except ValueError as e:
                        errors.append((path.name, n, line.strip(), str(e)))
                        continue
                    rec = counts.setdefault(reg, [0, 0])
                    rec[1] += 1
                    if status == "P":
                        rec[0] += 1
        except (PermissionError, UnicodeDecodeError) as e:
            errors.append((path.name, 0, "", f"file skipped: {type(e).__name__}"))
    return counts, errors


def main():
    if not DATA_DIR.is_dir():                      # glob() on a missing folder returns nothing, silently
        print(f"Error: folder {DATA_DIR} does not exist")
        return 1
    counts, errors = process_month(DATA_DIR)
    OUT_DIR.mkdir(exist_ok=True)
    low = []
    with open(OUT_DIR / "attendance_report.csv", "w", encoding="utf-8") as rep:
        rep.write("register,present,total,percentage\n")
        for reg in sorted(counts):
            p, t = counts[reg]
            pct = 100 * p / t
            rep.write(f"{reg},{p},{t},{pct:.1f}\n")
            if pct < THRESHOLD:
                low.append((reg, pct))
    with open(OUT_DIR / "below_75.txt", "w", encoding="utf-8") as f:
        for reg, pct in low:
            f.write(f"{reg} {pct:.1f}%\n")
    with open(OUT_DIR / "damaged_lines.log", "w", encoding="utf-8") as f:
        for name, n, text, msg in errors:
            f.write(f"{name}:{n}: {msg}: {text!r}\n")
    for name in ("attendance_report.csv", "below_75.txt", "damaged_lines.log"):
        print(f"--- {name}")
        print((OUT_DIR / name).read_text(encoding="utf-8"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
