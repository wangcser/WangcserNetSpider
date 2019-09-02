import re
import sqlite3
from jiayuanspider.jiayuan_time_stamp import current_time
from jiayuanspider.jiayuan_log import spider_log


def list_process(list_raw_data, db_path):


    time_stamp = current_time('file_name')
    # 能否将数据库操作移动到openspider中
    # db_path = "E:/02 Python/01 crawl/jiayuanspider/database/" + time_stamp + " jiayuan_user_list.db"
    conn = sqlite3.connect(db_path)
    cu = conn.cursor()

    try:
        CREATE_DB = "CREATE TABLE m_user_table(id INTEGER PRIMARY KEY AUTOINCREMENT, uid TEXT UNIQUE, nickname CHAR(50)," \
                    " age INTEGER, height INTEGER, education CHAR(50), work_location CHAR(50), image CHAR(100))"
        cu.execute(CREATE_DB)
        spider_log("database created, table name: m_user_table.")
    except:
        spider_log("database existed.")

    user_list = list_raw_data
    #spider_log("page in item was parsed, page_first_uid is: " + str(user_list[0]['realUid']))

    for user in user_list:
        try:
            INSERT_DB = "insert into m_user_table(uid, nickname, age, height, education, work_location, image) " \
                        "values(\'" + str(user['realUid']) + "\',\'" + user[
                            'nickname'] + "\', \'" + \
                        str(user['age']) + "\', \'" + str(
                user['height']) + "\', \'" + str(user['education']) + \
                        "\', \'" + str(user['work_location']) + "\', \'" + str(
                user['image']) + "\')"
            cu.execute(INSERT_DB)
            spider_log("insert uid: " + str(user['realUid']))
        except:
            spider_log("insert error. uid: " + str(user['realUid']))

    cu.close()
    conn.commit()  # 插入完毕后一并提交保存
    conn.close()