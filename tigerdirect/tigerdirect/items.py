# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TigerDirectCategory(scrapy.Item):
    itemType = scrapy.Field() #category
    categoryName = scrapy.Field()
    tdCategoryID= scrapy.Field()
    tdCategoryLevel = scrapy.Field()
    tdCategoryParent = scrapy.Field()
    uri = scrapy.Field()
    #hierarchy = scrapy.Field()
    manufacturers = scrapy.Field() #this contains an array of TigerDirectManufacturer s

class TigerDirectManufacturer(scrapy.Item):
    mfgName = scrapy.Field()
    mfgID = scrapy.Field()
    itemType = scrapy.Field() # manufacturer

class PriceItem(scrapy.Item):
    source = scrapy.Field()
    crawlTimestamp = scrapy.Field()
    _td_priceBox = scrapy.Field()
    fullPrice = scrapy.Field()
    salePrice = scrapy.Field()
    rebateAmount = scrapy.Field()
    finalPrice = scrapy.Field()
    purchaseURL = scrapy.Field()
    itemType = scrapy.Field() # price
    itemID = scrapy.Field()
    itemMongoID = scrapy.Field()

class TigerdirectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    itemType = scrapy.Field()   #item['type'] = "product"
    productName = scrapy.Field()
    link = scrapy.Field()
    detailsLink = scrapy.Field()
    #listPrice = scrapy.Field()
    itemNo = scrapy.Field()
    modelNo = scrapy.Field()
    tdCategoryID = scrapy.Field()
    specifications = scrapy.Field()
    source = scrapy.Field()
    crawlTimestamp = scrapy.Field()
    #some fields specific to tiger direct: (all the _td's)
    #_prodName = scrapy.Field()

    pricings = scrapy.Field()
    #need a price object... with a timestamp field. maybe timestamp is the index value
    _td_priceBox = scrapy.Field()
    #_td_salePrice = scrapy.Field()
    #_td_priceRebate = scrapy.Field() #how much is the rebate? Probably a negative value
    #_td_priceFinal = scrapy.Field() #final price - sale minus rebate

class SpecificationsItem(scrapy.Item):
    #Canonical stuff defined here. Other stuff will be added too
    #mostly this is here for consistency, and so I can have a seperate pipeline
    #because, at the end this is converted back to key/value pairs and merged in to TigerdirectItem['specifications']
    itemID = scrapy.Field() #used to tie specifications to item
    itemType = scrapy.Field() #specifications
    specType = scrapy.Field() #for example: 'harddrive', 'monitor' etc
    driveBytesCapacity=scrapy.Field() #the capacity, converted to bytes for consistency.
    driveType=scrapy.Field() #internal, external etc
    driveMedium=scrapy.Field() #ssd or spinning?
    genericSpecs = scrapy.Field()

