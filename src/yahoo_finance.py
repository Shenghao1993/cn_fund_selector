import click
import logging
import logging.config
import yaml
import time
import yfinance as yf
from addict import Dict as Addict
from pathlib import Path
from datetime import datetime, timedelta


@click.command()
@click.option('--config_file', help="Directory of the config file")
@click.option('--year', help="Year of ETF data to download")
def main(config_file, year):
    conf = Addict(yaml.safe_load(open(config_file, 'r')))
    if conf.get("logging") is not None:
        logfile = conf["logging"]["handlers"]["logfile"]["filename"]
        conf["logging"]["handlers"]["logfile"]["filename"] = \
            datetime.now().strftime(logfile)
        logging.config.dictConfig(conf["logging"])
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    # Load fund tickers from the universe file
    funds = load_funds(conf.get('univ'))
    num_funds = len(funds)
    logging.info("Number of funds to be processed: %s", num_funds)

    # Create output directory
    file_path = conf.get('output')
    output_dir = '/'.join(file_path.split('/')[:-1]).format(yyyy=year)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    logging.info("Output directory created: %s", output_dir)
    logging.info("Start to download historical fund data ...")
    start_time = time.time()
    for fund in funds:
        file_path_per_fund = file_path.format(yyyy=year, ticker=fund)
        download(fund, year, file_path_per_fund)
        logging.info("Data of %s written to %s", fund, file_path_per_fund)
    logging.info("Elapsed time: %s seconds",
                 round(time.time() - start_time, 6))


def load_funds(univ_file):
    with open(univ_file, 'r') as f:
        funds = [ticker.replace('\n', '') for ticker in f.readlines()]
    return funds


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
    data.to_csv(file_path, index=False)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception("Unhandled error during processing")
        raise
