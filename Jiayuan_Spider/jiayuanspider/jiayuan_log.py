'''
module name: jiayuan_log
module func: 记录系统运行情况
             系统的日志模块不好用，所以设计了新的日志模块
'''

import time

from jiayuanspider.jiayuan_time_stamp import current_time


def spider_log(log_data):
    # log spider info into txt.
    time_stamp = current_time('sec')
    f = open("E:/02 Python/01 crawl/jiayuanspider/04 user_data/jiayuan_user_data_log.txt", "a")

    f.write("spider (" + time_stamp + " ): " + log_data + "\n")
    f.close()
    pass


