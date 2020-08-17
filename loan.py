#!/usr/bin/env python3

class Loan:
    """ TODO
    Documentation goes here
    """

    def __init__(self, name, balance, apr: float, payment: float):
        self.name = name
        self.balance = balance
        self.payment = payment
        self.apr = apr

        # Calculate the Effective Monthly Interest Rate
        self.K = 12.  # Compounding periodicity [Months per year]
        # APR -> Compound Rate
        self.aprc = self.K * ((1 + self.apr)**(1 / self.K) - 1)
        self.mpr = self.aprc / self.K  # Monthly interest rate

        # Store time history for post-processing
        self.history = [self.balance]

    def __str__(self):
        s = f"Loan:    {self.name:<16s}"
        #s += f"\tMontly Payment: ${self.payment:.2f}"
        s += f"\tBalance: ${self.balance:<9.2f}"
        s += f"\tAPR: {self.apr*100:.2f}%\n"
        #s += f"\tMonthly Rate: {self.mpr*100:.2f}%\n"

        return s

    def getPayment(self) -> float:
        """ Get the monthly payment amount """
        return self.payment

    def makePayment(self, source, payment=None) -> float:
        """ Make a single payment on the loan """
        if self.balance <= 0:
            return

        if payment is None:
            # Use the specified monthly payment by default
            # Don't go below 0!
            payment = min(self.payment, self.balance)

        self.balance -= payment
        source.withdraw(payment)

        print(
            f"Withdraw ${payment:<7.2f} from {source.name} for loan {self.name}")
        if self.balance <= 0:
            print(
                f"~*~*~ Congrats! You've paid off the {self.name} loan! ~*~*~")

        return self.balance

    def accumulate(self) -> float:
        """ Accumulate monthly interest on the loan """
        self.balance *= (1 + self.mpr)
        return self.balance

    def step(self, source) -> float:
        """ Advance in time one month """
        if self.balance <= 0:
            return 0

        self.makePayment(source)
        balance = self.accumulate()
        self.history.append(self.balance)

        return balance
