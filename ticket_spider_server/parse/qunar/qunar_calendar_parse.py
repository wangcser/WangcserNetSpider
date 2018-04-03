from bs4 import BeautifulSoup

from module.spider_log import spider_log
from parse.qunar.qunar_calendar_insert_db import qunar_calendar_insert_db


def qunar_calendar_parse_data(air_port, file_path):

    p_dict = {}
    # 读取数据
    with open(file_path, 'r', encoding='utf-8') as f:
        page = f.read()
        f.close()
    # 解析数据
    soup = BeautifulSoup(page, 'lxml')
    try:
        price_list = soup.find_all('span', class_="price")

        for iter in range(4,34):
            # 前四个数据为8月数据，文件中为“查看”，只解析9月的30个数据
            tmp = BeautifulSoup(str(price_list[iter]), 'lxml')
            date = iter - 3
            p_dict[str(date)] = tmp.body.span.span.text

        qunar_calendar_insert_db(air_port, p_dict)
    except:
        spider_log("price_list not find.")
'''
if __name__ == '__main__':
    air_port = "成都_洛杉矶"
    file_path = "E:/ticket_spider/raw_data/qunar_8.7.12_searchDepartureAirport=成都&searchArrivalAirport=洛杉矶.txt"
    qunar_calendar_parse_data(air_port, file_path)
'''