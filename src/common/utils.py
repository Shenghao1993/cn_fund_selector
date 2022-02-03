import pandas as pd
from glob import glob
from datetime import datetime, timedelta


def load_funds(univ_file):
    with open(univ_file, 'r') as f:
        funds = [ticker.replace('\n', '') for ticker in f.readlines()]
    return funds


def load_yf_hist(ticker, hist_dir):
    price_cols = ['Date', 'Adj Close']
    vol_cols = ['Date', 'Volume']
    hist_price_df = pd.DataFrame()
    hist_vol_df = pd.DataFrame()
    for hist_file in glob(hist_dir):
        df = pd.read_csv(hist_file)
        hist_price_df = pd.concat([hist_price_df, df[price_cols]])
        hist_vol_df = pd.concat([hist_vol_df, df[vol_cols]])
    return (hist_price_df, hist_vol_df)


def agg_fund_pv(logger, tickers, edate, timeframe):
    sdate = interpret_agg_window(logger, edate, timeframe)
    pdata = pd.DataFrame()
    vdata = pd.DataFrame()
    for ticker in tickers:


def interpret_agg_window(logger, end_date, agg_window):
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    duration = int(agg_window[:-1])
    unit = agg_window[-1]
    if unit == 'd':
        start_date = end_date - timedelta(days=duration)
    elif unit == 'm':
        start_date = end_date - timedelta(months=duration)
    elif unit == 'y':
        start_date = end_date - timedelta(years=duration)
    else:
        logger.exception(f"Invalid aggregation window given: {agg_window}")
        return
    return start_date.strftime('%Y-%m-%d')
