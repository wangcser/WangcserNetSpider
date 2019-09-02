#coding:utf-8

from bs4 import BeautifulSoup
import re
import sqlite3
import operator # 用于比较字符串，查找异常用户信息
from jiayuanspider.jiayuan_log import spider_log

'''
一个问题，页面上有些字段的信息是未给出的，需要测试一下当页面检索失败时候的情况，该问题已经解决了，采用了try机制
另外，html的title中也有一些信息，目前还没提取
'''
def user_process(user_id, user_raw_data, db_path):
    # 下面定义了需要获取的数据容器
    # 暂存用户基本数据
    info = {
        'nickname': '默认昵称',
        'uid': '',
        'charm': '',
        'age': '',
        'marriage': '',
        'province': '',
        'city': '',
        'education': '',
        'height': '',
        'weight': '',
        'salary': '',
        'car': '',
        'house': '',
        'constellation': '',
        'minority': '',
        'zodiac': '',
        'blood_type': ''
    }
    # 暂存用头像数据
    image = {
        'img_url': '',
        'img_num': ''
    }
    # 暂存用户自我简介
    self_intro = "self_intro."
    # 暂存用户的交友要求
    demand = {
        'demand_age': '',
        'demand_height': '',
        'demand_minority': '',
        'demand_education': '',
        'demand_photo': '',
        'demand_marriage': '',
        'demand_location': '',
        'demand_sincerity': ''
    }
    '''
    # 暂存用户的生活方式
    lifestyle = {
        'smoke': '',
        'drink': '',
        'exercise': '',
        'eat': '',
        'shop': '',
        'faith': '',
        'time': '',
        'circle': '',
        'cost': ''
    }
    '''
    '''
    # 暂存用户的经济能力，该信息已由基本信息给出
    economic = {
        'salary': '',
        'car': '',
        'house': ''
    }
    '''
    # 暂存用户的工作信息
    work = {
        'position': '',
        'industry': '',
        'university': '',
        'major': '',
        'language': ''
    }
    # 暂存用户的家庭信息
    marriage = {
        'origin': '',
        'residence': '',
        'nationality': '',
        'personality': '',
        'humor': '',
        'temper': '',
        'marriage_attitude': '',
        'kid': '',
        'marriage_time': '',
        'share_house': '',
        'parents': '',
        'relatives': ''
    }
    # maybe use a class will be better.
    user = [info, image, self_intro, demand, work, marriage]

    # parse data.
    raw_data = user_raw_data
    soup = BeautifulSoup(raw_data, "lxml")

    # 排除异常情况，对用户进行标记
    title_text = soup.title.text
    title_pattern = "世纪佳缘交友网:查看用户详细资料失败"
    if operator.eq(title_text, title_pattern):
        body_text = soup.body.text
        case_1 = ["该会员已被加黑"]
        case_2 = ["该用户找到意中人"]
        # case_3 = [""]

        if operator.eq(re.findall(r"该会员已被加黑", body_text), case_1):
            user[0]['uid'] = user_id
            user[0]['nickname'] = "该会员已被加黑"
            spider_log("insert uid: " + user[0]['uid'] + " 该会员已被加黑")
            pass

        elif operator.eq(re.findall(r"该用户找到意中人", body_text), case_2):
            user[0]['uid'] = user_id
            user[0]['nickname'] = "该用户找到意中人"
            spider_log("insert uid: " + user[0]['uid'] + " 该用户找到意中人")
            pass
        elif operator.eq(re.findall(r"该用户正在约会中", body_text), case_2):
            user[0]['uid'] = user_id
            user[0]['nickname'] = "该用户正在约会中"
            spider_log("insert uid: " + user[0]['uid'] + " 该用户正在约会中")
            pass
        else:
            pass
    else:

        # 全局定位方案，采用BOM迭代访问,下文中也采用了查找定位，查找的缺陷是后面的模块不好遍历
        user_info = soup.find(class_='content_705')
        # BOM树遍历
        # 自我介绍
        self_intro_div = user_info.div.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
        # 爱情DNA
        self_DNA_div = self_intro_div.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
        # 择偶要求
        self_demand_div = self_DNA_div.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
        # 生活方式
        self_style_div = self_demand_div.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
        # 经济实力
        self_economic_div = self_style_div.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
        # 工作学习
        self_work_div = self_economic_div.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
        # 婚姻观念
        self_marriage_div = self_work_div.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling


        #-----***-----
        # h4 data: nickname, uid
        tag = soup.h4.text
        # user nickname
        user[0]['nickname'] = (re.findall(r"(.+?)ID", tag))[0]
        #user uid
        user[0]['uid'] = (re.findall(u"[0-9]+",tag))[0]

        # h6 data: charm
        tag = soup.h6.text
        user[0]['charm'] = tag

        #user info.
        tag = soup.find(class_='member_name').text
        user[0]['age'] = (re.findall(u"[0-9]+",tag))[0]
        user[0]['marriage'] = (re.findall(r"岁，(.+?)，来", tag))[0]
        user[0]['province'] = soup.find(class_='member_name').a.text
        user[0]['city'] = soup.find(class_='member_name').a.next_sibling.text

        #user info detail.
        tag = soup.find(class_='member_info_list fn-clear')

        # html list obj.
        education = tag.li
        user[0]['education'] = education.em.text

        height = education.next_sibling.next_sibling
        user[0]['height'] = height.em.text

        car = height.next_sibling.next_sibling
        user[0]['car'] = car.div.next_sibling.next_sibling.text.strip()

        salary = car.next_sibling.next_sibling
        user[0]['salary'] = salary.div.next_sibling.next_sibling.text.strip()# 去掉 数据前面的换行

        house = salary.next_sibling.next_sibling
        user[0]['house'] =  house.div.next_sibling.next_sibling.text.strip()

        weight = house.next_sibling.next_sibling
        user[0]['weight'] = weight.div.next_sibling.next_sibling.text.strip()

        constellation = weight.next_sibling.next_sibling
        user[0]['constellation'] = constellation.em.text

        minority = constellation.next_sibling.next_sibling
        user[0]['minority'] = minority.em.text

        zodiac = minority.next_sibling.next_sibling
        user[0]['zodiac'] = zodiac.em.text

        blood_type = zodiac.next_sibling.next_sibling
        user[0]['blood_type'] = blood_type.em.text

        # self image.
        tag = soup.find(class_='big_pic fn-clear')
        attr = tag.ul.li.a.next_element.attrs # url 位于书标签属性之中，返回属性dict
        user[1]['img_url'] = attr['_src']

        img_num = soup.find(class_='pho_ico').text
        user[1]['img_num'] = img_num.strip() # remove subspace.

        # self intro.
        user_info = soup.find(class_='js_text').text
        user[2] = user_info.strip() # remove subspace.

        #demand info.
        try:
            tag = soup.find(class_='js_list fn-clear')

            demand_age = tag.li
            user[3]['demand_age'] = demand_age.div.text

            demand_height = demand_age.next_sibling.next_sibling
            user[3]['demand_height'] = demand_height.div.text

            demand_minority = demand_height.next_sibling.next_sibling
            user[3]['demand_minority'] = demand_minority.div.text

            demand_education = demand_minority.next_sibling.next_sibling
            user[3]['demand_education'] = demand_education.div.text

            demand_photo = demand_education.next_sibling.next_sibling
            user[3]['demand_photo'] = demand_photo.div.text

            demand_marriage = demand_photo.next_sibling.next_sibling
            user[3]['demand_marriage'] = demand_marriage.div.text

            demand_location = demand_marriage.next_sibling.next_sibling
            user[3]['demand_location'] = demand_location.div.text

            demand_sincerity = demand_location.next_sibling.next_sibling
            user[3]['demand_sincerity'] = demand_sincerity.div.text
        except:
            # print("user demand info is not exsit.")
            pass

        # work info.
        tag = self_work_div
        # 工作信息
        try:
            work_item = tag.ul
            work = work_item.li
            user[4]['position'] = work.em.text

            industry = work.next_sibling.next_sibling
            user[4]['industry'] = industry.em.text
        except:
            # print("work info is not exist.")
            pass

        # 学习信息
        try:
            study_item = tag.ul.next_sibling.next_sibling.next_sibling.next_sibling
            university = study_item.li
            user[4]['university'] = university.em.text

            major = university.next_sibling.next_sibling
            user[4]['major'] = major.em.text

            language = major.next_sibling.next_sibling
            user[4]['language'] = language.em.text
        except:
            # print("study info is not exist.")
            pass

        # marriage info.
        try:
            tag = self_marriage_div
            # 关于自己
            self_item = tag.ul
            about_self = self_item.li
            user[5]['origin'] = about_self.em.text

            residence = about_self.next_sibling.next_sibling
            user[5]['residence'] = residence.em.text

            nationality = residence.next_sibling.next_sibling
            user[5]['nationality'] = nationality.em.text

            personality = nationality.next_sibling.next_sibling
            user[5]['personality'] = personality.em.text

            humor = personality.next_sibling.next_sibling
            user[5]['humor'] = humor.em.text

            temper = humor.next_sibling.next_sibling
            user[5]['temper'] = temper.em.text

            marriage_attitude = temper.next_sibling.next_sibling
            user[5]['marriage_attitude'] = marriage_attitude.em.text

            kid = marriage_attitude.next_sibling.next_sibling
            user[5]['kid'] = kid.em.text

            marriage_time = kid.next_sibling.next_sibling
            user[5]['marriage_time'] = marriage_time.em.text
        except:
            # print("marriage info is not exist.")
            pass


        # 关于家庭
        try:
            family_item = tag.ul.next_sibling.next_sibling.next_sibling.next_sibling
            share_house = family_item.li
            user[5]['share_house'] = share_house.em.text

            relatives = share_house.next_sibling.next_sibling
            user[5]['relatives'] = relatives.em.text

            parents = relatives.next_sibling.next_sibling
            user[5]['parents'] = parents.em.text
        except:
            # print("family info is not exist.")
            pass


    # 以上分别清理了正常用户和异常用户的数据，并暂存在dic中

    conn = sqlite3.connect(db_path)
    cu = conn.cursor()
    #spider_log("database created, table name: m_user_table.")

    # create db if not exsit.
    try:
        CREATE_DB = "CREATE TABLE m_user_table(id INTEGER PRIMARY KEY AUTOINCREMENT, uid TEXT, nickname CHAR(50),charm INTEGER, "\
            "age INTEGER, height INTEGER, weight INTEGER, province CHAR(5), city CHAR(5), education CHAR(50), salary CHAR(50), car CHAR(10),"\
            " house CHAR(10), constellation CHAR(5), minority CHAR(2), zodiac CHAR(3), blood_type CHAR(3), marriage CHAR(3), img_url TEXT, "\
            "img_num INTEGER, self_intro TEXT)"

        cu.execute(CREATE_DB)

    except:
        #spider_log("database existed.")
        pass

    try:
        # 目前只设计了user info 数据的持久化，明天加入其它剩余数据的持久化，完成整个数据爬取和数据持久化的过程，集成到scrapy中，成后完成开发日志，如果将raw_data 本地化会占用大量的空间，不如使用数据库持久化
        INSERT_DB = "insert into m_user_table(uid, nickname, charm, age, height, weight, province, city, education, salary, car, house, constellation, minority, zodiac, blood_type" \
            ", marriage, img_url, img_num, self_intro) values(\'" + user[0]['uid'] + "\', \'" + user[0]['nickname'] + "\', \'" + user[0]['charm'] + "\', \'" + user[0]['age'] + \
             "\', \'" + user[0]['height'] + "\', \'" + user[0]['weight'] + "\', \'" + user[0]['province'] + "\', \'" + user[0]['city'] + "\', \'" + user[0]['education'] + \
             "\', \'" + user[0]['salary'] + "\', \'" + user[0]['car'] + "\', \'" + user[0]['house'] + "\', \'" + user[0]['constellation'] + "\', \'" + user[0]['minority'] + \
             "\', \'" + user[0]['zodiac'] + "\', \'" + user[0]['blood_type'] + "\', \'" + user[0]['marriage'] + "\', \'" + user[1]['img_url'] + "\', \'" + user[1]['img_num'] + \
             "\', \'" + user[2] + "\')"

        cu.execute(INSERT_DB)
        spider_log("insert uid: " + user[0]['uid'])
    except:
        spider_log("insert error. uid: " + user[0]['uid'])

    cu.close()
    conn.commit() # 只有commit()之后才能写入数据
    conn.close()

    file_name = user_id
    #file_name = user[0]['uid'] # 这种处理方法不能包括拉去不到用户信息的情况
    file_path = "E:/02 Python/01 crawl/jiayuanspider/04 user_data/raw_data/m_user/" + file_name + ".txt"
    f = open(file_path, 'w')
    try:
        f.write(user_raw_data)
        f.close()# 一个BUG，当用户名不包括gbk编码字符时，写文件报错（数据库数据无影响）

    except:
        str = "用户名包含非GBK编码字符，windows文本编码无法识别。"
        f.write(str)
        f.close()
