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
import matplotlib.ticker as mticker



fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

stock = yf.Ticker("NVDA")

hist = stock.history(period="1mo", rounding=True)

# for item in hist:
#     print(item.Open)

# df = pd.DataFrame(hist)
# print(df)
# print(df['Open'])



# myvalues = [i['2020-05-07'] for i in hist if '2020-05-07' in i]
# print(hist['Date'])

# print(hist['Close'])

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

# ohlc = []

# ohlc.append(dateOHLC)
# ohlc.append(openOHLC)
# ohlc.append(highOHLC)
# ohlc.append(lowOHLC)
# ohlc.append(closeOHLC)

def convertArratInt(array):
    for i in range(0, len(array)): 
        array[i] = float(array[i]) 

convertArratInt(openOHLC)
convertArratInt(highOHLC)
convertArratInt(lowOHLC)
convertArratInt(closeOHLC)

newdateOHLC = []
def convertDate2Num(array):
    for i in array:
        dateTimeOBJ = dt.datetime.strptime(i, '%Y-%m-%d')
        t1 = dateTimeOBJ.timetuple()
        newformat = time.mktime(t1)
        newdateOHLC.append(newformat)
convertDate2Num(dateOHLC)

x = 0
y = len(newdateOHLC)
ohlc = []
while x < y:
    appendMe = newdateOHLC[x], openOHLC[x], highOHLC[x], lowOHLC[x], closeOHLC[x]
    ohlc.append(appendMe)
    x += 1


    


# hist['Close'].plot()
# ohlc = []
# appendMe = hist['Close'], hist['Open'], hist['High'], hist['Low'], hist['Volume']
# ohlc.append(appendMe)

# hist.plot()
candlestick_ohlc(ax1, ohlc, width=0.4, colorup='g', colordown='r')
# for label in ax1.xaxis.get_ticklabels():
#         label.set_rotation(45)
# ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y-%d'))
ax1.grid(True)
plt.show()

# print()
# print("%s seconds" % (time.time() - start_time))
# print(str((process.memory_info().rss)/1000000) + " MB") # in bytes

