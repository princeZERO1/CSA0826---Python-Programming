"""
Q5 – Functions, Parameters and Scope
College Canteen Order System

Bug: add_item(item, order=[]) uses a mutable default argument.
The default list is created ONCE at function definition time.
All calls that omit `order` share the SAME list object.

Bloom's Level: K4 – Analyse
"""

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 : THE BUG and THE FIX (Complete the Code – TODO 1)
# ─────────────────────────────────────────────────────────────────────────────

def add_item_buggy(item, order=[]):
    """BUGGY: mutable default accumulates across calls."""
    order.append(item)
    return order


def add_item(item, order=None):
    """FIXED (TODO 1): Use None sentinel; create a fresh list each call."""
    if order is None:
        order = []          # new list created each time
    order.append(item)
    return order


print("=" * 55)
print("COMPLETE THE CODE – Expected output")
print("=" * 55)
print(add_item_buggy("Tea"), add_item_buggy("Vada"))
print(add_item("Tea"),       add_item("Vada"))

# Inspect the shared default list
print(f"\nadd_item_buggy.__defaults__ = {add_item_buggy.__defaults__}")
print("→ The default list accumulates items because it is shared across all calls.")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 : THREE CUSTOMERS – independent orders
# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 55)
print("THREE CUSTOMERS – independent orders")
print("=" * 55)

def process_order(customer_name, *items):
    """
    Demonstrates:
      - positional parameters: customer_name
      - *items: variable positional (tuple of items)
      - default parameter: order=None (None sentinel)
    Returns: (order_list, total, gst)   ← multiple return values via tuple
    """
    PRICES = {"Tea": 10, "Vada": 15, "Dosa": 30, "Coffee": 20, "Idli": 25}
    GST_RATE = 0.05

    order = []
    for item in items:
        order = add_item(item, order)

    total = sum(PRICES.get(it, 0) for it in order)
    gst   = round(total * GST_RATE, 2)
    return order, total, gst       # multiple return values


for name, menu_items in [
    ("Customer 1", ("Tea", "Vada")),
    ("Customer 2", ("Dosa", "Coffee", "Idli")),
    ("Customer 3", ("Tea", "Tea", "Idli")),
]:
    order, total, gst = process_order(name, *menu_items)
    print(f"  {name}: {order}  Total=₹{total}  GST=₹{gst}")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 : POSITIONAL, KEYWORD and DEFAULT parameters
# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 55)
print("PARAMETER TYPES DEMONSTRATED")
print("=" * 55)

def bill(customer, item, qty=1, discount=0.0):
    """
    customer : positional (required)
    item     : positional (required)
    qty      : default (optional)
    discount : default (optional)
    """
    PRICES = {"Tea": 10, "Dosa": 30}
    base = PRICES.get(item, 0) * qty
    return base * (1 - discount)

print(f"  Positional only         : {bill('Alice', 'Tea')}")
print(f"  With qty keyword        : {bill('Bob', 'Dosa', qty=2)}")
print(f"  With discount keyword   : {bill('Carol', 'Tea', qty=3, discount=0.1)}")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 : LOCAL, GLOBAL, NONLOCAL scope
# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 55)
print("SCOPE RULES")
print("=" * 55)

# --- global ---
order_count = 0          # global variable

def record_order():
    global order_count   # declare intent to modify global
    order_count += 1

record_order(); record_order()
print(f"  global order_count after 2 calls: {order_count}")
print("  (without 'global', the assignment would create a LOCAL variable and fail)")

# --- local ---
def show_local():
    x = 99               # local to show_local
    print(f"  local x inside function: {x}")

show_local()
# print(x)  # would raise NameError – x not visible here

# --- nonlocal ---
def outer():
    counter = 0
    def inner():
        nonlocal counter     # access enclosing scope variable
        counter += 1
        return counter
    return inner

tick = outer()
print(f"  nonlocal counter: {tick()}, {tick()}, {tick()}")

print("""
  WHY global IS USUALLY AVOIDED:
    • Any function can silently change a global → hard to debug.
    • Breaks function purity (same input may give different output).
    • Better: pass state as parameters and return updated values.
""")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 : ALTERNATIVE DESIGNS
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 55)
print("ALTERNATIVE 1 – Explicit list passed by caller")
print("=" * 55)

def add_item_explicit(item, order):
    """Caller always passes the list – no default parameter at all."""
    order.append(item)
    return order

o1 = []; add_item_explicit("Tea",  o1)
o2 = []; add_item_explicit("Vada", o2)
print(f"  o1={o1}, o2={o2}  ← always independent")

print()
print("=" * 55)
print("ALTERNATIVE 2 – Closure-based order builder")
print("=" * 55)

def make_order():
    """Returns an inner function; order is captured in its closure."""
    _order = []
    def add(item):
        _order.append(item)
        return list(_order)   # return a copy so caller can't mutate internal state
    return add

order_a = make_order()
order_b = make_order()
order_a("Tea"); order_a("Idli")
order_b("Coffee")
print(f"  Customer A: {order_a('Dosa')}")
print(f"  Customer B: {order_b('Vada')}")

print("""
COMPLEXITY:
  All three designs: O(1) per add_item call (list.append is amortised O(1)).
  Space per customer: O(k) where k = number of items in the order.
  Closure uses slightly more memory per customer (closure cell overhead),
  but negligible in practice.
""")
