# Memory
import os
import psutil
process = psutil.Process()

# Time
import time
start_time = time.time()

# Stocks
import yfinance as yf
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import csv
import pandas as pd
import matplotlib.dates as mdates
import datetime as dt
from datetime import timedelta
import matplotlib.ticker as mticker
import matplotlib.animation as animation



fig = plt.figure()
ax1 = plt.subplot2grid((1, 1), (0, 0))



def animate(i):
    stock = yf.Ticker("NVDA")

    hist = stock.history(period="5d", rounding=True)
    
    # putting data into csv
    dateData = hist['Close']
    dateData.to_csv('date.csv')
    dateOHLC = []
    with open('date.csv') as f:
        reader = csv.reader(f, delimiter=",")
        next(f)
        for i in reader:
            dateOHLC.append(i[0])

    openData = hist['Open']
    openData.to_csv('open.csv')
    openOHLC = []
    with open('open.csv') as f:
        reader = csv.reader(f, delimiter=",")
        next(f)
        for i in reader:
            openOHLC.append(i[1])

    highData = hist['High']
    highData.to_csv('high.csv')
    highOHLC = []
    with open('high.csv') as f:
        reader = csv.reader(f, delimiter=",")
        next(f)
        for i in reader:
            highOHLC.append(i[1])

    lowData = hist['Low']
    lowData.to_csv('low.csv')
    lowOHLC = []
    with open('low.csv') as f:
        reader = csv.reader(f, delimiter=",")
        next(f)
        for i in reader:
            lowOHLC.append(i[1])

    closeData = hist['Close']
    closeData.to_csv('close.csv')
    closeOHLC = []
    with open('close.csv') as f:
        reader = csv.reader(f, delimiter=",")
        next(f)
        for i in reader:
            closeOHLC.append(i[1])

    #converting prices into int
    def convertArratInt(array):
        for i in range(0, len(array)): 
            array[i] = float(array[i]) 
    convertArratInt(openOHLC)
    convertArratInt(highOHLC)
    convertArratInt(lowOHLC)
    convertArratInt(closeOHLC)

    # converting date into num
    newdateOHLC = []
    def convertDate2Num(array):
        for i in array:
            dateTimeOBJ = dt.datetime.strptime(i, '%Y-%m-%d')
            t1 = dateTimeOBJ.timetuple()
            newformat = time.mktime(t1)
            newdateOHLC.append(newformat)
    convertDate2Num(dateOHLC)

    # appending required data for candlestick chart
    x = 0
    y = len(newdateOHLC)
    ohlc = []
    while x < y:
        appendMe = newdateOHLC[x], openOHLC[x], highOHLC[x], lowOHLC[x], closeOHLC[x]
        ohlc.append(appendMe)
        x += 1

    ax1.clear()
    ax1.grid(True)
    candlestick_ohlc(ax1, ohlc, width=10000, colorup='g', colordown='r')

# ax1.xaxis.set_major_locator(xmajor_locator)
# for label in ax1.xaxis.get_ticklabels():
#         print(label)
# ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d-%Y'))

plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Stock Name')
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()

# print()
# print("%s seconds" % (time.time() - start_time))
# print(str((process.memory_info().rss)/1000000) + " MB") # in bytes

