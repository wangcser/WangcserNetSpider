'''
module name: ctrip_spider.py
func: 综合考虑各种爬虫方案后选择浏览器的方案爬取数据
'''

import time
from selenium import webdriver

from module.spider_log import spider_log
from module.time_stamp import current_time
from parse.ctrip.ctrip_calendar_parse import ctrip_calendar_parse_data


def ctrip_calendar_spider(air_port_list):

    spider_log("ctrip_spider start, webdriver: Firefox")
    driver = webdriver.Firefox()

    time.sleep(1)

    main_url = "http://flights.ctrip.com"
    air_line = "international"
    depart_time = "2017-09-01"
    position = "y_s"

    for air_port_item in air_port_list:

        spider_log("crawl air_line: " + air_port_item)

        search_url = main_url + "/" + air_line + "/" + air_port_item + "?" + depart_time + "&" + position
        spider_log("crawl url: " + search_url)

        driver.get(search_url)
        time.sleep(1)
        # 点击低价日历，获取当月（9月）价格情况
        driver.find_element_by_xpath(".//*[@id='calendar_tab']/div[4]/a").click()
        time.sleep(1)
        month_page = driver.page_source

        # 写入文件，准备解析, 这里使用了文件进行解析，也可以不用文件中转。
        crawl_time = current_time('file_name_hour')
        # name_structure: site + time_stamp + line_info
        file_name = "ctrip_" + crawl_time +"_" + air_port_item + ".txt"
        file_path = "E:/ticket_spider/raw_data/" + file_name
        # 打开文件的时候就要指定编码
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(month_page)
            f.close()

        spider_log(air_port_item + ": download, file_path: " + file_path)
        time.sleep(1)

        ctrip_calendar_parse_data(air_port_item, file_path)
        time.sleep(1)

    driver.quit()






