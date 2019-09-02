import time

from module.spider_log import spider_log
from spider.ctrip_calendar_spider import ctrip_calendar_spider
from spider.qunar_calendar_spider import qunar_calendar_spider


def start_spider():

    ''' --- module spilt --- '''
    # 将希望爬取的路线写到该list中
    ctrip_air_port_list = [
        'chengdu-losangeles-ctu-lax', # 洛杉矶
        'chengdu-newyork-ctu-nyc', # 纽约
        'chengdu-tokyo-ctu-tyo', # 东京
        'chengdu-seoul-ctu-sel', # 首尔
        'chengdu-london-ctu-lon', # 伦敦
        'chengdu-sydney-ctu-syd', # 悉尼
        'chengdu-paris-ctu-par', # 巴黎
        'chengdu-moscow-ctu-mow' # 莫斯科
    ]

    spider_log("ctrip_spider,crawl air_line:")
    spider_log(str(ctrip_air_port_list))
    ctrip_calendar_spider(ctrip_air_port_list)
    spider_log("ctrip_spider stop.")
    time.sleep(1)


    ''' --- module spilt --- '''
    # 由于qunar对PhantJS支持不好，同时Firefox运行不稳定，所以先不加入qunar的数据采集
    # 将希望爬取的路线写到该list中

    qunar_air_port_list = [
        'searchDepartureAirport=成都&searchArrivalAirport=洛杉矶',
        'searchDepartureAirport=成都&searchArrivalAirport=纽约',
        'searchDepartureAirport=成都&searchArrivalAirport=东京',
        'searchDepartureAirport=成都&searchArrivalAirport=首尔',
        'searchDepartureAirport=成都&searchArrivalAirport=伦敦',
        'searchDepartureAirport=成都&searchArrivalAirport=悉尼',
        'searchDepartureAirport=成都&searchArrivalAirport=巴黎',
        'searchDepartureAirport=成都&searchArrivalAirport=莫斯科'
    ]

    spider_log("qunar_spider, crawl air_line:")
    spider_log(str(qunar_air_port_list))
    qunar_calendar_spider(qunar_air_port_list)
    spider_log("qunar_spider stop.")
    time.sleep(1)

    ''' --- module spilt --- '''


'''
if __name__ == '__main__':
    start_spider()
'''