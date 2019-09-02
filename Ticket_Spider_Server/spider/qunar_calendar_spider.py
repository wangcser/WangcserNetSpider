'''
module name: qunar_spider.py
func: 综合考虑各种爬虫方案后选择浏览器的方案爬取数据
BUG: qunar使用PhantomJS初始的headers无法获取数据
'''

import time
import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from module.spider_log import spider_log
from module.time_stamp import current_time
from parse.qunar.qunar_calendar_parse import qunar_calendar_parse_data


def qunar_calendar_spider(air_port_list):

    spider_log("qunar_spider start, webdriver: Firefox")

    driver = webdriver.Firefox()

    time.sleep(1)

    main_url = "https://flight.qunar.com/site/oneway_list_inter.htm"
    depart_time = "searchDepartureTime=2017-09-01"
    passager_info = "adultNum=1&childNum=0"

    for air_port_item in air_port_list:

        spider_log("crawl air_line: " + air_port_item)

        search_url = main_url + "?" + air_port_item + "?" + depart_time + "?" + passager_info
        spider_log("crawl url: " + search_url)

        driver.get(search_url)
        # 点击低价日历，获取当月（8月）价格情况
        driver.find_element_by_xpath(".//*[@id='dateBar']/div[2]/div").click()
        time.sleep(1)

        # 原来计划获取90天的情况，现在觉得把问题简化比较好,只获取9月的情况
        month_page = driver.page_source
        # 写入文件
        crawl_time = current_time('file_name_hour')
        # name_structure: site + time_stamp + line_info
        file_name = "qunar_" + crawl_time +"_" + air_port_item + ".txt"
        file_path = "E:/ticket_spider/raw_data/" + file_name
        # 打开文件的时候就要指定编码
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(month_page)
            f.close()

        spider_log(air_port_item + ": download, file_path: " + file_path)
        time.sleep(1)

        # 将port信息解析为易读的形式（方便建立数据库）
        location = re.findall(r'[\u4e00-\u9fa5]+', air_port_item)
        air_port = location[0] + "_" + location[1]

        qunar_calendar_parse_data(air_port, file_path)
        time.sleep(1)

    driver.quit()

'''
if __name__ == '__main__':
    qunar_air_port_list = [
        'searchDepartureAirport=成都&searchArrivalAirport=洛杉矶'
    ]

    qunar_calendar_spider(qunar_air_port_list)
'''





