import requests
import time
import os
import logging


def list_spider(p):
    # request info.

    key_word = "区块链"
    page = str(p)
    ka = "page-" + page

    list_url = "https://www.zhipin.com/c100010000/"

    headers = {
        'cache-control': "no-cache",
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/71.0.3578.80 Safari/537.36'
    }

    querystring = {
        "query": key_word,
        "page": page,
        "ka": ka
    }

    # request
    try:
        r = requests.request("GET", list_url, headers=headers,
                             params=querystring)
        content = r.content.decode('utf-8')

        # raw data.
        file = "./raw_data/list/" + page + ".html"
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

        result = " succeed."
    except IOError as e:
        result = " failed" + e

    log = "request list page " + page + result
    print(log)


if __name__ == "__main__":

    for i in range(1, 11):
        list_spider(p=i)
        time.sleep(1)
