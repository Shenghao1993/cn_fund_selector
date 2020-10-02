import os
import csv
import argparse
import logging
import logging.config
import yaml
import requests
from addict import Dict as Addict


class FundUnivWorker:
    def __init__(self, url, output_fp):
        """Initialization
        """
        self.url = url
        self.output_fp = output_fp
    
    def _crawl(self):
        rsp = requests.get(url=self.url)
        results = rsp.text.split('],[')
        logging.info("%s funds found from the source website.", len(results))
        funds = []
        for result in results:
            quote_pos = result.index('"')
            fund_info = result[quote_pos:]
            fund_info = fund_info.replace('[', '')
            fund_info = fund_info.replace(']', '')
            fund_info = fund_info.replace('"', '')
            fund_info = fund_info.replace(';', '')
            funds.append(fund_info.split(','))
        return funds    

    def _output(self, funds):
        # Remove any exisitng output file
        if os.path.exists(self.output_fp):
            os.remove(self.output_fp)

        counter = 0
        with open(self.output_fp, 'a') as f:
            write = csv.writer(f)
            write.writerow(["基金代码", "基金简拼", "基金名称", "基金类型", "基金全拼"])
            for fund in funds:
                write.writerow(fund)
                if counter > 0 and counter % 1000 == 0:
                    logging.info("%s funds processed...", counter)
                counter += 1
    
    def run(self):
        fund_list = self._crawl()
        self._output(fund_list)


def main(config_file):
    conf = Addict(yaml.safe_load(open(config_file, 'r')))
    if conf.get("logging") is not None:
        logging.config.dictConfig(conf["logging"])
    else:
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s - %(levelname)s - %(message)s")
    fund_univ_url = conf.get("source").get("univ_url")
    fund_univ_file = conf.get("output").get("fund_univ")
    logging.info("Acquire fund data from %s", fund_univ_url)
    fund_univ_worker = FundUnivWorker(fund_univ_url, fund_univ_file)
    fund_univ_worker.run()
    logging.info("List of available funds written to %s", fund_univ_file)


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