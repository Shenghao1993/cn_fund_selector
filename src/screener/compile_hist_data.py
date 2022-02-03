import os
import click
import yaml
import time
import pandas as pd
from datetime import datetime, timedelta

from src.common.logger import init_logger, timeit
from src.config.fund_screener import FundScreenerConfig
from src.common.utils import (
    load_funds, load_yf_hist
)


@click.command()
@click.option('-w', '--agg_window', help="Aggregation window")
@click.option('-e', '--end_date', help="End date in yyyy-mm-dd")
def main(agg_window, end_date):
    logger = init_logger(os.path.basename(__file__).split(".")[0])
    cfg = FundScreenerConfig()
    logger.info(f"cfg: {cfg}")

    # Load fund tickers from the universe file
    funds = load_funds(cfg['univ'])
    num_funds = len(funds)
    logger.info("Number of funds loaded: %s", num_funds)
    agg_price_df, agg_vol_df = compile(
        logger, funds, end_date, agg_window, cfg['output']
    )
    logger.info(agg_price_df.head(20))


def compile(logger, funds, end_date, agg_window, hist_dir):
    start_date = _interpret_agg_window(logger, end_date, agg_window)
    agg_price_df = pd.DataFrame()
    agg_vol_df = pd.DataFrame()
    for fund in funds[:3]:
        hist_dir = hist_dir.format(ticker=fund, yyyy='*')
        price_df, vol_df = load_yf_hist(fund, hist_dir)
        price_df = price_df[
            (price_df['Date'] >= start_date) & (price_df['Date'] <= end_date)
        ].set_index('Date')
        vol_df = vol_df[
            (vol_df['Date'] >= start_date) & (vol_df['Date'] <= end_date)
        ].set_index('Date')
        agg_price_df = pd.concat([agg_price_df, price_df], axis=1)
        agg_vol_df = pd.concat([agg_vol_df, vol_df], axis=1)
    return (agg_price_df, agg_vol_df)


def _interpret_agg_window(logger, end_date, agg_window):
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


if __name__ == "__main__":
    main()
