"""
Task 7 – Build a Module
  Demonstrates three import styles and uses milkrate from a separate script.
  Explains if __name__ == '__main__' and sys.path / sys.modules.
"""

import sys
import math
from decimal import Decimal

SEP = "=" * 64

print(SEP)
print("TASK 7 – Module: milkrate.py")
print(SEP)

# ════════════════════════════════════════════════════════════════
# THREE IMPORT STYLES
# ════════════════════════════════════════════════════════════════
print("""
── Three import styles ───────────────────────────────────────────
  Style 1  import milkrate
           → milkrate.rate_per_litre(fat, snf)
           → milkrate.BASE_RATE
           Namespace is explicit; no name collisions.

  Style 2  from milkrate import payout
           → payout(litres, fat, snf)   (direct, unqualified)
           Risk: if the calling script also defines payout(), the
           local name silently wins.

  Style 3  import milkrate as mr
           → mr.rate_per_litre(fat, snf)
           Useful when the module name is long or clashes with a
           local variable; keeps namespace clear with less typing.
""")

# Style 1
import milkrate

print("── Style 1: import milkrate ──────────────────────────────────")
for litres, fat, snf in [(10, 3.5, 8.5), (8.5, 4.2, 8.7), (12, 3.1, 8.3)]:
    rate = milkrate.rate_per_litre(fat, snf)
    pay  = milkrate.payout(litres, fat, snf)
    print(f"  {litres:5} L  fat {fat}  snf {snf}  "
          f"rate {rate:6.2f}  pay {pay:8.2f}")

# Style 2
print("\n── Style 2: from milkrate import payout ──────────────────────")
from milkrate import payout, rate_per_litre
print(f"  payout(10, 3.5, 8.5)   = {payout(10, 3.5, 8.5)}")
print(f"  rate_per_litre(4.2, 8.7) = {rate_per_litre(4.2, 8.7)}")

# Style 3
print("\n── Style 3: import milkrate as mr ────────────────────────────")
import milkrate as mr
print(f"  mr.BASE_RATE        = {mr.BASE_RATE}")
print(f"  mr.payout(8.5, 4.2, 8.7) = {mr.payout(8.5, 4.2, 8.7)}")

# ════════════════════════════════════════════════════════════════
# if __name__ == '__main__'  EXPLANATION
# ════════════════════════════════════════════════════════════════
print("""
── if __name__ == '__main__' explained ───────────────────────────
  When milkrate.py is run directly:
      __name__ is '__main__'  → the test table IS printed.
  When milkrate is imported by this script:
      __name__ is 'milkrate'  → the condition is False → table is NOT printed.

  Without that guard, every import would print the table – cluttering
  every program that uses the module.
""")

# ════════════════════════════════════════════════════════════════
# sys.modules  – Python loads each module only once
# ════════════════════════════════════════════════════════════════
print("── sys.modules caching ───────────────────────────────────────")
print(f"  'milkrate' in sys.modules → {'milkrate' in sys.modules}")
print("  Python loads milkrate once and caches it in sys.modules.")
print("  Subsequent imports return the cached object – O(1) lookup cost.")

# ════════════════════════════════════════════════════════════════
# Standard-library modules
# ════════════════════════════════════════════════════════════════
print("\n── Standard modules used in this project ─────────────────────")
print(f"  math.floor(-3.5)      = {math.floor(-3.5)}")
print(f"  Decimal('0.1')+Decimal('0.2') == Decimal('0.3') → "
      f"{Decimal('0.1') + Decimal('0.2') == Decimal('0.3')}")

# ════════════════════════════════════════════════════════════════
# sys.path
# ════════════════════════════════════════════════════════════════
print("\n── Where Python looks for modules (sys.path) ─────────────────")
for i, p in enumerate(sys.path[:5], 1):
    print(f"  [{i}] {p or '(current directory)'}")
print("  Python searches in order; first match wins.")
print("  milkrate.py in the same folder → found at entry [1] ('' = cwd).")

# ════════════════════════════════════════════════════════════════
# ALTERNATIVE CONCEPT
# ════════════════════════════════════════════════════════════════
print("""
── Alternative: copying functions into every script ──────────────
  If rate_per_litre() and payout() were copy-pasted into each script:
    • A rate change requires editing k scripts – high risk of partial updates
      (exactly the bug the original volunteer made).
    • Module import cost: Python parses milkrate.py once at start-up and
      caches it in sys.modules; every subsequent 'import milkrate' in the
      same process is an O(1) dict lookup – negligible overhead.
  Conclusion: always centralise rate logic in a module.
""")
