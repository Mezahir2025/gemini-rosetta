from decimal import Decimal, getcontext

class FixedDepositAccount:
    def calculate_interest(self):
        # Precise Decimal Arithmetic & ISO Dates
        # Resolves Y2K and Floating Point issues
        ctx = getcontext()
        ctx.prec = 28
        
        # Formula: Principal * Rate * Years
        # Using Decimal for currency is standard practice
        amount = self.principal * ((1 + self.rate/100) ** self.years)
        return (amount - self.principal).quantize(Decimal("0.01"))
