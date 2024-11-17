# flake8: noqa
# fmt: off

from datetime import datetime

import mplfinance as mpf
import pandas as pd

# %%
import yfinance as yf

# %%
stock = yf.Ticker("AAPL")

# get historical market data
hist = stock.history(period="1y")
hist.head()
# %%

# plot price line chart with volume
mpf.plot(hist, type='line', volume=True)
# %%

mpf.plot(
    hist['2024-08':'2024-11'],
    figratio=(20, 12),
    type='candle',
    title='Apple Share Price',
    mav=20,
    volume=True,
    tight_layout=True,
    style='yahoo'
)
# %%
