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


# getting runtime and memory program used up
def time_memory():
    print()
    print("%s seconds" % round((time.time() - start_time)))
    print(str(round((process.memory_info().rss)/1000000)) + " MB") # in bytes


# plot size, labels, grid, and different axes
fig = plt.figure(figsize=(20,10.7)) # size for bigger screens (20, 10.7)
ax1 = plt.subplot2grid((4, 1), (2, 0), rowspan=2, colspan=1)
ax1.grid(False)
plt.xlabel('Date')
plt.ylabel('Price')
ax2 = plt.subplot2grid((4, 1), (0, 0), rowspan=2, colspan=1) 


# getting stock information using yfinance library
stock = yf.Ticker("TSLA")
hist = stock.history(period="5d", rounding=True)


# parsing date data, converting to string and creating array
dateData = hist.index
dateOHLC = []
for i in dateData:
    i = str(i)
    dateOHLC.append(i)


# parsing open stock info and adding data to array
openOHLC = hist["Open"].tolist()

# parsing high stock info and adding data to array
highOHLC = hist["High"].tolist()

# parsing low stock info and adding data to array
lowOHLC = hist["Low"].tolist()

# parsing close stock info and adding data to array
closeOHLC = hist["Close"].tolist()


#converting prices into int
def convertArratInt(array):
    for i in range(0, len(array)): 
        array[i] = float(array[i]) 
convertArratInt(openOHLC)
convertArratInt(highOHLC)
convertArratInt(lowOHLC)
convertArratInt(closeOHLC)

# converting date into correct num format
def bytespdate2num(b):
    return mdates.datestr2num(b)
newdateOHLC = []
def convertDate2Num(array):
    for i in array:
        # dateTimeOBJ = dt.datetime.strptime(i, '%Y-%m-%d')
        # t1 = dateTimeOBJ.timetuple()
        newformat = bytespdate2num(i)
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

# animating data for first graph displaying close prices
def animate(i):
    ticker = yf.Ticker('TSLA')
    tsla_df = ticker.history(period="5d")
    ax2 = tsla_df['Close']
    # stockLive = yf.Ticker("AAPL")
    # liveDate = []
    # dateDataLive = hist.index
    # for i in dateDataLive:
    #     i = str(i)
    #     liveDate.append(i)
    # liveClose = hist["Close"].tolist()
        
    
    # ax2.grid(True)
    plt.title('Stock Name')
    # plt.xlabel('')
    # plt.setp(ax2.get_xticklabels(), visible=False) # hiding top graph x axis labels
    ax2.plot()


candlestick_ohlc(ax1, ohlc, width=1./24, colorup='g', colordown='r') # adding data to candlestick chart
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.subplots_adjust(left=0.05, bottom=0.11, right=0.9, top=0.95, wspace=0.2, hspace=0.73) # adjusting window
for label in ax1.xaxis.get_ticklabels(): # rotating date labels on x axis
        label.set_rotation(45)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d-%Y')) # converting x-axis to proper date format
plt.show()

# time_memory()