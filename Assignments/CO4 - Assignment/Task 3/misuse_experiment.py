"""Task 3.4: except Exception: pass hides a typing error (NameError)."""
def count_present(lines):
    present = 0
    for line in lines:
        try:
            reg, date, status = line.strip().split(",")
            if status == "P":
                presnt += 1            # typo: should be 'present'
        except Exception:
            pass                       # swallows EVERYTHING, even NameError
    return present

lines = ["1,2026-10-01,P", "2,2026-10-01,P", "3,2026-10-01,A"]
print("Misused handler : present =", count_present(lines), "(correct answer is 2) -- no error shown")

def count_present_fixed(lines):
    present = 0
    for line in lines:
        try:
            reg, date, status = line.strip().split(",")
        except ValueError:
            continue
        if status == "P":
            presnt += 1                # same typo
    return present

try:
    count_present_fixed(lines)
except NameError as e:
    print("Specific handler: NameError surfaced ->", e)
