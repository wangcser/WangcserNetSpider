#coding:utf-8
from bs4 import BeautifulSoup
import re
import sqlite3
from jiayuan_grade_spider.jiayuan_log import spider_log


def user_process(uid, user_raw_data, db_path):
    # 下面定义了需要获取的数据容器
    #
    grade = {
        'total_grade': '0',
        'rank': '0%'
    }
    #
    info_degree = {
        'info_grade': 0,
        'info_degree': '0%',
        'integrity_degree': '0星',
        'photo_degree': '0张'
    }
    #
    safe_degree = {
        'safe_grade': 0,
        'ip_degree': 'safe',
        'login_degree': 'consistent'
    }
    #
    integrity_degree = {
        'integrity_grade': 0,
        'read_degree': '0%',
        'reply_degree': '0%',
        'sensitive_degree': '0%',
        'follow_rule_degree': '0%'
    }
    #
    frequence_degree = {
        'frequence_grade': 0,
        'login_times': 'normal',
        'recent_login': 'yes',
        'search_users': 'many',
        'vip_cost': 'no',
        'vip_server': 'no'
    }
    #
    behavior_degree = {
        'behavior_grade': 0,
        'black_list': 'no',
        'pre_black_list': 'no',
        'complain_list': 'no'
    }

    # maybe use a class will be better.
    user_grade = [grade, info_degree, safe_degree, integrity_degree, frequence_degree, behavior_degree]

    # parse data.
    raw_data = user_raw_data
    soup = BeautifulSoup(raw_data, "lxml")

    try:
        # 定位到表格区域
        table = soup.body.div.div.next_sibling.next_sibling
        # 用户总分
        total_grade = table.div.span.text
        user_grade[0]['total_grade'] = total_grade
        # 用户排名
        rank = table.div.span.next_sibling.next_sibling.text
        user_grade[0]['rank'] = rank

        # 各项评分
        grade_1 = table.div.next_sibling.next_sibling.ul.li
        user_grade[1]['info_grade'] = grade_1.span.next_sibling.next_sibling.text
        grade_2 = grade_1.next_sibling.next_sibling
        user_grade[2]['safe_grade'] = grade_2.span.next_sibling.next_sibling.text
        grade_3 = grade_2.next_sibling.next_sibling
        user_grade[3]['intergrity_grade'] = grade_3.span.next_sibling.next_sibling.text
        grade_4 = grade_3.next_sibling.next_sibling
        user_grade[4]['frequence__grade'] = grade_4.span.next_sibling.next_sibling.text
        grade_5 = grade_4.next_sibling.next_sibling
        user_grade[5]['behavior_grade'] = grade_5.span.next_sibling.next_sibling.text

        # 详细评分
        data = table.div.next_sibling.next_sibling.div.find_all(class_='kop-txt')

        # 资料可信度
        user_grade[1]['info_degree'] = (re.findall(r'：(.+?)</span>', str(data[0])))[0]
        user_grade[1]['integrity_degree'] = (re.findall(r'：(.+?)</span>', str(data[1])))[0]
        user_grade[1]['photo_degree'] = (re.findall(r'：(.+?)</span>', str(data[2])))[0]

        # 账号安全度
        user_grade[2]['ip_degree'] = (re.findall(r'：(.+?)</span>', str(data[3])))[0]
        login_data = table.div.next_sibling.next_sibling.div.find_all(class_='kop-allTxt')
        user_grade[2]['login_degree'] = (re.findall(r'：(.+?)</span>', str(login_data)))[0]

        # 交友真诚度
        user_grade[3]['read_degree'] = (re.findall(r'：(.+?)</span>', str(data[4])))[0]
        user_grade[3]['reply_degree'] = (re.findall(r'：(.+?)</span>', str(data[5])))[0]
        user_grade[3]['sensitive_degree'] = (re.findall(r'：(.+?)</span>', str(data[6])))[0]
        user_grade[3]['follow_rule_degree'] = (re.findall(r'：(.+?)</span>', str(data[7])))[0]

        # 交友紧迫度
        user_grade[4]['login_times'] = (re.findall(r'：(.+?)</span>', str(data[8])))[0]
        user_grade[4]['recent_login'] = (re.findall(r'：(.+?)</span>', str(data[9])))[0]
        user_grade[4]['search_users'] = (re.findall(r'：(.+?)</span>', str(data[10])))[0]
        user_grade[4]['vip_cost'] = (re.findall(r'：(.+?)</span>', str(data[11])))[0]
        user_grade[4]['vip_server'] = (re.findall(r'：(.+?)</span>', str(data[12])))[0]

        # 行为合规度
        user_grade[5]['black_list'] = (re.findall(r'：(.+?)</span>', str(data[13])))[0]
        user_grade[5]['pre_black_list'] = (re.findall(r'：(.+?)</span>', str(data[14])))[0]
        user_grade[5]['complain_list'] = (re.findall(r'：(.+?)</span>', str(data[15])))[0]
    except:
        spider_log(uid + ", cookie expired.")

    # 以上分别清理了正常用户和异常用户的数据，并暂存在dic中
    conn = sqlite3.connect(db_path)
    cu = conn.cursor()
    # create db if not exsit.

    try:
        '''
         uid, 靠谱度, 靠谱排名,
         资料可信度, 资料完成度, 诚信认证, 上传照片,
         账号安全度, 最后登录IP号段, 注册地与登陆地,
         交友真诚度, 看信比例, 回信比例, 敏感词比例, 发信符合择偶条件比例,
         交友紧迫度, 登陆次数, 最近1天登录, 浏览资料数, 会员消费, 会员服务,
         行为合规度, 是否加黑, 是否准加黑, 是否投诉
         '''

        CREATE_DB = "CREATE TABLE f_user_grade(id INTEGER PRIMARY KEY AUTOINCREMENT, uid TEXT, KPD INTEGER, KPPM CHAR(5), "\
            "ZLKXD CHAR(5), ZLWCD CHAR(5), CXRZ CHAR(5), SCZP CHAR(5), "\
            "ZHAQD CHAR(5), ZHDL_IP CHAR(5), ZCDYDLD CHAR(5), "\
            "JYZCD CHAR(5), KXBL CHAR(5), HXBL CHAR(5), MGCBL CHAR(5), FXFHZYTJBL CHAR(5), "\
            "JYJPD CHAR(5), DLCS CHAR(5), ZJYTDL CHAR(5), LLZLS CHAR(5), HYXF CHAR(5), HYFW CHAR(5), "\
            "XWHGD CHAR(5), SFJH CHAR(5), SFZJH CHAR(5), SFTS CHAR(5))"

        cu.execute(CREATE_DB)
        spider_log("db create.")
    except:
        pass

    try:
        INSERT_DB = "insert into f_user_grade(uid, KPD, KPPM, " \
                    "ZLKXD, ZLWCD, CXRZ, SCZP, " \
                    "ZHAQD, ZHDL_IP, ZCDYDLD, " \
                    "JYZCD, KXBL, HXBL, MGCBL, FXFHZYTJBL, " \
                    "JYJPD, DLCS, ZJYTDL, LLZLS, HYXF, HYFW, " \
                    "XWHGD, SFJH, SFZJH, SFTS) values(\'" + \
                    uid + "\', \'" + user_grade[0]['total_grade'] + "\', \'" + user_grade[0]['rank'] + "\', \'" + \
                    user_grade[1]['info_grade'] + "\', \'" + user_grade[1]['info_degree'] + "\', \'" + user_grade[1]['integrity_degree'] + "\', \'" + user_grade[1]['photo_degree'] + "\', \'" + \
                    user_grade[2]['safe_grade'] + "\', \'" + user_grade[2]['ip_degree'] + "\', \'" + user_grade[2]['login_degree'] + "\', \'" + \
                    user_grade[3]['intergrity_grade'] + "\', \'" + user_grade[3]['read_degree'] + "\', \'" + user_grade[3]['reply_degree'] + "\', \'" + user_grade[3]['sensitive_degree'] + "\', \'" + user_grade[3]['follow_rule_degree'] + "\', \'" + \
                    user_grade[4]['frequence__grade'] + "\', \'" + user_grade[4]['login_times'] + "\', \'" + user_grade[4]['recent_login'] + "\', \'" + user_grade[4]['search_users'] + "\', \'" + user_grade[4]['vip_cost'] + "\', \'" + user_grade[4]['vip_server'] + "\', \'" + \
                    user_grade[5]['behavior_grade'] + "\', \'" + user_grade[5]['black_list'] + "\', \'" + user_grade[5]['pre_black_list'] + "\', \'" + user_grade[5]['complain_list']  + "\')"
        cu.execute(INSERT_DB)
        spider_log(uid + ", data insert.")
    except:
        pass

    cu.close()
    conn.commit()
    conn.close()
