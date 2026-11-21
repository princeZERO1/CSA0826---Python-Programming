"""Task 3 'change the file name' part: summarise() now handles a missing file."""
from complete_code import InvalidRecord, parse_line   # re-runs the original demo first


def summarise(path):
    present, absent, errors = 0, 0, []
    try:
        with open(path, encoding="utf-8") as f:
            for number, line in enumerate(f, start=1):
                try:
                    reg, date, status = parse_line(line)
                except InvalidRecord as e:
                    errors.append((number, str(e)))
                else:
                    present += status == "P"
                    absent += status == "A"
    except FileNotFoundError:
        errors.append((0, f"file not found: {path}"))
    return present, absent, errors

print(summarise("does_not_exist.csv"))
