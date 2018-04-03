# -*- coding: utf-8 -*-
import sqlite3
from jiayuan_grade_spider.jiayuan_email import send_email
from jiayuan_grade_spider.jiayuan_log import spider_log
from jiayuan_grade_spider.jiayuan_time_stamp import current_time
from jiayuan_grade_spider.jiayuan_user_process import user_process


class JiayuanspiderPipeline(object):

    def __init__(self):
        # 对处理过的item计数
        self.item_count = 1
        self.db_path = ""
        pass

    def open_spider(self,spider):
        self.db_path = "E:/user_grade/user_grade.db"
        spider_log("spider start.")

    def process_item(self, item, spider):


        tmp_id = item.get("user_id_item")
        tmp_data= item.get("user_grade_item")
        user_raw_data = str(tmp_data)
        user_id = str(tmp_id)
        user_process(user_id, user_raw_data, self.db_path)
    def close_spider(self,spider):


        # close database.
        # 获取爬取的统计信息,发送邮件
        conn = sqlite3.connect(self.db_path)
        cu = conn.cursor()
        SELECT_DB = "select uid from f_user_grade"
        cu.execute(SELECT_DB)
        data_list = cu.fetchall()
        count = len(data_list)

        email_content_dict = {
            'project_name': 'jiayuan_grade_spider',
            'crawler_name': spider.name,
            'list_name': 'f_user',
            'id_range': '1-10000',
            'date': current_time(),
            'crawl num': count
        }
        spider_log("crawl num: " + str(count))
        #send_email(str(email_content_dict), self.db_path)

        cu.close()
        conn.commit()  # 插入完毕后一并提交保存
        conn.close()
        spider_log("spider_closed.")