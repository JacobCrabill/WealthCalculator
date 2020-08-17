#!/usr/bin/env python3


class Savings:
    """ TODO
    Documentation goes here
    """

    def __init__(self, name, balance, apy):
        self.name = name
        self.balance = balance
        self.apy = apy
        
        # Calculate the Effective Monthly Interest Rate
        self.K = 12  # Compounding periodicity [Months per year]
        self.apyc = self.K * ((1 + self.apy)**(1 / self.K) - 1) # apy -> Compound Rate
        self.mpr = self.apyc / self.K  # Monthly interest rate

        # Store time history for post-processing
        self.history = [self.balance]

    def __str__(self):
        s = f"Savings: {self.name:<16s}"
        s += f"\tBalance: ${self.balance:.2f}"
        s += f"\tAPY: {self.apy*100:.2f}%\n"
        #s += f"\tMonthly Rate: {self.mpr*100:.2f}%\n"

        return s

    def deposit(self, deposit):
        """ Make a deposit to our balance """
        self.balance += deposit
        return self.balance

    def withdraw(self, withdrawl):
        """ Make a withdrawl from our balance """
        self.balance -= withdrawl

        if self.balance < 0:
            raise Exception("Negative balance!")

        return self.balance

    def step(self) -> float:
        """ Advance in time one month """
        self.balance *= (1 + self.mpr)
        self.history.append(self.balance)
        return self.balance
