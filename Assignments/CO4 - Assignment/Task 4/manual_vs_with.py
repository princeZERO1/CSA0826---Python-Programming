"""Alternative: manual open/try/finally/close versus with. Same complexity; count open files on error."""
import gc, io, os, tempfile, time, tracemalloc

tmp = tempfile.mkdtemp(); path = os.path.join(tmp, "a.txt"); open(path, "w").write("x\n" * 1000)

def manual():
    f = open(path)
    try:
        return len(f.read())
    finally:
        f.close()
def with_stmt():
    with open(path) as f:
        return len(f.read())
def manual_no_finally():          # the version people actually write by mistake
    f = open(path)
    n = len(f.read())
    raise RuntimeError("error before close()")
    f.close()
def with_error():
    with open(path) as f:
        n = len(f.read())
        raise RuntimeError("error inside with")

for fn in (manual, with_stmt):
    tracemalloc.start(); t0 = time.perf_counter()
    for _ in range(2000): fn()
    dt = (time.perf_counter() - t0) / 2000; peak = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"{fn.__name__:12s}: {dt*1e6:6.1f} microseconds per call, peak {peak/1024:6.1f} KiB")

def open_fds():
    """Number of file objects currently open (works on Windows, macOS and Linux)."""
    return sum(1 for o in gc.get_objects() if isinstance(o, io.TextIOWrapper) and not o.closed)
print("\nOpen files left behind after 50 errors (the exceptions are kept, as a logger or test runner would):")
for fn in (manual_no_finally, with_error):
    before = open_fds()
    kept = []
    for _ in range(50):
        try: fn()
        except RuntimeError as e: kept.append(e)       # traceback -> frame -> f stays alive
    print(f"  {fn.__name__:18s}: files still open = {open_fds() - before}")
    kept.clear()
