"""Alternative concept: f.read()/readlines() versus iterating line by line (50,000 lines)."""
import time, tracemalloc
FILE = "mess_big.txt"

def by_read():
    with open(FILE, encoding="utf-8") as f:
        return sum(1 for _ in f.read().split("\n") if _)
def by_readlines():
    with open(FILE, encoding="utf-8") as f:
        return sum(1 for _ in f.readlines())
def by_iteration():
    n = 0
    with open(FILE, encoding="utf-8") as f:
        for _ in f:
            n += 1
    return n

for fn in (by_read, by_readlines, by_iteration):
    tracemalloc.start(); t0 = time.perf_counter(); n = fn(); dt = time.perf_counter() - t0
    peak = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"{fn.__name__:13s}: lines={n}  time={dt*1000:7.1f} ms  peak memory={peak/1024:9.1f} KiB")
import os
print("file size on disk:", round(os.path.getsize(FILE)/1024, 1), "KiB")
