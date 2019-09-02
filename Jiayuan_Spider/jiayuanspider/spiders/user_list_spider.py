import scrapy
import json
import re
from jiayuanspider.items import JiayuanListItem # data item
from jiayuanspider.jiayuan_log import spider_log # run status log
from jiayuanspider.jiayuan_cookie import get_cookie


class list_spider(scrapy.Spider):

    name = "user_list_spider"


    def start_requests(self):
        # defined start url
        url = "http://search.jiayuan.com/v2/search_v2.php"
        spider_log("user_list_spider start.")

        cookie_in_dict = get_cookie() # 账号好像出问题了
        headers = {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            'cache-control': "no-cache",
            'connection': "keep-alive",
            'host': "www.jiayuan.com",
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
        }

        # change params in this dict
        # t=148568&ft=off&f=select&mt=d
        params = {
            'f':"select",
            'jsversion':"v5",
            'listStyle':"bigPhoto",
            'p':"1",
            'sex':"m",
            'sn':"defualt",
            'stc':"27:1,1:99", # 最近注册
            'sv':"1"
        }

        #log url info.
        spider_log("crawl url: " + url)

        # crawl strategy.
        for page in range(1, 2):
            params['p'] = str(page)
            #yield scrapy.FormRequest(url=url, callback=self.parse, formdata=params)
            yield scrapy.FormRequest(url=url, headers=headers, callback=self.parse, formdata=params, cookies=cookie_in_dict)
            spider_log("request page" + params['p'] +", response yield.")

    def parse(self, response):

        # get raw reopnse data(in json), package it into item.

        re_list = re.findall(r"##jiayser##(.+?)##jiayser##", (response.body).decode('raw_unicode_escape')) # 这里的编码还未确定，目前可用
        js = json.loads(re_list[0])
        item = JiayuanListItem(user_list_item=js['userInfo'])
        spider_log("item yield.")
        yield item
