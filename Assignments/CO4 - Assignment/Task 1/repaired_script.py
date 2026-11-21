"""Task 1.2: repaired mess-bill totaller (with, line-by-line, specific exceptions, rejects)."""
import sys
from decimal import Decimal, InvalidOperation


def total_mess_bills(filename):
    """Return (total, report_lines, rejected) for a file of 'regno,name,amount' lines.

    total        -- Decimal sum of valid amounts (exact, paise kept)
    report_lines -- list of 'name amount' strings
    rejected     -- list of (line_number, original_text, reason)
    """
    total = Decimal("0")
    report_lines, rejected = [], []
    with open(filename, encoding="utf-8") as f:          # always closed
        for number, line in enumerate(f, start=1):       # one line in memory at a time
            line = line.rstrip("\n")
            if not line.strip():                         # blank / last empty line
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) != 3:
                rejected.append((number, line, f"expected 3 fields, found {len(parts)}"))
                continue
            try:
                amount = Decimal(parts[2])
            except InvalidOperation:
                rejected.append((number, line, f"amount {parts[2]!r} is not a number"))
                continue
            if amount < 0:
                rejected.append((number, line, "negative amount"))
                continue
            total += amount
            report_lines.append(f"{parts[1]} {amount}")
    return total, report_lines, rejected


def main(filename):
    try:
        total, report_lines, rejected = total_mess_bills(filename)
    except FileNotFoundError:
        print(f"Error: file {filename!r} not found")
        return 1
    except PermissionError:
        print(f"Error: no permission to read {filename!r}")
        return 1
    except UnicodeDecodeError as e:
        print(f"Error: {filename!r} is not valid UTF-8 ({e.reason})")
        return 1
    print("\n".join(report_lines))                       # one join, not repeated +
    print("Total", total)
    print(f"Rejected lines: {len(rejected)}")
    for number, text, reason in rejected:
        print(f"  line {number}: {text!r} -> {reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "mess_oct.txt"))
