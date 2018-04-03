'''
module name: jiayuan_log
module func: 记录系统运行情况
             系统的日志模块不好用，所以设计了新的日志模块
'''
from module.time_stamp import current_time


def spider_log(log_data):
    # log spider info into txt.
    time_stamp = current_time('sec')
    f = open("E:/ticket_spider/log/ticket_calendar_log.txt", "a")

    write_str = "spider (" + time_stamp + " ): " + log_data + "\n"
    f.write(write_str)
    print(write_str)
    f.close()
    pass


