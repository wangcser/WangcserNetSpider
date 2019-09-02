import requests
import logging

logger = logging.getLogger(__name__)

def job_spider(jid, ka, i):
    """

    :param jid: "1913e38066dd3c8e1Hd40t--FVE~"
    :param ka: "search_list_1"
    :param i: 0, i is index
    :return:
    """
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
    except IOError as e:
        result = e

    log = "job " + str(i) + " : " + jid + " crawl " + result
    logger.info(log)


def list_spider(page, key_word="区块链"):
    """
    :param page: page.
    :param key_word: search key word.
    :return:
    """
    # request info.
    ka = "page-" + str(page)
    list_url = "https://www.zhipin.com/c100010000/"
    headers = {
        'cache-control': "no-cache",
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/71.0.3578.80 Safari/537.36'
    }
    querystring = {
        "query": key_word,
        "page": str(page),
        "ka": ka
    }

    # request
    try:
        r = requests.request("GET", list_url, headers=headers,
                             params=querystring)
        content = r.content.decode('utf-8')
        # raw data.
        file = "./raw_data/list/" + str(page) + ".html"
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

        result = " succeed."
    except IOError as e:
        result = e

    log = "request list page " + str(page) + result
    logger.info(log)

