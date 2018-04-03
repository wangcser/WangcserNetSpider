from bs4 import BeautifulSoup
import re

from module.spider_log import spider_log
from parse.ctrip.ctrip_calendar_insert_db import ctrip_calendar_insert_db


def ctrip_calendar_parse_data(air_port, file_path):
    p_dict = {}

    # 读取数据
    with open(file_path, 'r', encoding='utf-8') as f:
        page = f.read()
        f.close()

    # 解析数据
    soup = BeautifulSoup(page, 'lxml')
    try:
        price_list = soup.table.tbody.find_all(class_="price")
        price_num = len(price_list) # 这个参数可以取消

        for iter in range(0, price_num):
            ticket_price = re.findall(r"</dfn>(.+?)</div>", str(price_list[iter]))
            date = iter + 1
            p_dict[str(date)] = ticket_price[0]

        ctrip_calendar_insert_db(air_port, p_dict)
    except:
        spider_log("price_list not find.")