"""Rate card of the village milk co-operative (used as a module).

Constants
---------
BASE_RATE      : float – Rs per litre for milk with 3.5 % fat and 8.5 % SNF
FAT_STEP_VALUE : float – Rs per litre for every 0.1 % of fat above/below 3.5
SNF_STEP_VALUE : float – Rs per litre for every 0.1 % of SNF above/below 8.5

Functions
---------
rate_per_litre(fat, snf) -> float
payout(litres, fat, snf) -> float
"""

BASE_RATE      = 30.00      # Rs per litre for milk with 3.5 % fat and 8.5 % SNF
FAT_STEP_VALUE = 0.40       # Rs per litre for every 0.1 % of fat above or below 3.5
SNF_STEP_VALUE = 0.30       # Rs per litre for every 0.1 % of SNF above or below 8.5
FAT_STD        = 3.5        # standard fat %
SNF_STD        = 8.5        # standard SNF %
STEP_SIZE      = 0.1        # one step = 0.1 %


def rate_per_litre(fat, snf):
    """
    Returns the price per litre, rounded to 2 decimals.

    Parameters
    ----------
    fat : float  Fat percentage of the milk sample
    snf : float  SNF percentage of the milk sample

    Returns
    -------
    float  Price per litre in rupees.
    """
    # TODO 1: Count the 0.1 % steps of fat from 3.5 and of SNF from 8.5
    #         (round to the nearest whole step), add their values to
    #         BASE_RATE and round to 2 decimals.
    fat_steps = round((fat - FAT_STD) / STEP_SIZE)   # nearest whole step
    snf_steps = round((snf - SNF_STD) / STEP_SIZE)
    rate = BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE
    return round(rate, 2)


def payout(litres, fat, snf):
    """
    Returns the amount payable to the farmer, rounded to 2 decimals.

    Parameters
    ----------
    litres : float  Quantity of milk delivered
    fat    : float  Fat percentage
    snf    : float  SNF percentage

    Returns
    -------
    float  Amount payable in rupees.
    """
    # TODO 2: Multiply litres by the rate per litre and round to 2 decimals.
    return round(rate_per_litre(fat, snf) * litres, 2)


if __name__ == "__main__":
    # This block executes only when milkrate.py is run directly.
    # When imported by another script, Python skips this block entirely,
    # so the table is never printed during an import.
    print("milkrate.py – self-test")
    print(f"{'Litres':>7}  {'Fat':>5}  {'SNF':>5}  {'Rate':>8}  {'Pay':>10}")
    print("-" * 44)
    for litres, fat, snf in [(10, 3.5, 8.5), (8.5, 4.2, 8.7), (12, 3.1, 8.3)]:
        rate, pay = rate_per_litre(fat, snf), payout(litres, fat, snf)
        print(f"{litres:5} L  fat {fat}  snf {snf}  rate {rate:6.2f}  pay {pay:8.2f}")
