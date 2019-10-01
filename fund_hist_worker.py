# https://blog.csdn.net/yys1164922014/article/details/100098533

import argparse
import pandas as pd
import requests
import re
import yaml
import logging
import logging.config
from lxml import etree
from addict import Dict as Addict


found_code='111111'
page_number=''
#start_date='2010-08-20'
end_date=''

url='http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz'\
    '&code=110022&page=10&sdate=2019-01-01&edate=2019-02-13&per=1'

def get_found_info_per1_list(url_found):
    ########本函数获取单只基金一页一天的数据，per=1，返回list
    ######定义空列表存储基金信息
    list_info=[]
    ######re.findall,xpath匹配信息
    response=requests.get(url_found)
    text=response.text
    text_html=re.findall('content:"(.*?)",records:',text)[0]
#    print(text_html)
    html = etree.HTML(text_html)
#    print(html)
    
    html_data = html.xpath('//tr/td')
    logging.info('---------------')

    for info in html_data:
        list_info.append(info.text)
        
    logging.info(html_data,'\n','==='*20)
    logging.info(list_info)
    return (list_info)


class FundHistWorker:
    def __init__(self, index, name, url):
        """Initialization
        @param index
        @param url
        @param output_fp

        """
        self.index = index
        self.name = name
        self.url = url
        #self.output_fp = output_fp

    def _get_start_date(self):
        """Get the start date of a fund
        """

        search_url = self.url.format(index=self.index)
        rsp = requests.get(search_url)
        text = rsp.content.decode('utf-8')
        start_date = re.findall('<td><span class="letterSpace01">成 立 日</span>：(.*?)</td>', text)
        
        # Mark the fund without an effective start date
        if start_date == []:
            start_date=['无记录']
        
        return (start_date[0])

    def _crawl(self):
        rsp = requests.get(url=self.url)
        soup = BeautifulSoup(rsp.text, features='html.parser')

    def _output(self):
        pass
    
    def run(self):
        # https://blog.csdn.net/Urbanears/article/details/79204684
        start_date = self._get_start_date()
        logging.info(start_date)


def main(config_file):
    conf = Addict(yaml.safe_load(open(config_file, 'r')))
    if conf.get("logging") is not None:
        logging.config.dictConfig(conf["logging"])
    else:
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s - %(levelname)s - %(message)s")
    fund_home_url = conf.get("source").get("fund_home_url")
    fund_info_file = conf.get("output").get("fund_univ")
    funds_df = pd.read_csv(fund_info_file, dtype={'基金代码': str})
    for i in range(3):
        fund_id = funds_df.iloc[i]['基金代码']
        fund_name = funds_df.iloc[i]['基金名称']
        logging.info("Index: %s Name: %s", fund_id, fund_name)
        fund_hist_worker = FundHistWorker(fund_id, fund_name, fund_home_url)
        fund_hist_worker.run()


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