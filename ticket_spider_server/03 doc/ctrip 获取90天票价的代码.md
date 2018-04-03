# Ctrip crawl 90 days code

# ctrip_calendar_spider.py

```python
'''
module name: ctrip_spider.py
func: 综合考虑各种爬虫方案后选择浏览器的方案爬取数据
'''

import time
from selenium import webdriver
from parse.ctrip.ctrip_parse import ctrip_calendar_parse_data


def ctrip_calendar_spider(air_port_list):

    print("ctrip_spider start.")

    driver = webdriver.Firefox()
    '''
    --- url content ---
    http://flights.ctrip.com/international/chengdu-taipei-ctu-tpe?2017-09-01&y_s
    --- * ---
    url_add: http://flights.ctrip.com/
    国际航班: international/
    起降机场: 单程 chengdu-taipei-ctu-tpe / 往返 round-chengdu-taipei-ctu-tpe
    --- url args ---
    出发时间: 2017-08-10 如果不带时间则返回今天的航班
    仓位: 经济舱 y_s / 公务舱&头等舱 c_f / 公务舱 c / 头等舱 f
    '''
    main_url = "http://flights.ctrip.com"
    subs = "/"
    air_line = "international"
    air_round = "round-"
    #air_port = "chengdu-taipei-ctu-tpe"
    depart_time = "2017-09-01"
    arrive_time = "2017-10-01"
    position = "y_s"

    for air_port_item in air_port_list:

        print("crawl air_line: " + air_port_item)

        month_page = []

        search_url = main_url + "/" + air_line + "/" + air_port_item + "?" + position
        driver.get(search_url)
        # 点击低价日历，获取当月（8月）价格情况
        driver.find_element_by_xpath(".//*[@id='calendar_tab']/div[4]/a").click()
        time.sleep(1)
        month_page.append(driver.page_source)
        # 点击向下翻页，获取下一月（9月）的情况
        driver.find_element_by_class_name("bottom_arrow").click()
        time.sleep(1)
        month_page.append(driver.page_source)
        # 点击向下翻页，获取下一月（10月）的情况
        driver.find_element_by_class_name("bottom_arrow").click()
        time.sleep(1)
        month_page.append(driver.page_source)
        # 写入文件，准备解析, 这里使用了文件进行解析，也可以不用文件中转。
        for seq in range(3):
            file_name = "ctrip_" + air_port_item  + "_" + str(seq) + ".txt"
            file_path = "E:/02 Python/01 crawl/ticketspider/01 raw_data/" + file_name
            # 打开文件的时候就要指定编码
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(month_page[seq])
                f.close()
            print(air_port_item + ": page_" + str(seq) + " download.")
            time.sleep(1)
        ctrip_calendar_parse_data(air_port_item)
        time.sleep(1)

    print("ctrip_spider: data all insert.")
    driver.quit()
```

# ctrip_calendar_parse_data.py

```python
from bs4 import BeautifulSoup
import re
import time
import calendar
from parse.ctrip.ctrip_insert_db import ctrip_insert_db


def ctrip_calendar_parse_data(air_port):

    # seq: 0_2 0 Aug, 1 Sep, 2 Oct
    aug_p_dict = {}
    sep_p_dict = {}
    oct_p_dict = {}
    p_list = [aug_p_dict, sep_p_dict, oct_p_dict]

    for seq in range(0, 3):
        # 读取数据
        file_name = "ctrip_" + air_port + "_" + str(seq) + ".txt"
        file_path = "E:/02 Python/01 crawl/ticketspider/01 raw_data/" + file_name
        with open(file_path, 'r', encoding='utf-8') as f:
            page = f.read()
            f.close()
        # 解析数据
        soup = BeautifulSoup(page, 'lxml')
        price_list = soup.table.tbody.find_all(class_="price")
        price_num = len(price_list) # 这个参数可以取消

        # 初始化dict
        t = time.localtime()
        month_range = calendar.monthrange(t.tm_year, t.tm_mon + seq)
        month_len = month_range[1]

        for iter in range(1, month_len + 1):
            p_list[seq][str(iter)] = '0'

         # 获取当前的日期
        current_day = t.tm_mday
        for iter in range(0, price_num):
            ticket_price = re.findall(r"</dfn>(.+?)</div>", str(price_list[iter]))
            if seq == 0: # 如果是当前月份，需要去掉过去的日期
                date = iter + current_day
                if date == 31: # 这里是协程的BUG，日历中没有给出31号的票价
                    break
            else:
                date = iter + 1
            p_list[seq][str(date)] = ticket_price[0]

    ctrip_insert_db(air_port, p_list[0], p_list[1], p_list[2])
```

# ctrip_calendar_insert_db.py

```python
import re
import sqlite3
from module.time_stamp import current_time


def ctrip_insert_db(air_port, Aug_p_dict, Sep_p_dict, Oct_p_dict):

    db_name = "ctrip_ticekt_calendar.db"
    db_path = "E:/02 Python/01 crawl/ticketspider/02 database/" + db_name
    conn = sqlite3.connect(db_path)
    cu = conn.cursor()

    try:
        table_name = re.sub(r"-", '_', air_port)
        CREATE_DB = "CREATE TABLE " + table_name + "(crawl_time CHAR(50), " \
                    "Aug01 INTEGER, Aug02 INTEGER, Aug03 INTEGER, " \
                    "Aug04 INTEGER, Aug05 INTEGER, Aug06 INTEGER, " \
                    "Aug07 INTEGER, Aug08 INTEGER, Aug09 INTEGER, " \
                    "Aug10 INTEGER, Aug11 INTEGER, Aug12 INTEGER, " \
                    "Aug13 INTEGER, Aug14 INTEGER, Aug15 INTEGER, " \
                    "Aug16 INTEGER, Aug17 INTEGER, Aug18 INTEGER, " \
                    "Aug19 INTEGER, Aug20 INTEGER, Aug21 INTEGER, " \
                    "Aug22 INTEGER, Aug23 INTEGER, Aug24 INTEGER, " \
                    "Aug25 INTEGER, Aug26 INTEGER, Aug27 INTEGER, " \
                    "Aug28 INTEGER, Aug29 INTEGER, Aug30 INTEGER, " \
                    "Aug31 INTEGER, " \
                    "Sep01 INTEGER, Sep02 INTEGER, Sep03 INTEGER, " \
                    "Sep04 INTEGER, Sep05 INTEGER, Sep06 INTEGER, " \
                    "Sep07 INTEGER, Sep08 INTEGER, Sep09 INTEGER, " \
                    "Sep10 INTEGER, Sep11 INTEGER, Sep12 INTEGER, " \
                    "Sep13 INTEGER, Sep14 INTEGER, Sep15 INTEGER, " \
                    "Sep16 INTEGER, Sep17 INTEGER, Sep18 INTEGER, " \
                    "Sep19 INTEGER, Sep20 INTEGER, Sep21 INTEGER, " \
                    "Sep22 INTEGER, Sep23 INTEGER, Sep24 INTEGER, " \
                    "Sep25 INTEGER, Sep26 INTEGER, Sep27 INTEGER, " \
                    "Sep28 INTEGER, Sep29 INTEGER, Sep30 INTEGER, " \
                    "" \
                    "Oct01 INTEGER, Oct02 INTEGER, Oct03 INTEGER, " \
                    "Oct04 INTEGER, Oct05 INTEGER, Oct06 INTEGER, " \
                    "Oct07 INTEGER, Oct08 INTEGER, Oct09 INTEGER, " \
                    "Oct10 INTEGER, Oct11 INTEGER, Oct12 INTEGER, " \
                    "Oct13 INTEGER, Oct14 INTEGER, Oct15 INTEGER, " \
                    "Oct16 INTEGER, Oct17 INTEGER, Oct18 INTEGER, " \
                    "Oct19 INTEGER, Oct20 INTEGER, Oct21 INTEGER, " \
                    "Oct22 INTEGER, Oct23 INTEGER, Oct24 INTEGER, " \
                    "Oct25 INTEGER, Oct26 INTEGER, Oct27 INTEGER, " \
                    "Oct28 INTEGER, Oct29 INTEGER, Oct30 INTEGER, " \
                    "Oct31 INTEGER)"
        cu.execute(CREATE_DB)
        print(air_port + ": db create,table name: " + table_name)
    except:
        print(air_port + ": db exist.")

    crawl_time = current_time()

    try:
        INSERT_DB = "insert into " + table_name + "(crawl_time, " \
                    "Aug01, Aug02, Aug03, Aug04, Aug05, Aug06, Aug07, Aug08, Aug09, Aug10, " \
                    "Aug11, Aug12, Aug13, Aug14, Aug15, Aug16, Aug17, Aug18, Aug19, Aug20, " \
                    "Aug21, Aug22, Aug23, Aug24, Aug25, Aug26, Aug27, Aug28, Aug29, Aug30, " \
                    "Aug31, " \
                    "Sep01, Sep02, Sep03, Sep04, Sep05, Sep06, Sep07, Sep08, Sep09, Sep10, " \
                    "Sep11, Sep12, Sep13, Sep14, Sep15, Sep16, Sep17, Sep18, Sep19, Sep20, " \
                    "Sep21, Sep22, Sep23, Sep24, Sep25, Sep26, Sep27, Sep28, Sep29, Sep30, " \
                    "" \
                    "Oct01, Oct02, Oct03, Oct04, Oct05, Oct06, Oct07, Oct08, Oct09, Oct10, " \
                    "Oct11, Oct12, Oct13, Oct14, Oct15, Oct16, Oct17, Oct18, Oct19, Oct20, " \
                    "Oct21, Oct22, Oct23, Oct24, Oct25, Oct26, Oct27, Oct28, Oct29, Oct30, " \
                    "Oct31) values(\'" + crawl_time \
                    + "\',\'" + Aug_p_dict['1'] + "\',\'" + Aug_p_dict['2'] \
                    + "\',\'" + Aug_p_dict['3'] + "\',\'" + Aug_p_dict['4'] \
                    + "\',\'" + Aug_p_dict['5'] + "\',\'" + Aug_p_dict['6'] \
                    + "\',\'" + Aug_p_dict['7'] + "\',\'" + Aug_p_dict['8'] \
                    + "\',\'" + Aug_p_dict['9'] + "\',\'" + Aug_p_dict['10'] \
                    + "\',\'" + Aug_p_dict['11'] + "\',\'" + Aug_p_dict['12'] \
                    + "\',\'" + Aug_p_dict['13'] + "\',\'" + Aug_p_dict['14'] \
                    + "\',\'" + Aug_p_dict['15'] + "\',\'" + Aug_p_dict['16'] \
                    + "\',\'" + Aug_p_dict['17'] + "\',\'" + Aug_p_dict['18'] \
                    + "\',\'" + Aug_p_dict['19'] + "\',\'" + Aug_p_dict['20'] \
                    + "\',\'" + Aug_p_dict['21'] + "\',\'" + Aug_p_dict['22'] \
                    + "\',\'" + Aug_p_dict['23'] + "\',\'" + Aug_p_dict['24'] \
                    + "\',\'" + Aug_p_dict['25'] + "\',\'" + Aug_p_dict['26'] \
                    + "\',\'" + Aug_p_dict['27'] + "\',\'" + Aug_p_dict['28'] \
                    + "\',\'" + Aug_p_dict['29'] + "\',\'" + Aug_p_dict['30'] \
                    + "\',\'" + Aug_p_dict['31'] \
                    + "\',\'" + Sep_p_dict['1'] + "\',\'" + Sep_p_dict['2'] \
                    + "\',\'" + Sep_p_dict['3'] + "\',\'" + Sep_p_dict['4'] \
                    + "\',\'" + Sep_p_dict['5'] + "\',\'" + Sep_p_dict['6'] \
                    + "\',\'" + Sep_p_dict['7'] + "\',\'" + Sep_p_dict['8'] \
                    + "\',\'" + Sep_p_dict['9'] + "\',\'" + Sep_p_dict['10'] \
                    + "\',\'" + Sep_p_dict['11'] + "\',\'" + Sep_p_dict['12'] \
                    + "\',\'" + Sep_p_dict['13'] + "\',\'" + Sep_p_dict['14'] \
                    + "\',\'" + Sep_p_dict['15'] + "\',\'" + Sep_p_dict['16'] \
                    + "\',\'" + Sep_p_dict['17'] + "\',\'" + Sep_p_dict['18'] \
                    + "\',\'" + Sep_p_dict['19'] + "\',\'" + Sep_p_dict['20'] \
                    + "\',\'" + Sep_p_dict['21'] + "\',\'" + Sep_p_dict['22'] \
                    + "\',\'" + Sep_p_dict['23'] + "\',\'" + Sep_p_dict['24'] \
                    + "\',\'" + Sep_p_dict['25'] + "\',\'" + Sep_p_dict['26'] \
                    + "\',\'" + Sep_p_dict['27'] + "\',\'" + Sep_p_dict['28'] \
                    + "\',\'" + Sep_p_dict['29'] + "\',\'" + Sep_p_dict['30'] \
                    \
                    + "\',\'" + Oct_p_dict['1'] + "\',\'" + Oct_p_dict['2'] \
                    + "\',\'" + Oct_p_dict['3'] + "\',\'" + Oct_p_dict['4'] \
                    + "\',\'" + Oct_p_dict['5'] + "\',\'" + Oct_p_dict['6'] \
                    + "\',\'" + Oct_p_dict['7'] + "\',\'" + Oct_p_dict['8'] \
                    + "\',\'" + Oct_p_dict['9'] + "\',\'" + Oct_p_dict['10'] \
                    + "\',\'" + Oct_p_dict['11'] + "\',\'" + Oct_p_dict['12'] \
                    + "\',\'" + Oct_p_dict['13'] + "\',\'" + Oct_p_dict['14'] \
                    + "\',\'" + Oct_p_dict['15'] + "\',\'" + Oct_p_dict['16'] \
                    + "\',\'" + Oct_p_dict['17'] + "\',\'" + Oct_p_dict['18'] \
                    + "\',\'" + Oct_p_dict['19'] + "\',\'" + Oct_p_dict['20'] \
                    + "\',\'" + Oct_p_dict['21'] + "\',\'" + Oct_p_dict['22'] \
                    + "\',\'" + Oct_p_dict['23'] + "\',\'" + Oct_p_dict['24'] \
                    + "\',\'" + Oct_p_dict['25'] + "\',\'" + Oct_p_dict['26'] \
                    + "\',\'" + Oct_p_dict['27'] + "\',\'" + Oct_p_dict['28'] \
                    + "\',\'" + Oct_p_dict['29'] + "\',\'" + Oct_p_dict['30'] \
                    + "\',\'" + Oct_p_dict['31'] + "\')"
        cu.execute(INSERT_DB)
        print(air_port + ": data insert.")
    except:
        print(air_port + ": data insert error.")

    cu.close()
    conn.commit()
    conn.close()

```