# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class NeweggCaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    itemType = scrapy.Field()   #item['type'] = "product"
    productName = scrapy.Field()
    link = scrapy.Field()
    detailsLink = scrapy.Field()
    #listPrice = scrapy.Field()
    itemNo = scrapy.Field()
    modelNo = scrapy.Field()
    specifications = scrapy.Field()
    source = scrapy.Field()
    crawlTimestamp = scrapy.Field()