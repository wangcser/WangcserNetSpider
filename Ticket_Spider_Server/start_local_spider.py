from module.send_email import send_log_email
from module.spider_log import spider_log
from spider.start_spider import start_spider

'''
function: 用于本地运行，设定每1个小时运行一次，每次爬取10条路线，每天爬取5次，爬取一周。
          从下午1点开始爬取，进行到下午5点。
'''
if __name__ == '__main__':

    spider_log("ticket spider local mode start.")

    try:
        start_spider()
        spider_log("---")
        email_content = "spider run success, ctrip price calendar log."
    except:
        email_content = "spider run error."

    log_path = "E:/ticket_spider/log/ticket_calendar_log.txt"
    #send_log_email(email_content, log_path)
