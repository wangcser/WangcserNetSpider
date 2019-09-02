from zhipin.zhipin_spider import job_spider, list_spider
from zhipin.zhipin_parser import job_parser, list_parser, to_csv
import pandas as pd
import time
import logging

if __name__ == "__main__":
    # TODO: finish this logging module.
    logging.basicConfig(level=logging.INFO,
                        # filename='../zhipin/zhipin_spider.log',
                        datefmt='%Y/%m/%d %H:%M:%S',
                        format='%(asctime)s %(levelname)s: '
                               '%(module)s %(message)s')

    # 1. crawl job list with list_spider.
    # 2. parser job list, store job id.
    crawl_page = 10
    for i in range(1, crawl_page+1):
        list_spider(page=i)
        list_parser(p=i)
        time.sleep(1)   # politely

    # 3. crawl job with job_spider
    file = "./raw_data/list/job_list.csv"
    df = pd.read_csv(file, encoding='utf-8', header=None)

    jid_list = df[0].values.tolist()
    ka_list = df[1].values.tolist()

    for i in range(0, len(jid_list)):
        job_spider(jid_list[i], ka_list[i], i)
        time.sleep(1)

    # 4. parser job.
    job_list = []
    for jid in jid_list:
        job_dict = job_parser(jid)
        job_list.append(job_dict)

    to_csv(job_list)


