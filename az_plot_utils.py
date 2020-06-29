#!/usr/local/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import pandas

from az_log import log_info, log_error

def _plot_preprocess(data, category):
    spend, credit = data[0], data[1]
    plt.ylabel('Amount $')
    plt.xlabel(category);
    plt.title("Amount per {}".format(category));

    labels = sorted(list(set(spend.keys()).union(set(credit.keys()))))
    spend_x = [spend[l] if l in spend else 0 for l in labels]
    credit_x = [credit[l] if l in credit else 0 for l in labels]

    return (labels, spend_x, credit_x)

def print_table(data, category):
    log_info("Printting Table - {}".format(category))
    x, y1, y2 = _plot_preprocess(data, category)

    df = pandas.DataFrame({
             'Class': x,
             "Spend": y1,
             "Credit": y2,
             })

    print(df.to_string())

def plot_bar_seaborn(data, category):
    log_info("Plotting Bar Chart - {}".format(category))
    x, y1, y2 = _plot_preprocess(data, category)

    df = pandas.DataFrame({
             'Class': x + x,
	     'Spend/Credit': ["Spend"] * len(x) + ["Credit"] * len(x),
	     'Amount': y1 + y2,
	     })
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

