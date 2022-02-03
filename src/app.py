import os
import streamlit as st
import datetime
import pandas as pd

from common.logger import init_logger, timeit
from config.fund_screener import FundScreenerConfig
from common.utils import (
    load_funds, load_yf_hist
)

TIMEFRAMES = {
    '1m': '1 month',
    '3m': '3 months',
    '6m': '6 months',
    '1y': '1 year',
    '3y': '3 years',
    '5y': '5 years'
}


def main():
    logger = init_logger(os.path.basename(__file__).split(".")[0])
    cfg = FundScreenerConfig()
    logger.info(f"cfg: {cfg}")

    # Load fund tickers from the universe file
    funds = load_funds(cfg.univ)
    num_funds = len(funds)
    logger.info(f"Number of funds loaded: {num_funds}")

    # Register your pages
    pages = {
        "Overview": page_overview,
        "Sectors Screener": page_sectors,
        "Porfolio Simulator": page_portfolio
    }

    st.sidebar.title("Simple Funds Screener")

    # Widget to select your page, you can choose between radio buttons or a selectbox
    page = st.sidebar.radio("Select your page", tuple(pages.keys()))
    #page = st.sidebar.selectbox("Select your page", tuple(pages.keys()))

    # Display the selected page
    pages[page]()


def page_overview():
    st.title("Funds Overview")
    d = st.date_input(
        "Reference date",
        datetime.date(2020, 10, 1)
    )
    option = st.selectbox(
        'Select time frame',
        options=list(TIMEFRAMES.keys()),
        format_func=format_func
    )
    st.write('You selected:', option)

    # Display funds data
    df = pd.read_csv("etfdb/etfs_details_type_fund_flow.csv")
    st.dataframe(df.head())


def page_sectors():
    st.title("This is my second page")
    # ...


def page_portfolio():
    st.title("This is my third page")
    #


def format_func(option):
    return TIMEFRAMES[option]


if __name__ == "__main__":
    main()
