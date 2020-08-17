#!/usr/bin/env python3

from savings import Savings


class Retirement(Savings):
    """ TODO
    Documentation goes here
    """

    def __init__(self, name, balance, apy, contribution, income=0):
        super().__init__(name, balance, apy)

        self.contribution = contribution
        self.income = income

    def getContribution(self):
        """ Return the contribution amount as % of income """
        return self.contribution

    def setIncome(self, income):
        """ Set the monthly income on which our contribution is based """
        self.income = income

    def applyDeduction(self):
        deposit = self.contribution * self.income
        self.deposit(deposit)
        return deposit
