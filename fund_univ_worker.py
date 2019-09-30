import os
import csv
import yaml
import argparse
import logging
import logging.config
import requests
from bs4 import BeautifulSoup
from addict import Dict as Addict


class FundUnivWorker:
    def __init__(self, url, output_fp):
        """Initialization
        @param url
        @param output_fp

        """
        self.url = url
        self.output_fp = output_fp

    def _crawl(self):
        ret = requests.get(url=self.url)
        soup = BeautifulSoup(ret.text, features='html.parser')
        # fund_table
        div = soup.find(name='div', attrs={'class': 'box'})
        td_cells = div.find_all(name='td')
        fund_dict = {}
        for cell in td_cells:
            text = cell.get_text()
            if text:
                name = text[:-8]
                index = text[-7:-1]
                logging.info("name: %s  index: %s", name, index)
                if index not in fund_dict:
                    fund_dict[index] = name
        return fund_dict

    def _output(self, funds):
        # Remove any eixsitng output file
        if os.path.exists(self.output_fp):
            os.remove(self.output_fp)

        with open(self.output_fp, 'a') as f:
            write = csv.writer(f)
            for index, name in funds.items():
                write.writerow([index, name])

    def run(self):
        fund_list = self._crawl()
        self._output(fund_list)
        logging.info("List of available funds written to %s", self.output_fp)


def main(config_file):
    conf = Addict(yaml.safe_load(open(config_file, 'r')))
    if conf.get("logging") is not None:
        logging.config.dictConfig(conf["logging"])
    else:
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s - %(levelname)s - %(message)s")
    fund_univ_url = conf.get("url")
    fund_univ_file = conf.get("output").get("fund_univ")
    fund_univ_worker = FundUnivWorker(fund_univ_url, fund_univ_file)
    fund_univ_worker.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", required=True,
                        help="directory of the config file")
    args = parser.parse_args()
    try:
        main(args.config)
    except Exception:
        logging.exception("Unhandled error during processing")
        raise