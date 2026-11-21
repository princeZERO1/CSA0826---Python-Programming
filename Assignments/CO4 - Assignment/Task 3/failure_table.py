"""Task 3.1: provoke every failure and print the exception actually raised."""
import os, tempfile
from pathlib import Path

def attempt(label, fn):
    try:
        fn(); print(f"{label:<22} -> no exception")
    except Exception as e:
        print(f"{label:<22} -> {type(e).__name__}: {e}")

tmp = Path(tempfile.mkdtemp())
(tmp / "latin.txt").write_bytes(b"\xe9\xe8")
(tmp / "empty.txt").write_text("")
(tmp / "locked.txt").write_text("x"); os.chmod(tmp / "locked.txt", 0)
attempt("missing folder",    lambda: os.listdir(tmp / "nofolder"))
attempt("missing file",      lambda: open(tmp / "nofile.txt"))
if not hasattr(os, "geteuid") or os.geteuid() == 0:
    print("permission denied      -> NOT demonstrable here: this system does not enforce chmod here (root user or Windows). "
          " A normal user gets PermissionError: [Errno 13] Permission denied.")
else:
    attempt("permission denied", lambda: open(tmp / "locked.txt").read())
attempt("wrong encoding",    lambda: open(tmp / "latin.txt", encoding="utf-8").read())
def unpack3():
    reg, date, status = "1,2".split(",")      # a line with only 2 fields
attempt("damaged: 2 fields", unpack3)
attempt("damaged: index",    lambda: "1,2".split(",")[2])
attempt("damaged: int('x')", lambda: int("P"))
attempt("empty file read",   lambda: print("   read() of empty file gives", repr(open(tmp / "empty.txt").read())))
attempt("open a directory",  lambda: open(tmp))
