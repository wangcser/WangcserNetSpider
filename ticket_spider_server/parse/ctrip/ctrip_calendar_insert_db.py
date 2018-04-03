import re
import sqlite3

from module.spider_log import spider_log
from module.time_stamp import current_time


def ctrip_calendar_insert_db(air_port, Sep_p_dict,):

    db_name = "ctrip_calendar_Seq_ticket.db"
    db_path = "E:/ticket_spider/database/" + db_name
    conn = sqlite3.connect(db_path)
    cu = conn.cursor()

    try:
        table_name = re.sub(r"-", '_', air_port)
        CREATE_DB = "CREATE TABLE " + table_name + "(crawl_time CHAR(50), " \
                    "Sep01 INTEGER, Sep02 INTEGER, Sep03 INTEGER, " \
                    "Sep04 INTEGER, Sep05 INTEGER, Sep06 INTEGER, " \
                    "Sep07 INTEGER, Sep08 INTEGER, Sep09 INTEGER, " \
                    "Sep10 INTEGER, Sep11 INTEGER, Sep12 INTEGER, " \
                    "Sep13 INTEGER, Sep14 INTEGER, Sep15 INTEGER, " \
                    "Sep16 INTEGER, Sep17 INTEGER, Sep18 INTEGER, " \
                    "Sep19 INTEGER, Sep20 INTEGER, Sep21 INTEGER, " \
                    "Sep22 INTEGER, Sep23 INTEGER, Sep24 INTEGER, " \
                    "Sep25 INTEGER, Sep26 INTEGER, Sep27 INTEGER, " \
                    "Sep28 INTEGER, Sep29 INTEGER, Sep30 INTEGER)"
        cu.execute(CREATE_DB)
        spider_log(air_port + ": db create,table name: " + table_name)
    except:
        #spider_log(air_port + ": db exist.")
        pass

    crawl_time = current_time()

    try:
        INSERT_DB = "insert into " + table_name + "(crawl_time, " \
                    "Sep01, Sep02, Sep03, Sep04, Sep05, Sep06, Sep07, Sep08, Sep09, Sep10, " \
                    "Sep11, Sep12, Sep13, Sep14, Sep15, Sep16, Sep17, Sep18, Sep19, Sep20, " \
                    "Sep21, Sep22, Sep23, Sep24, Sep25, Sep26, Sep27, Sep28, Sep29, Sep30) " \
                    "values(\'" + crawl_time \
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
                    + "\')"
        cu.execute(INSERT_DB)
        spider_log(air_port + ": data insert.")
    except:
        spider_log(air_port + ": data insert error.")

    cu.close()
    conn.commit()
    conn.close()
