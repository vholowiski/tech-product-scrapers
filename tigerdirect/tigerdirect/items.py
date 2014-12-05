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
    crawlTimestamp = scrapy.Field()
    #some fields specific to tiger direct: (all the _td's)
    _prodName = scrapy.Field()

    #need a price object... with a timestamp field. maybe timestamp is the index value
    _td_priceBox = scrapy.Field()
    _td_salePrice = scrapy.Field()
    _td_priceRebate = scrapy.Field() #how much is the rebate? Probably a negative value
    _td_priceFinal = scrapy.Field() #final price - sale minus rebate
