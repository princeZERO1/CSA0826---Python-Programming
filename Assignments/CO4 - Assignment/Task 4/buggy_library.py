"""Task 4.1/4.2: the original buggy library program plus a test that demonstrates each defect."""
import os, tempfile

def save_returns(books):
    log = open("returns.log", "w")       # DEFECT 1: "w" truncates -> earlier days lost
    for b in books:
        log.write(b)                     # DEFECT 2: no newline -> titles run together
    log.close()                          # DEFECT 3: skipped if write() fails -> file left open

def process(day_file):
    try:
        books = open(day_file).read().split("\n")   # DEFECT: input file never closed either
        save_returns(books)
    except FileNotFoundError:
        print("missing")                 # DEFECT 4: only a print; error not saved; other errors uncaught

os.chdir(tempfile.mkdtemp())
for day, titles in (("mon", "Python Basics\nData Structures"), ("tue", "Algorithms\nDatabases"), ("wed", "Networks\nOS Concepts")):
    with open(f"{day}.txt", "w") as f:
        f.write(titles)
for day in ("mon", "tue", "wed"):
    process(f"{day}.txt")
print("Log after three days:")
print(repr(open("returns.log").read()))

print("\nDefect 3: write() fails halfway (a non-string book) -> does close() run?")
log = None
def failing_save(books):
    global log
    log = open("returns.log", "w")
    for b in books:
        log.write(b)                     # 123 is not a str -> TypeError
    log.close()
try:
    failing_save(["Good Book", 123])
except TypeError as e:
    print("TypeError:", e)
print("file closed after the error? ->", log.closed)

print("\nDefect 4: a different error (UnicodeDecodeError) is not handled and nothing is logged")
open("bad.txt", "wb").write(b"\xff\xfe")
try:
    process("bad.txt")
except UnicodeDecodeError as e:
    print("program stopped with", type(e).__name__, "and no message was saved")
