"""Tasks 3.2 / 3.3: custom exception, complete try statement, raise ... from ..."""
import sys
from pathlib import Path


class InvalidRecord(Exception):
    """A line is not 'register,date,P|A'. Raised in parse_line, handled in process_file."""


def parse_line(line):
    """Return (reg, date, status) or raise InvalidRecord chained to the original cause."""
    try:
        reg, date, status = line.strip().split(",")        # ValueError if not exactly 3 parts
    except ValueError as e:
        raise InvalidRecord(f"wrong number of fields in {line.strip()!r}") from e
    if status not in ("P", "A"):
        raise InvalidRecord(f"invalid status {status!r}")
    return reg, date, status


def process_file(path):
    """Return (present, absent, bad_lines). Shows try / except / else / finally."""
    present = absent = 0
    bad = []
    f = None
    try:
        f = open(path, encoding="utf-8")
        lines = f.readlines()
    except FileNotFoundError:
        print(f"[except] file not found: {Path(path).name}")
        return 0, 0, bad
    except PermissionError:
        print(f"[except] permission denied: {Path(path).name}")
        return 0, 0, bad
    except UnicodeDecodeError as e:
        print(f"[except] wrong encoding in {Path(path).name}: {e.reason}")
        return 0, 0, bad
    else:
        print(f"[else] {Path(path).name} opened and read ({len(lines)} lines)")
        if not lines:
            print("[else] file is empty")
    finally:
        if f is not None:
            f.close()
        print(f"[finally] cleanup done for {Path(path).name}")
    for n, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            _, _, status = parse_line(line)
        except InvalidRecord as e:
            bad.append((n, str(e), repr(e.__cause__)))
            continue
        present += status == "P"
        absent += status == "A"
    return present, absent, bad


if __name__ == "__main__":
    good = Path(__file__).parent.parent / "Task02" / "data" / "2026-10" / "attendance_2026-10-07.txt"
    print(process_file(good))
    print(process_file("missing_file.txt"))
    empty = Path(__file__).parent / "empty.txt"; empty.write_text("")
    print(process_file(empty)); empty.unlink()
    badenc = Path(__file__).parent / "latin.txt"; badenc.write_bytes(b"192311001,2026-10-01,P\xe9\n")
    print(process_file(badenc)); badenc.unlink()
