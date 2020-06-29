#!/usr/local/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import pandas

from az_log import log_info, log_error
from pprint import pprint

def _plot_preprocess(data, category, mapping=None):
    spend, credit = data[0], data[1]
    plt.ylabel('Amount $')
    plt.xlabel(category);
    plt.title("Amount per {}".format(category));

    labels = sorted(list(set(spend.keys()).union(set(credit.keys()))))
    spend_x = [spend[l] if l in spend else 0 for l in labels]
    credit_x = [credit[l] if l in credit else 0 for l in labels]

    res = []
    for i in range(len(labels)):
        res.append((labels[i], spend_x[i], credit_x[i], mapping[labels[i]]))

    res.sort(key=lambda x:-x[1])

    return res

def print_table(data, category, mapping=None):
    log_info("Printting Table - {}".format(category))
    p = _plot_preprocess(data, category, mapping)

    df = pandas.DataFrame({
             'Class': [p[i][0] for i in range(len(p))],
             "Spend": [p[i][1] for i in range(len(p))],
             "Credit": [p[i][2] for i in range(len(p))],
	     "Comment": [p[i][3] for i in range(len(p))],
             })

    print(df.to_string())

def plot_bar_seaborn(data, category):
    log_info("Plotting Bar Chart - {}".format(category))
    p = _plot_preprocess(data, category)

    x = [p[i][0] for i in range(len(p))]
    y1 = [p[i][1] for i in range(len(p))]
    y2 = [p[i][2] for i in range(len(p))]

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

    p = _plot_preprocess(data, category)

    x = [p[i][0] for i in range(len(p))]
    y1 = [p[i][1] for i in range(len(p))]
    y2 = [p[i][2] for i in range(len(p))]

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

