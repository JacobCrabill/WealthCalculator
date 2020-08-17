# /usr/bin/env python3
"""
TODO: Docstring
"""
import matplotlib.pyplot as plt

from income import Income
from loan import Loan
from savings import Savings
from retirement import Retirement


class Wealth:
    """ TODO
    Documentation goes here
    """

    def __init__(self):
        self.income = []
        self.loans = []
        self.savings = []
        self.expenses = {}
        self.month = 0

        # Storage for computed time-history of loans and savings accounts
        self.hist_loan = []
        self.hist_save = []

    def __str__(self):
        """ For use with print() """
        s = "\n"
        gross = 0
        for dolla in self.income:
            gross += dolla.income_month * 12
        s += f"Annual Gross Income: ${gross:.2f}\n"

        for loan in self.loans:
            s += loan.__str__()

        for save in self.savings:
            s += save.__str__()

        n = max([len(x) for x in s.expandtabs().split("\n")])

        s = '-'*n + s
        s += '-'*n
        s += "\n"

        return s

    def plot(self):
        """ Plot time histories of all accounts """

        # Loans
        plt.figure(1, figsize=(10, 4))
        plt.subplot(1, 2, 1)
        plt.title("Loan Balances")
        for loan in self.loans:
            plt.plot(loan.history, label=loan.name)

        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        # Savings
        plt.subplot(1, 2, 2)
        plt.title("Savings Balances")
        for save in self.savings:
            plt.plot(save.history, label=save.name)

        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def addIncome(self, income):
        """ Add a source of income """
        self.income.append(income)

    def addLoan(self, loan: Loan):
        """ Add a loan payment """
        self.loans.append(loan)

    def addSavings(self, savings: Savings):
        """ Add a savings account """
        self.savings.append(savings)

    def addExpense(self, expense: str, amount: float):
        """ Add a monthly expense """
        self.expenses[expense] = amount

    def step(self):
        """ Advance all accounts forward in time one month """
        print(f"**** Month {self.month+1} ****\n")

        total_savings_0 = 0
        for save in self.savings:
            if isinstance(save, Savings):
                total_savings_0 += save.balance

        for dolla in self.income:
            dolla.step()

        primeAcct = self.savings[0]

        for loan in self.loans:
            loan.step(primeAcct)

        for exp, amt in self.expenses.items():
            if amt <= 0:
                continue

            primeAcct.withdraw(amt)
            print(f"Withdraw ${amt:<7.2f} from {primeAcct.name} for {exp}")

        for save in self.savings:
            save.step()

        total_savings_1 = 0
        for save in self.savings:
            if isinstance(save, Savings):
                total_savings_1 += save.balance
        net_saved = total_savings_1 - total_savings_0
        print(f"~~ Net saved this month: ${net_saved:.2f} ~~\n")

        self.month += 1


if __name__ == "__main__":
    """ Sample of how to use the Wealth Calculator """
    # Need an instance of the Wealth class
    w = Wealth()

    # Add a high-yield savings account for our direct deposit
    hy_savings = Savings("High-Yield", 10000, 1.3/100.)

    # Add a second traditional savings account
    savings = Savings("Generic", 5000, .03/100)

    # Add sources of income (gross annual) and their tax rates
    # Set our high-yield savings account as the destination for our income
    income = Income(100000, tax_rate=.35, account=hy_savings)
    housing_allowance = Income(6000, tax_rate=.428, account=hy_savings)

    # Add our income streams to the Welath calculator
    w.addIncome(income)
    w.addIncome(housing_allowance)

    # Add a retirement account (like a savings account but can be used for pre-/post-tax deductions)
    retire = Retirement("401(k)", balance=1234.56, apy=.05, contribution=.07)

    # Setup our retirement account as a pre-tax deduction
    income.addPreTaxDeduction(retire)

    # Add our loan information
    w.addLoan(Loan("Refi", 54321.98, 4.5/100, 678.90))
    w.addLoan(Loan("Fed Loan", 8765, 3.7/100., 200))
    w.addLoan(Loan("Car", 5000, .02, 222.22))

    # Add our savings and retirement accounts (handled in the same manner for now)
    # NOTE: Right now, the 1st account added is used to deduct all expenses!
    w.addSavings(hy_savings)
    w.addSavings(savings)
    w.addSavings(retire)

    # Add out monthly expenses
    w.addExpense("Rent", 1800)
    w.addExpense("Food", 350)
    w.addExpense("Utilities", 150)
    w.addExpense("Misc", 500)

    w.addExpense("OneTime", 0)  # Placeholder for one-time expenses

    # Here's the simulation loop: Each step moves our accounts forward in time by one month
    # If you have any life events planned, account for them by modifying the expenses,
    # the loan rates, one-time loan or retirement deposits, etc.
    for i in range(0, 60):
        w.expenses["OneTime"] = 0  # Reset the one-time expenses

        if i > 0 and i % 12 == 0:
            # Boss man gives us a nice raise every year :)
            w.income[0].applyRaise(.03)
            # Landlord man raises the rent every year :(
            w.expenses["Rent"] *= 1.025

        if (i + 3) % 12 == 0:
            w.expenses["OneTime"] = 1500  # Annual spring break trip.
        
        if i == 12:
            retire.contribution = .11
            w.expenses["OneTime"] += 3000  # Trip to Mars.

        w.step()

    # Pretty-print the final balances
    print(w)

    # Plot the time histories
    w.plot()
