import scrapy
import time
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from newegg_ca.items import NeweggCaItem
import re

from newegg_ca.spiders.ItemItemLoader import ItemItemLoader

class NewEggCaSpider(CrawlSpider): 
	name = "neweggCanada"
	allowed_domains = ["www.newegg.ca"]

	start_urls = ["http://www.newegg.ca/Product/Product.aspx?Item=N82E16834757022",
	"http://www.newegg.ca/Product/Product.aspx?Item=N82E16823126188",
	"http://www.newegg.ca/ProductSort/CategoryList.aspx?Depa=0&Name=All-Categories"
	]

	#a category: http://www.newegg.ca/All-in-One-PCs/Category/ID-355?Tid=24203
	#a product: http://www.newegg.ca/Product/Product.aspx?Item=N82E16834757022
	#another product http://www.newegg.ca/Product/Product.aspx?Item=N82E16820226678
	#a messy product link http://promotions.newegg.ca/corsair/13-4480/index.html?cm_sp=SubCat_-_Internal-SSD-_-corsair%2f13-4480-_-http%3a%2f%2fpromotions.newegg.ca%2fcorsair%2f13-4480%2f118x118.jpg&icid=211345&_ga=1.218403545.1316303197.1430745554
	rules = (
		Rule(LinkExtractor(allow=('Category\/ID-[0-9]+\?Tid=[0-9]+$', ),deny=('ShoppingCart'))),
		Rule(LinkExtractor(allow=('Product\/Product.aspx\?Item=.*$', )), callback='parse_items', follow= True),
	)
	#rules = (
	#	Rule(LinkExtractor(allow=('_.lc\.asp\?CatId=[0-9]+$', ),deny=('SearchTools')), callback='parse_categories', follow= True),
	#	Rule(LinkExtractor(allow=('category\/super.asp?Id=', ))),
	#	Rule(LinkExtractor(allow=('item-details\.asp\?EdpNo=[0-9]*\&[cC]at[iI]d=[0-9]+$', ),deny=('searchtools')), callback='parse_items', follow= True),
	#)
	def parse_items(self, response):
		l = ItemItemLoader(NeweggCaItem(), response)
		#set up the basics
		l.add_value('itemType', 'product')
		l.add_value('crawlTimestamp', unicode(time.time()))
		l.add_value('source', 'www.newegg.ca')

		#get the product id
		l.add_value('itemNo', response.url)
		
		item = ItemItemLoader(l.load_item())

		yield item

		#item = NeweggCaItem()
		#item['type'] = "product"
		#item['crawlTimestamp'] = time.time()
		#item['source'] = 'www.newegg.ca'
		
		#prodName = response.xpath('//span[contains(@id,"grpDescrip_0")]/text()')
		#if prodName:
		#	item['productName'] = response.xpath('//span[contains(@id,"grpDescrip_0")]/text()')[0].extract()
		#item['detailsLink'] = response.url

		# response.xpath('//*[@id="singleFinalPrice"]/strong/text()').extract()
		# response.xpath('//*[@id="singleFinalPrice"]/sup/text()').extract()
		#price = ''.join((dollar,decimal))

		#//*[@id="singleFinalPrice"]/strong
		#listPrice = scrapy.Field()
		#itemNo = scrapy.Field()
		#modelNo = scrapy.Field()
		#specifications = scrapy.Field()
		#source = scrapy.Field()

		#return item