"""Stage 5: five demonstration scenarios, each asserted."""
import tempfile
from pathlib import Path
from festreg.pipeline import run
from festreg.validator import valid_email

def make(files):
    d = Path(tempfile.mkdtemp())
    for name, text in files.items():
        (d / f"{name}.txt").write_text(text, encoding="utf-8")
    return d

def log(out):
    return (Path(out) / "error_log.txt").read_text(encoding="utf-8").splitlines()

# 1. clean files
base = {d: f"19231{k}001,A{k},{d.upper()},a{k}@c.edu,Quiz;Dance\n19231{k}002,B{k},{d.upper()},b{k}@c.edu,Music\n"
        for k, d in enumerate(["cse", "ece", "mech", "civil", "eee"], start=1)}
out = tempfile.mkdtemp(); info = run(make(base), out)
assert info == {"files_expected": 5, "files_ok": 5, "lines": 10, "duplicates": 0, "rejected": 0}, info
assert log(out) == []
print("1. clean files            :", info)

# 2. duplicate registration
d = dict(base); d["ece"] += "192311001,A1,CSE,a1@c.edu,Drama\n"
out = tempfile.mkdtemp(); info = run(make(d), out)
assert info["duplicates"] == 1 and info["rejected"] == 0 and any("duplicate" in l for l in log(out))
print("2. duplicate registration :", info, "->", log(out)[0])

# 3. invalid e-mail
d = dict(base); d["mech"] += "192313009,Z,MECH,not-an-email,Quiz\n"
out = tempfile.mkdtemp(); info = run(make(d), out)
assert info["rejected"] == 1 and any("invalid e-mail" in l for l in log(out))
print("3. invalid e-mail         :", info, "->", log(out)[0])

# 4. damaged line
d = dict(base); d["civil"] += "garbage line without commas\n"
out = tempfile.mkdtemp(); info = run(make(d), out)
assert info["rejected"] == 1 and any("expected 5 fields" in l for l in log(out))
print("4. damaged line           :", info, "->", log(out)[0])

# 5. missing department file
d = dict(base); del d["eee"]
out = tempfile.mkdtemp(); info = run(make(d), out)
assert info["files_ok"] == 4 and info["lines"] == 8 and any("missing" in l for l in log(out))
print("5. missing department file:", info, "->", log(out)[0])

# e-mail validator unit checks
good = ["a@b.co", "x.y@dept.college.edu"]; bad = ["a@b", "@b.com", "a b@c.com", "a@@b.com", "a@.com", "a@b..com", "a@b.", ""]
assert all(valid_email(e) for e in good) and not any(valid_email(e) for e in bad)
print("6. e-mail validator       : 2 valid and 8 invalid examples all classified correctly")
# 7. event names typed in different cases must be one event (regression test for a bug found in review)
d = dict(base); d["cse"] += "192311009,Q,CSE,q@c.edu,quiz;QUIZ;Quiz\n"
out = tempfile.mkdtemp(); run(make(d), out)
files = sorted(p.name for p in (Path(out) / "events").iterdir())
assert files == ["dance.txt", "music.txt", "quiz.txt"], files
quiz = (Path(out) / "events" / "quiz.txt").read_text().splitlines()
assert sum("192311009" in l for l in quiz) == 1
print("7. event-name case        : 'quiz;QUIZ;Quiz' -> one event file quiz.txt, student listed once")

print("\nAll Task 6 tests passed.")
