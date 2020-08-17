#!/usr/bin/env python3


class Income:
    """ TODO
    Documentation goes here
    """

    def __init__(self, gross_annual, tax_rate, account=None):
        self.income_month = gross_annual / 12.
        self.pretax = []
        self.posttax = []
        self.deposit_acct = account
        self.tax_rate = tax_rate

        # Temporary variable to store monthly income while applying deductions
        self.income = 0

    def addPreTaxDeduction(self, ded):
        """ Add a pre-tax deduction/account """
        self.pretax.append(ded)

    def addPostTaxDeduction(self, ded):
        """ Add a post-tax deduction/account """
        self.posttax.append(ded)

    def setDepositAccount(self, acct):
        """ Setup 'direct deposit' account """
        self.deposit_acct = acct

    def applyPreTax(self):
        """ Apply all pre-tax deductions """
        for ded in self.pretax:
            ded.setIncome(self.income_month)
            amt = ded.applyDeduction()
            self.income -= amt
            print(f"Deduct ${amt:.2f} pre-tax for {ded.name}")

    def applyTax(self):
        """ Remove taxes from income """
        self.income *= (1 - self.tax_rate)

    def applyPostTax(self):
        """ Apply all automatic post-tax deductions """
        for ded in self.posttax:
            amt = ded.applyDeduction()
            self.income -= amt

    def deposit(self):
        """ Deposit remainder into our deposit account """
        self.deposit_acct.deposit(self.income)
        print(f"Deposit ${self.income:.2f} into {self.deposit_acct.name}")
        self.income = 0

    def applyRaise(self, raise_pct):
        """ Increase gross income by the given percentage """
        self.income_month *= (1 + raise_pct)

    def step(self):
        """ Step forward one month """
        self.income = self.income_month
        self.applyPreTax()
        self.applyTax()
        self.applyPostTax()
        self.deposit()
