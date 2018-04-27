# Avalanche
Avalanche is a simple payoff calculator utilizing the avalanche philosophy of debt management.

## Avalanche Philosophy
The avalanche philosophy emphasizes paying off debts in order from highest interest rate to lowest interest rate. When a debt is paid off, the monthly payment from that finished debt is applied towards the next highest debt. This moves forward the expected payoff date of other debts, at the expense of not returning any freed up debt payments to your cash flow until all debts have been paid off.

## Usage
./payoff.py DEBT [EXTRA]

Where DEBT is the path to a file whose format appears below, and EXTRA is an optional parameter specifying a monthly amount on top of minimum monthly payments.

**Example with only monthly minimums:**

./payoff.py debts.json

**Example with extra cash put towards debt:**

./payoff.py debts.json 50.00

## Input
The JSON formatted file can have any name. The file does not need to be ordered in any way. An example file `debts.json` would appear as follows:

```
[
  {
    "name": "Student Loan #1",
    "amount": 962.91,
    "rate": 0.0303,
    "payment": 25.08
  },
  {
    "name": "Student Loan #2",
    "amount": 3288.67,
    "rate": 0.0596,
    "payment": 43.82
  }
]
```

## Warning
TLDR: Your mileage may vary.

This tool does not capture the complexity of every financial situation. This tool makes the following assumptions, which may not hold for your situation:
- The debt compounds monthly. Your debt may compound daily or at another frequency.
- The debt compounds each month before the payment is made.
- All debt is in repayment from the first month. Some of your debts may be in a grace period and don't require repayment right away.

For any of these reasons a discrepancy can arise between the final month you pay off your debt and the final month this tool predicts you will pay off your debt. This discrepancy will be small at first but exacerbate the more months it takes.
