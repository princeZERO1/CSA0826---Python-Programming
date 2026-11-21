"""Task 4.3: repaired library program (append mode, newlines, with, error log)."""
import logging
from pathlib import Path



def setup_logging(path="errors.log"):
    """Send ERROR messages to a file (absolute path so it does not depend on the current folder)."""
    logging.basicConfig(filename=str(Path(path).resolve()), level=logging.ERROR,
                        format="%(levelname)s %(message)s", force=True)


def save_returns(books, log_file="returns.log"):
    """Append each book title on its own line; the file is always closed."""
    with open(log_file, "a", encoding="utf-8") as log:       # "a" keeps earlier days
        for title in books:
            log.write(title + "\n")                           # newline after every title


def process(day_file):
    """Read one day's returns and append them to the log. Returns True on success."""
    try:
        with open(day_file, encoding="utf-8") as f:
            books = [line.strip() for line in f if line.strip()]
        save_returns(books)
        return True
    except FileNotFoundError:
        logging.error("missing file: %s", day_file)
    except (UnicodeDecodeError, PermissionError, OSError) as e:
        logging.error("cannot process %s: %s: %s", day_file, type(e).__name__, e)
    return False


if __name__ == "__main__":
    import os, tempfile
    os.chdir(tempfile.mkdtemp())
    setup_logging()
    for day, titles in (("mon", "Python Basics\nData Structures"), ("tue", "Algorithms\nDatabases"), ("wed", "Networks\nOS Concepts")):
        Path(f"{day}.txt").write_text(titles, encoding="utf-8")
    Path("bad.txt").write_bytes(b"\xff\xfe")
    results = [process(d) for d in ("mon.txt", "tue.txt", "missing.txt", "bad.txt", "wed.txt")]
    print("results:", results)
    print("returns.log:"); print(Path("returns.log").read_text(), end="")
    print("errors.log:");  print(Path("errors.log").read_text(), end="")
