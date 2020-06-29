#!/usr/local/bin/python3

import csv
import os
import pandas
import sys
import time

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from collections import defaultdict
from datetime import datetime
from pprint import pprint 

from az_log import log_info, log_warn, log_debug, log_error
from az_constants import AMEX_CSV_HEADER

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

def _plot_preprocess(data, category):
    spend, credit = data[0], data[1]
    plt.ylabel('Amount $')
    plt.xlabel(category);
    plt.title("Amount per {}".format(category));

    labels = sorted(list(set(spend.keys()).union(set(credit.keys()))))
    spend_x = [spend[l] if l in spend else 0 for l in labels]
    credit_x = [credit[l] if l in credit else 0 for l in labels]

    return (labels, spend_x, credit_x)

def plot_bar_seaborn(data, category):
    log_info("Plotting Bar Chart - {}".format(category))
    x, y1, y2 = _plot_preprocess(data, category)

    df = pandas.DataFrame({
             'Class': x + x,
	     "Spend/Credit": ["Spend"] * len(x) + ["Credit"] * len(x),
	     "Amount": y1 + y2,
	     })
    log_info(df.to_string())
    sns.catplot(x="Class", y="Amount", hue="Spend/Credit", data=df, kind='bar')
    plt.draw()
    plt.pause(0.001)
    input("Press enter to continue...")
    plt.close()

def plot_bar_matplotlib(data, category):
    log_info("Plotting Bar Chart - {}".format(category))

    x, y1, y2 = _plot_preprocess(data, category)
    ind = np.arange(len(x))

    width = 0.35
    plt.bar(ind, y1, width, label='Spend')
    plt.bar(ind + width, y2, width, label='Credit')
    plt.xticks(ind + width / 2, x)
    plt.legend(loc='best')

    plt.draw()
    plt.pause(0.001)
    input("Press enter to continue...")
    plt.close()

def visualize(data, category):
    log_info("Visualizing ...")
    #pprint(data)
    plot_bar_seaborn(data, category)

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
