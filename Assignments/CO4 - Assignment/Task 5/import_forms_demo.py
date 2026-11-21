"""Task 5.3: three import forms for the package, plus one-time import cost and sys.modules."""
import importlib, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "d_package"))

print("1) import attendance.stats")
import attendance.stats
print("   call as: attendance.stats.percentage(...)  ->", attendance.stats.percentage({"R1": [("d1", "P"), ("d2", "A")]}))
print("   names bound here:", "attendance" in globals(), "| 'stats' bound:", "stats" in globals())

print("2) from attendance import stats")
from attendance import stats
print("   call as: stats.percentage(...)             ->", stats.percentage({"R1": [("d1", "P")]}))

print("3) from attendance.stats import percentage")
from attendance.stats import percentage
print("   call as: percentage(...)                   ->", percentage({"R1": [("d1", "A")]}))

print("\nAll three names point to the SAME function object:",
      attendance.stats.percentage is stats.percentage is percentage)

print("\nOne-time import cost (modules cached in sys.modules):")
for name in ["attendance", "attendance.reader", "attendance.stats", "attendance.report"]:
    sys.modules.pop(name, None)
t0 = time.perf_counter(); importlib.import_module("attendance.reader"); importlib.import_module("attendance.stats"); importlib.import_module("attendance.report")
first = time.perf_counter() - t0
t0 = time.perf_counter()
for _ in range(1000):
    importlib.import_module("attendance.stats")
again = (time.perf_counter() - t0) / 1000
print(f"   first import of package + 3 sub-modules : {first*1e6:8.1f} microseconds")
print(f"   repeated import (cache hit, per call)   : {again*1e6:8.2f} microseconds")
print("   'attendance.stats' in sys.modules:", "attendance.stats" in sys.modules)
