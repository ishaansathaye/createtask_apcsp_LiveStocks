import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from mplfinance.original_flavor import candlestick_ohlc
import numpy as np
import urllib.request
from matplotlib import style

style.use('fivethirtyeight')

MA1 = 10
MA2 = 30

def highMinusLow(high, low):
    return high-low


def movingAverage(value, window):
    weights = np.repeat(1.0, window)/window
    smas = np.convolve(value, weights, 'valid')
    return smas


def bytespdate2num(b):
    return mdates.datestr2num(b.decode('utf-8'))


def graph_data(days):
    fig = plt.figure()
    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=1, colspan=1)
    plt.title('Stock Info')
    plt.ylabel('H-L')
    ax2 = plt.subplot2grid((6, 1), (1, 0), rowspan=4, colspan=1, sharex=ax1)
    # plt.xlabel('Date')
    plt.ylabel('Price')
    ax2v = ax2.twinx() # truly share that x-axis
    ax3 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
    plt.ylabel('MovingAvgs')

    stockPrice = 'https://pythonprogramming.net/yahoo_finance_replacement'
    sourceCode = urllib.request.urlopen(stockPrice).read().decode()
    stockData = []
    splitSource = sourceCode.split('\n')

    intDays = int(days)

    for line in splitSource[1:(intDays+1)]:
        splitLine = line.split(',')
        if len(splitLine) == 7:
            if 'values' not in line and 'labels' not in line:
                stockData.append(line)

    date, closep, highp, lowp, openp, adj_closep, volume = np.loadtxt(stockData, delimiter=',', unpack=True,
                                                                      converters={0: bytespdate2num})
    print(date)
    x = 0
    y = len(date)
    ohlc = []

    while x < y:
        appendMe = date[x], openp[x], highp[x], lowp[x], closep[x], volume[x]
        ohlc.append(appendMe)
        x += 1

    ma1 = movingAverage(closep, MA1)
    ma2 = movingAverage(closep, MA2)
    start = len(date[MA2-1:])

    h_l = list(map(highMinusLow, highp, lowp))

    ax1.plot_date(date[-start:], h_l[-start:], '-', label='H-L')
    ax1.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4, prune='lower'))

    candlestick_ohlc(ax2, ohlc[-start:], width=0.4, colorup='g', colordown='r')

    ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=7, prune='upper'))
    ax2.grid(True)

    bbox_props = dict(boxstyle='round', fc='w', ec='k', lw=1)  # adding annotation for last price
    ax2.annotate(str(closep[0]), (date[0], closep[0]), xytext=(date[-start] + 4, closep[-start]), bbox=bbox_props, fontsize='xx-small')
    ax2v.plot([], [], color='#007983', alpha=0.4, label='Volume')
    ax2v.fill_between(date[-start:], 0, volume[-start:], facecolor='#007983', alpha=0.4)
    ax2v.axes.yaxis.set_ticklabels([])
    ax2v.grid(False)
    ax2v.set_ylim(0, 3*volume.max())

    ax3.plot(date[-start:], ma1[-start:], linewidth=3, label=str(MA1)+'MA1')
    ax3.plot(date[-start:], ma2[-start:], linewidth=3, label=str(MA2)+'MA2')
    ax3.fill_between(date[-start:], ma2[-start:], ma1[-start:], where=(ma1[-start:] < ma2[-start:]), facecolor='r', edgecolor='r', alpha=0.5)
    ax3.fill_between(date[-start:], ma2[-start:], ma1[-start:], where=(ma1[-start:] > ma2[-start:]), facecolor='g', edgecolor='g', alpha=0.5)
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d-%Y'))
    ax3.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax3.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4, prune='upper'))
    for label in ax3.xaxis.get_ticklabels():
        label.set_rotation(45)
    

    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.setp(ax2.get_xticklabels(), visible=False)
    plt.subplots_adjust(left=0.11, bottom=0.24, right=0.9, top=0.90, wspace=0.2, hspace=0)
    ax1.legend()
    leg = ax1.legend(loc=9, ncol=2, prop={'size':11})
    leg.get_frame().set_alpha(0.4)
    ax2v.legend()
    leg = ax2v.legend(loc=9, ncol=2, prop={'size':11})
    leg.get_frame().set_alpha(0.4)
    ax3.legend()
    leg = ax3.legend(loc=9, ncol=2, prop={'size':11})
    leg.get_frame().set_alpha(0.4)
    plt.show()

graph_data(days=input('How many days of stock history?: '))