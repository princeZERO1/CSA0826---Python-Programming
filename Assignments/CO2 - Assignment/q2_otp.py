"""
Q2 – Loops that Count Attempts
OTP Verification at a Bank Kiosk

Rules:
  - 3 attempts allowed
  - Blank entry does NOT count as an attempt
  - After 3 wrong attempts → account locked for 30 min
  - loop-else clause used to lock the account

Bloom's Level: K3 – Apply
"""

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 : while loop design
# ─────────────────────────────────────────────────────────────────────────────
def otp_while(correct_otp):
    """OTP verification using while loop."""
    print("\n--- WHILE LOOP VERSION ---")
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        entered = input(f"  Enter OTP (attempt {attempts + 1}/{max_attempts}): ").strip()

        if entered == "":           # blank → continue without counting
            print("  Blank entry ignored. Try again.")
            continue                # <-- continue: skip counter update, loop again

        if entered == correct_otp:
            print("  ✓ OTP verified successfully!")
            break                   # <-- break: exit loop on success
        else:
            attempts += 1           # only counted for non-blank wrong entries
            print(f"  ✗ Incorrect OTP. ({attempts}/{max_attempts} attempts used)")
            if attempts == max_attempts:
                pass                # <-- pass: placeholder; locking handled below
    else:
        # loop-else fires only when loop exhausts without break
        print("  ⛔ Account locked for 30 minutes after 3 failed attempts.")

    # BUG DEMONSTRATION:
    # If we update attempts BEFORE the blank check, blank entries count as attempts.
    # Correct placement: increment AFTER confirming the entry is non-blank and wrong.


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 : for loop design
# ─────────────────────────────────────────────────────────────────────────────
def otp_for(correct_otp):
    """OTP verification using for loop with range(3)."""
    print("\n--- FOR LOOP VERSION ---")
    attempts_used = 0

    for attempt_num in range(1, 4):       # range(3) gives 0,1,2 → use range(1,4)
        entered = input(f"  Enter OTP (attempt {attempt_num}/3): ").strip()

        if entered == "":
            print("  Blank entry ignored.")
            continue                        # <-- continue: go to next iteration
                                            # NOTE: for-loop auto-increments attempt_num
                                            # This is a limitation vs while: we can't
                                            # truly "not count" this iteration's slot.

        if entered == correct_otp:
            print("  ✓ OTP verified successfully!")
            break
        else:
            attempts_used += 1
            print(f"  ✗ Incorrect. ({attempt_num} slots used)")
            pass                            # <-- pass: nothing extra needed here
    else:
        print("  ⛔ Account locked for 30 minutes.")

    # WHEN IS while MORE NATURAL?
    # while is more natural here because:
    #   • We control WHEN to increment the counter (blank entries don't count).
    #   • for auto-advances its counter on every iteration, making "not counting"
    #     a blank entry require extra tracking with attempts_used.
    #   • while expresses "keep trying until max wrong attempts" more directly.


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 : Extended – 2 extra attempts after security question
# ─────────────────────────────────────────────────────────────────────────────
def otp_extended(correct_otp, security_answer):
    """
    Changed condition: 2 extra attempts if security question answered correctly.
    Re-evaluated design: use while with a dynamic max_attempts.
    """
    print("\n--- EXTENDED WHILE LOOP (security question) ---")
    attempts = 0
    max_attempts = 3
    extra_given = False

    while attempts < max_attempts:
        entered = input(f"  Enter OTP (attempt {attempts + 1}/{max_attempts}): ").strip()

        if entered == "":
            print("  Blank entry ignored.")
            continue

        if entered == correct_otp:
            print("  ✓ OTP verified successfully!")
            break
        else:
            attempts += 1
            print(f"  ✗ Incorrect. ({attempts}/{max_attempts} attempts used)")

            # Offer security question once when last normal attempt is used
            if attempts == 3 and not extra_given:
                ans = input("  Answer security question to get 2 more attempts: ").strip()
                if ans.lower() == security_answer.lower():
                    max_attempts += 2       # dynamically extend limit
                    extra_given = True
                    print(f"  ✓ Correct! You have {max_attempts - attempts} more attempt(s).")
                else:
                    print("  ✗ Wrong answer. No extra attempts.")
    else:
        print("  ⛔ Account locked for 30 minutes.")

    # DESIGN NOTE: while is clearly superior for the extended condition because
    # max_attempts can be changed at runtime. A for loop with range(3) would
    # require restructuring the entire loop.


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 : RECURSIVE version (Alternative Concept)
# ─────────────────────────────────────────────────────────────────────────────
def otp_recursive(correct_otp, attempt=1, max_attempts=3):
    """
    Recursive OTP verification.
    Time:  O(a) for a attempts – same as loops.
    Space: O(a) stack frames – WORSE than loops (O(1)).
    """
    if attempt > max_attempts:
        print("  ⛔ [Recursive] Account locked for 30 minutes.")
        return False

    entered = input(f"  [Recursive] Enter OTP (attempt {attempt}/{max_attempts}): ").strip()

    if entered == "":
        print("  Blank entry ignored.")
        return otp_recursive(correct_otp, attempt, max_attempts)   # don't advance counter

    if entered == correct_otp:
        print("  ✓ [Recursive] OTP verified!")
        return True
    else:
        print(f"  ✗ Incorrect. ({attempt}/{max_attempts} attempts used)")
        return otp_recursive(correct_otp, attempt + 1, max_attempts)


# ─────────────────────────────────────────────────────────────────────────────
# DEMO  (runs with simulated input for automated testing)
# ─────────────────────────────────────────────────────────────────────────────
def demo_simulate():
    """Simulate OTP verification without interactive input."""
    correct = "482910"

    # Simulate: blank, wrong, wrong, wrong → locked
    inputs_locked = ["", "111111", "222222", "333333"]
    # Simulate: blank, wrong, correct → verified
    inputs_ok     = ["", "111111", correct]

    def run_while_sim(correct_otp, inputs):
        print("\n=== SIMULATION – while loop ===")
        it = iter(inputs)
        attempts = 0
        while attempts < 3:
            entered = next(it, "").strip()
            print(f"  Input: '{entered}'")
            if entered == "":
                print("  Blank – ignored")
                continue
            if entered == correct_otp:
                print("  ✓ OTP correct!")
                break
            else:
                attempts += 1
                print(f"  ✗ Wrong. {attempts}/3 used.")
        else:
            print("  ⛔ Account locked.")

    def run_for_sim(correct_otp, inputs):
        print("\n=== SIMULATION – for loop ===")
        it = iter(inputs)
        for i in range(1, 4):
            entered = next(it, "").strip()
            print(f"  Slot {i}, Input: '{entered}'")
            if entered == "":
                print("  Blank – ignored (slot still consumed)")
                continue
            if entered == correct_otp:
                print("  ✓ OTP correct!")
                break
            else:
                print(f"  ✗ Wrong.")
        else:
            print("  ⛔ Account locked.")

    run_while_sim(correct, inputs_locked)
    run_while_sim(correct, inputs_ok)
    run_for_sim(correct, inputs_locked)
    run_for_sim(correct, inputs_ok)

    print("\n")
    print("KEY ANALYSIS:")
    print("  • while: blank entry truly doesn't consume an attempt (counter not incremented).")
    print("  • for  : blank uses a loop iteration slot even with continue.")
    print("  • while is MORE NATURAL for this problem.")
    print("  • BUG: If counter updated BEFORE blank check, blank entries count as attempts.")
    print("  • Recursive: O(a) time, O(a) space (stack) – loop is O(1) space, preferred.")


if __name__ == "__main__":
    demo_simulate()
