#coding:utf-8
import sqlite3
import re
import scrapy
from jiayuan_grade_spider.items import JiayuanGradeItem
from jiayuan_grade_spider.jiayuan_log import spider_log


class user_spider(scrapy.Spider):

    name = "user_grade_spider"

    item_uid = ""
    start_id = 30
    stop_id = 35
    url = "http://www.jiayuan.com/profile/reliable.php?uid="
    db_path = "E:/user_grade/user_grade.db"

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

        self.cookie_in_dict = {
            'SESSION_HASH': 'bb828fffe9ce8309b8d53a214aaf529832cbc7d3',
            'user_access': '1', 'save_jy_login_name': '18689966108',
            'stadate1': '132336188', 'myloc': '46%7C4601', 'myage': '27',
            'PROFILE': '133336188%3A%25E5%2586%25AC%25E8%25A5%25BF3%3Am%3Aimages1.jyimg.com%2Fw4%2Fglobal%2Fi%3A0%3A%3A1%3Azwzp_m.jpg%3A1%3A1%3A0%3A0',
            'mysex': 'm', 'myuid': '132336188', 'myincome': '20',
            'RAW_HASH': 'mfqSXK3yxme1iTxzh18v2gPRTU-NiYLoQaR3dd7IwDx6V10Wx7dxIErWm9yvdcW%2As3In9QjlrsRL3IawuUgyaCpmCaidZnB0sjcAUaYE-%2A29Qv0.',
            'COMMON_HASH': 'bfcb738df3f0f42114b6aa2ff88a7628',
            'sl_jumper': '%26cou%3D17%26omsg%3D0%26dia%3D0%26lst%3D2017-08-16',
            'last_login_time': '1502868020',
            'upt': 'WkDXGAoyAzbGhhtrvMJTSNl4dMku1RoD5W-xef4qskLzPYMWtCRHE0otg7xT0tBqePCYzMYhzvLo0c5ysbr7ver98rE.',
            'user_attr': '000000',
            'pclog': '%7B%22133336188%22%3A%221502868014820%7C1%7C0%22%7D',
            'IM_S': '%7B%22IM_CID%22%3A4758611%2C%22IM_SV%22%3A%22123.59.161.6%22%2C%22svc%22%3A%7B%22code%22%3A0%2C%22nps%22%3A0%2C%22unread_count%22%3A%225%22%2C%22ocu%22%3A0%2C%22ppc%22%3A0%2C%22jpc%22%3A0%2C%22regt%22%3A%221424485435%22%2C%22using%22%3A%222%2C%22%2C%22user_type%22%3A%220%22%2C%22uid%22%3A133336188%7D%7D',
            'IM_CS': '0', 'IM_ID': '1', 'IM_TK': '1502868015068',
            'IM_M': '%5B%7B%22cmd%22%3A57%2C%22data%22%3A%22123.59.161.6%22%7D%5D',
            'IM_CON': '%7B%22IM_TM%22%3A1502868015068%2C%22IM_SN%22%3A1%7D',
            'PHPSESSID': '619cfbe37c292c1c64db085d94570dd7'
        }

        conn = sqlite3.connect("E:/user_grade/user_list/jiayuan_f_user_list.db")
        cu = conn.cursor()
        SELECT_DB = "select uid from f_user_table where id=" + str(self.start_id)
        cu.execute(SELECT_DB)
        uid_obj = str(cu.fetchall())
        uid = (re.findall(u"[0-9]+", uid_obj))[0]
        self.item_uid = uid # 将uid持久化
        user_url = self.url + uid
        yield scrapy.Request(method='GET', url=user_url, callback=self.parse, headers=self.headers, cookies=self.cookie_in_dict)

    def parse(self, response):
        r = (response.body).decode('utf-8')
        item = JiayuanGradeItem(user_id_item=self.item_uid, user_grade_item=str(r))
        yield item

        if self.start_id < self.stop_id:
            self.start_id += 1
            conn = sqlite3.connect("E:/user_grade/user_list/jiayuan_f_user_list.db")
            cu = conn.cursor()
            SELECT_DB = "select uid from f_user_table where id=" + str(self.start_id)
            cu.execute(SELECT_DB)
            uid_obj = str(cu.fetchall())
            uid = (re.findall(u"[0-9]+", uid_obj))[0]  # 需要的uid信息
            self.item_uid = uid  # 将uid持久化
            user_url = self.url + uid
            yield scrapy.Request(method='GET', url=user_url, callback=self.parse, headers=self.headers, cookies=self.cookie_in_dict)
        else:
            spider_log("all task finished.")
            pass
