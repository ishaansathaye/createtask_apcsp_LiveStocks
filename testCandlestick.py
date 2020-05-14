import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from mplfinance.original_flavor import candlestick_ohlc
import numpy as np
import urllib.request
import datetime as dt


# Using SentDex method instead of pandas: fixed certificates problem

def bytespdate2num(b):
    return mdates.datestr2num(b.decode('utf-8'))


def graph_data(days):

    fig = plt.figure()
    ax1 = plt.subplot2grid((1, 1), (0, 0))

    stockPrice = 'https://pythonprogramming.net/yahoo_finance_replacement'
    sourceCode = urllib.request.urlopen(stockPrice).read().decode()
    stockData = []
    splitSource = sourceCode.split('\n')

    stDays = int(days)

    for line in splitSource[1:(stDays+1)]:
        splitLine = line.split(',')
        if len(splitLine) == 7:
            if 'values' not in line and 'labels' not in line:
                stockData.append(line)

    date, closep, highp, lowp, openp, adj_closep, volume = np.loadtxt(stockData, delimiter=',', unpack=True,
                                                                      converters={0: bytespdate2num})

    x = 0
    y = len(date)
    ohlc = []

    while x < y:
        appendMe = date[x], openp[x], highp[x], lowp[x], closep[x], volume[x]
        ohlc.append(appendMe)
        x += 1

    candlestick_ohlc(ax1, ohlc, width=0.4, colorup='g', colordown='r')

    for label in ax1.xaxis.get_ticklabels():
        # label.set_rotation(45)
        print(label)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    # ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax1.grid(True)

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('stock')
    # plt.legend()
    plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
    plt.show()
    

days = input('How many days of stock history?: ')
graph_data(days)
