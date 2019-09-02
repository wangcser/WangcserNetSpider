import time

from module.send_email import send_email
from module.spider_log import spider_log
from spider.start_spider import start_spider

'''
function: 用于服务器运行，设定每2个小时运行一次，每次爬取10条路线，每天爬取10次，爬取一周。
'''
if __name__ == '__main__':

    spider_log("ticket spider server mode start.")

    count = 1
    # 首次运行
    spider_log("running count: " + str(count))
    start_spider()
    spider_log("---")

    while(1):
        # 每隔 2h 运行一次
        time.sleep(5)
        start_spider()
        spider_log("---")
        count += 1
        spider_log("running count: " + str(count))

        if count == 3:
            break

    email_content = "ctrip price calendar data."

    db_path_1 = "E:/ticket_spider/database/ctrip_calendar_Seq_ticket.db"
    db_path_2 = "E:/ticket_spider/database/qunar_calendar_Seq_ticket.db"
    log_path = "E:/ticket_spider/log/ticket_calendar_log.txt"
    send_email(email_content, db_path_1,db_path_2, log_path)
