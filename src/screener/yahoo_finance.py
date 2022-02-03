import os
import click
import yaml
import time
import yfinance as yf
from addict import Dict as Addict
from pathlib import Path
from datetime import datetime, timedelta

from src.common.logger import init_logger, timeit
from src.common.utils import load_funds


@click.command()
@click.option('-c', '--config_file', help="Directory of the config file")
@click.option('-s', '--start', help="Start year of ETF data to download")
@click.option('-e', '--end', default=None, help="End year of ETF data to download")
def main(config_file, start, end):
    logger = init_logger(os.path.basename(__file__).split(".")[0])
    conf = Addict(yaml.safe_load(open(config_file, 'r')))

    # Load fund tickers from the universe file
    funds = load_funds(conf.get('univ'))
    num_funds = len(funds)
    logger.info("Number of funds to be processed: %s", num_funds)

    if end:
        years = list(range(int(start), int(end) + 1))
    else:
        years = [start]
    logger.info("Years of data to crawl: %s", years)

    for year in years:
        # Create output directory
        file_path = conf.get('output')
        output_dir = '/'.join(file_path.split('/')[:-1]).format(yyyy=year)
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        logger.info("Output directory created: %s", output_dir)

        # Crawl the data of the funds
        logger.info("Start to download historical fund data for %s...", year)
        start_time = time.time()
        for fund in funds:
            file_path_per_fund = file_path.format(yyyy=year, ticker=fund)
            download(fund, year, file_path_per_fund)
            logger.info("Data of %s written to %s", fund, file_path_per_fund)
        logger.info("Elapsed time: %s seconds",
                    round(time.time() - start_time, 6))
        logger.info(
            "-----------------------------------------------------------\n")


def download(ticker, year, file_path):
    current_year = datetime.today().year
    start_dt = str(year) + '-01-01'
    if year == current_year:
        end_dt = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    else:
        end_dt = str(year) + '-12-31'
    data = yf.download(
        ticker,
        start=start_dt,
        end=end_dt,
        progress=False
    ).reset_index()
    if data.shape[0] > 0:
        data.to_csv(file_path, index=False)


if __name__ == "__main__":
    main()
