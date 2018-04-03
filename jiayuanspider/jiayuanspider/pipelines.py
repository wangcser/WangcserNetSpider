# -*- coding: utf-8 -*-
import os
import sqlite3
from jiayuanspider.jiayuan_list_process import list_process
from jiayuanspider.jiayuan_log import spider_log
from jiayuanspider.jiayuan_user_process import user_process
from jiayuanspider.jiayuan_time_stamp import current_time
from jiayuanspider.jiayuan_email import send_email


class JiayuanspiderPipeline(object):

    def __init__(self):
        # 对处理过的item计数
        self.item_count = 1
        self.db_path = ""
        pass

    def open_spider(self,spider):

        time_stamp = current_time('file_name')

        if spider.name == "user_list_spider":
            spider_log("user_list_spider started.")
            #self.db_path = "E:/02 Python/01 crawl/jiayuanspider/database/" + time_stamp + " jiayuan_user_list.db"
            # 调试用
            #self.db_path = "E:/02 Python/01 crawl/jiayuanspider/database/jiayuan_m_user_list.db"

        elif spider.name == "user_data_spider":
            spider_log("user_data_spider started.")
            #self.db_path = "E:/02 Python/01 crawl/jiayuanspider/user_data/" + time_stamp + " jiayuan_user_data.db"
            self.db_path = "E:/02 Python/01 crawl/jiayuanspider/04 user_data/jiayuan_m_user_data.db"

        else:
            pass

    def process_item(self, item, spider):
        if spider.name == "user_list_spider":
            spider_log("user_list_spider item " + str(self.item_count) + " get.")
            list_raw_data = item.get("user_list_item")
            list_process(list_raw_data, self.db_path)
            self.item_count =+ 1

        elif spider.name == "user_data_spider":
            tmp_id = item.get("user_id_item")
            tmp_data= item.get("user_data_item")
            user_raw_data = str(tmp_data)
            user_id = str(tmp_id)
            user_process(user_id, user_raw_data, self.db_path)

        else:
            pass

    def close_spider(self,spider):

        # close database.
        # 获取爬取的统计信息,发送邮件
        conn = sqlite3.connect(self.db_path)
        cu = conn.cursor()
        SELECT_DB = "select uid from m_user_table"
        cu.execute(SELECT_DB)
        data_list = cu.fetchall()
        count = len(data_list)
        spider_log("user_data_spider crawl user count : " + str(count))

        # 输出不同的邮件内容
        if spider.name == "user_list_spider":
            '''
            email_content_dict = {
                'project_name': 'jiayuanspider',
                'crawler_name': spider.name,
                'list_name': 'm_user',
                'crawl num': count
            }
            '''
            pass
        elif spider.name == "user_data_spider":
            email_content_dict = {
                'project_name': 'jiayuanspider',
                'crawler_name': spider.name,
                'list_name': 'm_user',
                'id_range': '1-5000',
                'date': '8.8',
                'crawl num': count
            }
        else:
            pass


        cu.close()
        conn.commit()  # 插入完毕后一并提交保存
        conn.close()

        send_email(str(email_content_dict), self.db_path)

        spider_log(" ")
        spider_log("database closed.")
        spider_log("spider stopped.")
		
		# 执行完毕后自动关机
		#os.system('shutdown -s -t 60')