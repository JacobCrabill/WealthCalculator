# WealthCalculator

Personal finance calculator for loans, savings, and retirement.  Use at your own risk.  

**See wealth.py for the top-level calculator class and an example use case using made-up numbers.**

## Goal

Have a (relatively) simple way of simulating personal income and savings over time with a reasonable level of fideltiy, including the ability to set future events such as pay raises, buying a house, and drawing from a retirement account.

## Desired Code Structure

All calculations are done on a monthly basis.
Personal wealth is modeled as a collection of objects describing income, debt, expenses, etc. which can have monthly effects.
Events can modify, add, and remove objects from the simulation at predefined or dynamic time values.

### Objects

* Cash savings
* Income
* Taxes
* Debt (loans)
* Expenses (Rent, food, utilities, etc.)
* Retirement savings

### Events

* Pay raise
* Expense adjustment (i.e. rent increase/decrease)
* One-time expenses
* Debt refinance or payoff
* Take on debt (i.e. mortgage)
* Retirement start
