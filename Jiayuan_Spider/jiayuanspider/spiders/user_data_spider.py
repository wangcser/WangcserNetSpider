#coding:utf-8
import sqlite3
import re
# import time
import scrapy
from jiayuanspider.jiayuan_cookie import get_cookie
from jiayuanspider.items import JiayuanUserItem
from jiayuanspider.jiayuan_log import spider_log
# from scrapy import log


class user_spider(scrapy.Spider):
    # defined your spider and crawl url.

    name = "user_data_spider"

    item_uid = "123456789" # 该字段用于本地存储,同时用于标记包裹,由于scrapy异步处理的问题，目前部门实现对所有包裹的准确标记。哪呢改变策略，加黑用户就不下载原始数据了。
    start_id = 1586
    stop_id = 2267
    url = "http://www.jiayuan.com"
    headers = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        'cache-control': "no-cache",
        'connection': "keep-alive",
        'host': "www.jiayuan.com",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
        'postman-token': "0a075645-3dbf-a88c-d18f-5c2d6888d79b"
    }

    cookie_in_dict = {}


    def start_requests(self):
        # defined start url

        '''
        # 获取头文件信息,原来误以为cookie卸载headers中也行，结果发现这是不能被解析的，还是要单独传
        # 该处cookie用于调试
        self.cookie_in_dict = {
            'IM_TK': "1500986331371",
            'IM_S': "%7B%22IM_CID%22%3A9391466%2C%22IM_SV%22%3A%22123.59.161.3%22%2C%22svc%22%3A%7B%22code%22%3A0%2C%22nps%22%3A0%2C%22unread_count%22%3A%2229%22%2C%22ocu%22%3A0%2C%22ppc%22%3A0%2C%22jpc%22%3A0%2C%22regt%22%3A%221499681417%22%2C%22using%22%3A%22%22%2C%22user_type%22%3A%2210%22%2C%22uid%22%3A165993232%7D%2C%22m%22%3A0%2C%22f%22%3A0%2C%22omc%22%3A0%7D",
            'IM_CON': "%7B%22IM_TM%22%3A1500986329619%2C%22IM_SN%22%3A3%7D",
            'IM_M': "%5B%7B%22cmd%22%3A54%2C%22data%22%3A%7B%22m%22%3A0%2C%22f%22%3A0%2C%22omc%22%3A0%7D%7D%5D",
            'IM_ID': "2",
            'IM_CS': "1",
            'photo_scyd_165993232': "yes",
            'COMMON_HASH': "231d35ca301bf724f4854c1ef2730fe2",
            'RAW_HASH': "WO97gqavZzrFbviVwm25ZXtuLzrtlTl5-sz2PiBEHtRWdsTargoC0sYXaJn7%2A-SgAo7pYeXxoBSWLlMM7ZILceorTifQs1NIfBWmG4IvdL9WDQI.",
            'mylevel': "2",
            'myincome': "30",
            'myuid': "164993232",
            'mysex': "m",
            'PROFILE': "165993232%3Ayanyan%3Am%3Aimages1.jyimg.com%2Fw4%2Fglobal%2Fi%3A0%3A%3A1%3Azwzp_m.jpg%3A1%3A1%3A325%3A10",
            'myage': "22",
            'myloc': "51%7C5101",
            'stadate1':"164993232",
            'pclog': "%7B%22165993232%22%3A%221500986312194%7C1%7C0%22%7D",
            'jy_safe_tips_new': "xingfu",
            'main_search:165993232': "%7C%7C%7C00",
            'PHPSESSID': "865e7667923a411553c55dfa1929f6ba",
            'user_attr': "000000",
            'upt': "FNeMiDK4kQ2iYHaGf32RXOgbXqn0-7x3rKjPwLaqwIoMxogsQHuFiaNs-3NCbCTf6dUWaopSZQBZry-3zSnFhbVt",
            'last_login_time': "1500986309",
            'sl_jumper': "%26cou%3D17%26omsg%3D0%26dia%3D0%26lst%3D2017-07-25",
            'save_jy_login_name': "18215568626",
            'user_access': "1",
            'SESSION_HASH': "84e216409c212f8856014332bf8d7da3e149445e"
        }
        '''

        self.cookie_in_dict = get_cookie()

        # 从数据库获取 uid，抛出请求
        #从数据库获取数据大小

        conn = sqlite3.connect( "E:/02 Python/01 crawl/jiayuanspider/04 user_data/jiayuan_m_user_list.db")
        cu = conn.cursor()
        SELECT_DB = "select uid from m_user_table where id=" + str(self.start_id)
        cu.execute(SELECT_DB)
        uid_obj = str(cu.fetchall())
        uid = (re.findall(u"[0-9]+", uid_obj))[0] # 需要的uid信息

        self.item_uid = uid # 将uid持久化

        user_url = self.url + "/" + uid
        # 抛出请求
        yield scrapy.Request(method='GET', url=user_url, callback=self.parse, headers=self.headers, cookies=self.cookie_in_dict)
        '''
        # 调试用
        id = 1
        SELECT_DB = "select uid from m_user_table where id=" + str(id)
        cu.execute(SELECT_DB)
        uid_obj = str(cu.fetchall())
        uid = (re.findall(u"[0-9]+", uid_obj))[0] # 需要的uid信息
        '''
        '''
        uid = "1659932"
        user_url = url + "/" + uid
        # 抛出请求
        self.item_uid = uid # 获取id，用于持久化
        yield scrapy.Request(url=user_url, callback=self.parse, headers=headers, cookies=cookie_in_dict)
        '''

    def parse(self, response):
        # 不应该在这里持久化
        r = (response.body).decode('utf-8')# 炸裂啊！！！，花了1个多小时！！！搞清楚encode和decode的区别，decode作用于byte流
        item = JiayuanUserItem(user_id_item=self.item_uid, user_data_item=str(r))
        yield item


        if self.start_id < self.stop_id:
            self.start_id += 1
            conn = sqlite3.connect("E:/02 Python/01 crawl/jiayuanspider/04 user_data/jiayuan_m_user_list.db")
            cu = conn.cursor()
            SELECT_DB = "select uid from m_user_table where id=" + str(
                self.start_id)
            cu.execute(SELECT_DB)
            uid_obj = str(cu.fetchall())
            uid = (re.findall(u"[0-9]+", uid_obj))[0]  # 需要的uid信息

            self.item_uid = uid  # 将uid持久化

            user_url = self.url + "/" + uid
            # 抛出请求
            yield scrapy.Request(method='GET', url=user_url, callback=self.parse, headers=self.headers, cookies=self.cookie_in_dict)

        else:
            spider_log("url all yield.")
            pass
