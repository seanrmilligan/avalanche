#!/usr/bin/env python3

import json
import operator
import sys

description = [
	'    This tool takes in a list of debts (see DEBT) and uses the',
	'    avalanche philosophy of debt management to pay off debts. Each time',
	'    a debt is paid off, its payment amount (along with any EXTRA) will be',
	'    put towards the next highest paying debt.'
]
usageopts = [
	'    {:s} DEBT [EXTRA]'
]
usageargs = [
	'    DEBT',
	'        The file detailing debts in a JSON array format. Each element in the',
	'        array must have a debt name `name`, debt amount `amount`, interest rate',
	'        `rate`, and a minimum payment `payment`.',
	'    EXTRA',
	'        The extra amount to be paid each month, which will be allocated to the next highest debt.'
]

def help(progname):
	print('NAME')
	print('    {:s}'.format(progname))
	print()
	
	print('DESCRIPTION')
	for line in description:
		print(line)
	print()

	print('USAGE')
	for line in usageopts:
		print(line.format(progname))
	print()

	print('PARAMETERS')
	for line in usageargs:
		print(line)
	print()


def print_table(debts, extra_payments):
	zero_balance = False
	
	print_colnames(debts)
	
	# each iteration is a month
	while not zero_balance:
		zero_balance = all(debt['amount'] == 0 for debt in debts)

		# show monthly balance before any interest or payments
		print_row((debt['amount'] for debt in debts), 'starting amount')

		# calculate and show monthly interest
		interest = calculate_interest(debts)
		print_row(interest, 'interest')

		# add interest to the debt (this assumes monthly compounding)
		apply(debts, interest)
		print_row((debt['amount'] for debt in debts), 'new amount')

		# show minimum payments, then take them out of remaining debt
		minimum_payments = [-min(debt['payment'], debt['amount']) for debt in debts]
		print_row(minimum_payments, 'minimum payments')
		unused_minimum_payments = make_minimum_payments(debts)

		excess = calculate_excess(debts, unused_minimum_payments + extra_payments)
		print_row(excess, 'excess payments')

		# reduce highest rate debts first (debts were sorted by rate)
		apply(debts, excess)

		print_row((debt['amount'] for debt in debts), 'ending amount')
		print()

def print_colnames(debts):
	for debt in debts:
		print('{:>12}'.format(debt['name']), end=' | ')
	print('\n')

def print_row(values, end):
	for value in values:
		print('{:12.2f}'.format(value), end=' | ')
	print(end)

def calculate_interest(debts):
	return [debt['amount'] * (debt['rate'] / 12) if debt['amount'] > 0 else 0 for debt in debts]

def apply(debts, amount):
	for i in range(len(debts)):
		debts[i]['amount'] = debts[i]['amount'] + amount[i]

def calculate_excess(debts, excess):
	excess_payments = []
	for debt in debts:
		if debt['amount'] > 0 and excess > 0:
			if excess > debt['amount']:
				excess_payments.append(-debt['amount'])
				excess = excess - debt['amount']
			else:
				excess_payments.append(-excess)
				excess = 0
		else:
			excess_payments.append(-0.0)

	return excess_payments

def make_minimum_payments(debts):
	excess = 0

	for debt in debts:
		if debt['amount'] > 0:
			# see if we're about to pay off the debt
			if debt['payment'] > debt['amount']:
				# track the excess so that we can apply it to another debt
				excess = excess + (debt['payment'] - debt['amount'])
				# wipe out the debt
				debt['amount'] = 0
			else:
				# apply a regular payment
				debt['amount'] = debt['amount'] - debt['payment']
		else:
			# take the payment and set it aside to apply to another debt
			excess = excess + debt['payment']

	return excess

def load_debts(file_name):
	debts = None
	with open(file_name) as debt_file:
		# sort the debt by rate, highest rate first
		debts = sorted(json.load(debt_file), key=lambda d: d['rate'], reverse=True)
	return debts

if __name__ == '__main__':
	progname = sys.argv[0]
	argc = len(sys.argv)
	file_name = ''
	extra_payments = 0.0

	if argc >= 4:
		help(progname)
		sys.exit(1)
	if argc >= 3:
		extra_payments = float(sys.argv[2])
	if argc >= 2:
		file_name = sys.argv[1]
	if argc == 1:
		help(progname)
		sys.exit(1)

	debts = load_debts(file_name)
	print_table(debts, extra_payments)