from decimal import Decimal, ROUND_HALF_UP

class FixedDepositAccount:
    """
    Modern Python implementation of legacy COBOL Fixed Deposit logic.
    Ensures high precision decimal arithmetic for financial integrity.
    """
    def __init__(self, principal, rate, years):
        self.principal = Decimal(str(principal))
        self.rate = Decimal(str(rate))
        self.years = int(years)

    def calculate_interest(self):
        """
        Calculates Compound Interest.
        Formula: A = P(1 + r/100)^n
        Returns interest amount rounded to 2 decimal places.
        """
        if self.principal < 0 or self.rate < 0 or self.years < 0:
            raise ValueError("Negative values not allowed in financial transactions")

        amount = self.principal * ((1 + self.rate / 100) ** self.years)
        interest = amount - self.principal
        
        # Financial rounding (Round Half Up)
        return interest.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def get_maturity_amount(self):
        return self.principal + self.calculate_interest()
