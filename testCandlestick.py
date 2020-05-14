import yfinance as yf
import matplotlib as mpl

ticker = yf.Ticker('TSLA')

tsla_df = ticker.history(period="5d")

tsla_df['Close'].plot(title="TSLA's stock price")

plt.show()