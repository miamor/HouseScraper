# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class muabanItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    price = scrapy.Field()
    phone = scrapy.Field()
    des = scrapy.Field()
    address = scrapy.Field()
    available = scrapy.Field()
    type = scrapy.Field()
    contact_email = scrapy.Field()
    area = scrapy.Field()
    thumbs = scrapy.Field()
    contact_name = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
