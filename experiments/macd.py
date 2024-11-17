# flake8: noqa
# fmt: off

# %%
from typing import List

import mplfinance as mpf
import pandas as pd
import yfinance as yf

# %%
stock = yf.Ticker("AAPL")

# get historical market data
# df = stock.history(period="1y")
df = stock.history(period="6mo")
df.head()
# %%
#
# Plot price line chart with volume
#
mpf.plot(df, type='line', volume=True)
# %%

mpf.plot(
    df['2024-08':'2024-11'],
    figratio=(20, 12),
    type='candle',
    title='Apple Share Price',
    mav=20,
    volume=True,
    tight_layout=True,
    style='yahoo'
)
# %%
#
# Calculate MACD
#
# Get the 26-day EMA of the closing price
k = df['Close'].ewm(span=12, adjust=False, min_periods=12).mean()

# Get the 12-day EMA of the closing price
d = df['Close'].ewm(span=26, adjust=False, min_periods=26).mean()

# Subtract the 26-day EMA from the 12-Day EMA to get the MACD
macd = k - d

# Get the 9-Day EMA of the MACD for the Trigger line
macd_s = macd.ewm(span=9, adjust=False, min_periods=9).mean()

# Calculate the difference between the MACD - Trigger for the Convergence/Divergence value
macd_h = macd - macd_s

# Add all of our new values for the MACD to the dataframe
df['MACD_12_26_9'] = df.index.map(macd)
df['MACDh_12_26_9'] = df.index.map(macd_h)
df['MACDs_12_26_9'] = df.index.map(macd_s)

df.tail()
# %%
#
# Generate color for histogram
#
def gen_macd_color(df: pd.DataFrame) -> List[str]:
    macd_color = []
    macd_color.clear()

    for i in range (0,len(df["MACDh_12_26_9"])):
        if df["MACDh_12_26_9"][i] >= 0 and df["MACDh_12_26_9"][i-1] < df["MACDh_12_26_9"][i]:
            # green
            macd_color.append('#26A69A')

        elif df["MACDh_12_26_9"][i] >= 0 and df["MACDh_12_26_9"][i-1] > df["MACDh_12_26_9"][i]:
            # faint green
            macd_color.append('#B2DFDB')
            #print(i,'faint green')

        elif df["MACDh_12_26_9"][i] < 0 and df["MACDh_12_26_9"][i-1] > df["MACDh_12_26_9"][i] :
            # red
            macd_color.append('#FF5252')

        elif df["MACDh_12_26_9"][i] < 0 and df["MACDh_12_26_9"][i-1] < df["MACDh_12_26_9"][i] :
            # faint red
            macd_color.append('#FFCDD2')

        else:
            # no color
            macd_color.append('#000000')

    return macd_color

macd = df[['MACD_12_26_9']]
histogram = df[['MACDh_12_26_9']]
signal = df[['MACDs_12_26_9']]
macd_color = gen_macd_color(df)

# %%
apds = [
    mpf.make_addplot(macd, color='#2962FF', panel=1),
    mpf.make_addplot(signal, color='#FF6D00', panel=1),
    mpf.make_addplot(histogram,type='bar',width=0.7,panel=1, color=macd_color,alpha=1,secondary_y=True),
]

mpf.plot(
    df,
    volume=True,
    type="candle",
    style="yahoo",
    addplot=apds,
    volume_panel=2,
    figsize=(20,10)
)
# %%
