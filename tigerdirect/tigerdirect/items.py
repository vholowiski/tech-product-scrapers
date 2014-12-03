# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TigerdirectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    productName = scrapy.Field()
    link = scrapy.Field()
    detailsLink = scrapy.Field()
    listPrice = scrapy.Field()
    itemNo = scrapy.Field()
    modelNo = scrapy.Field()
    pass
