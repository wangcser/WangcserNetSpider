# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class JiayuanListItem(scrapy.Item):

    user_list_item = scrapy.Field()
    pass

class JiayuanUserItem(scrapy.Item):

    user_id_item = scrapy.Field()
    user_data_item = scrapy.Field()
    pass
