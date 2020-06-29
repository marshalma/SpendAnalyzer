#!/usr/local/bin/python3

import csv
import os
import sys
import time

from collections import defaultdict
from datetime import datetime
from pprint import pprint 

from az_log import log_info, log_warn, log_debug, log_error
from az_constants import AMEX_CSV_HEADER
from az_plot_utils import print_table, plot_bar_seaborn, plot_bar_matplotlib

def locate_amex_csv(directory):
    # TODO: verify that csv is AMEX specific
    files = list(filter(lambda x: x.endswith("csv"), os.listdir(directory)))
    return [os.path.join(directory, f) for f in files]

def read_amex_csv(files):
    transactions = []

    for f in files:
        fp = open(f, 'r')
        csvreader = csv.reader(fp)
        for row in csvreader:
            if row[0].startswith("Date"):
                continue

            transactions.append(row)
        fp.close()

    log_info("Found {} transactions".format(len(transactions)))
    return transactions

def _aggregate_by_month(data):
    spending = defaultdict(int)
    credit = defaultdict(int)
    date_idx = AMEX_CSV_HEADER.index("Date")
    amount_idx = AMEX_CSV_HEADER.index("Amount")

    for entry in data:
        date = entry[date_idx]
        month = datetime.strptime(date, "%m/%d/%y").strftime("20%y/%m")

        amount = float(entry[amount_idx])

        if amount >= 0:
            spending[month] += amount
        else:
            credit[month] += -amount 
    spending, credit = dict(spending), dict(credit)
    return spending, credit

def _aggregate_by_column(data, column):
    spending = defaultdict(int)
    credit = defaultdict(int)
    col_idx = AMEX_CSV_HEADER.index(column) if column in AMEX_CSV_HEADER else -1
    amount_idx = AMEX_CSV_HEADER.index("Amount")

    for entry in data:
        amount = float(entry[amount_idx])
        keyname = entry[col_idx] if col_idx > 0 else "Total"

        if amount >= 0:
            spending[keyname] += amount
        else:
            credit[keyname] += -amount

    spending, credit = dict(spending), dict(credit)
    return spending, credit

def _aggregate_by_category(data):
    return _aggregate_by_column(data, "Category")

def _aggregate_by_merchant(data):
    return _aggregate_by_column(data, "Description")

def _aggregate_total(data):
    return _aggregate_by_column(data, "Total")

AGGR_METHODS = {
    "Month": _aggregate_by_month,
    "Category": _aggregate_by_category,
    "Merchant": _aggregate_by_merchant,
    "Total": _aggregate_total,
}

def aggregate_result(data, method):
    return method(data)

def visualize(data, category):
    log_info("Visualizing ...")
    print_table(data, category)

def main():
    csv_directory = sys.argv[1]
    files = locate_amex_csv(csv_directory)
    data = read_amex_csv(files)

    for method, func in AGGR_METHODS.items():
        log_info("Aggregating data by {}".format(method))
        data_aggr = aggregate_result(data, func)
        visualize(data_aggr, method)

    log_info("Completed!")

if __name__ == "__main__":
    main()
