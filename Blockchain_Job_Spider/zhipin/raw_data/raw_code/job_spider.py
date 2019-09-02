import requests
import pandas as pd
import time


def job_spider(jid="1913e38066dd3c8e1Hd40t--FVE~", ka="search_list_1", i=0):
    # request info.
    job_url = "https://www.zhipin.com/job_detail/" + jid + ".html"

    headers = {
        'cache-control': "no-cache",
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/71.0.3578.80 Safari/537.36'
        }

    querystring = {"ka": ka}

    try:
        # request
        r = requests.request("GET", job_url, headers=headers, params=querystring)
        content = r.content.decode('utf-8')

        # raw data.
        file = "./raw_data/page/" + jid + ".html"
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        result = "suceed"
    except IOError:
        result = "failed"

    log = "job " + str(i) + " : " + jid + " crawl " + result
    print(log)


if __name__ == "__main__":

    file = "./raw_data/list/job_list.csv"
    df = pd.read_csv(file, encoding='utf-8', header=None)

    jid_list = df[0].values.tolist()
    ka_list = df[1].values.tolist()
    # print(jid_list)

    for i in range(0, len(jid_list)):
        job_spider(jid_list[i], ka_list[i], i)
        time.sleep(1)
