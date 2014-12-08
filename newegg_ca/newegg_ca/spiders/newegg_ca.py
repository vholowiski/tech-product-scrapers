import time
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from newegg_ca.items import NeweggCaItem

class NewEggCaSpider(CrawlSpider): 
	name = "newegg_ca"
	allowed_domains = ["www.newegg.ca"]

	start_urls = ["http://www.newegg.ca/ProductSort/CategoryList.aspx?Depa=0&Name=All-Categories"]

	#a category: http://www.newegg.ca/All-in-One-PCs/Category/ID-355?Tid=24203
	#a product: http://www.newegg.ca/Product/Product.aspx?Item=N82E16834757022
	rules = (
		Rule(LinkExtractor(allow=('Category\/ID-[0-9]+\?Tid=[0-9]+$', ),deny=('ShoppingCart')), callback='parse_categories'),
		Rule(LinkExtractor(allow=('item-details\.asp\?EdpNo=[0-9]*\&[cC]at[iI]d=[0-9]+$', ),deny=('ShoppingCart')), callback='parse_items', follow= True),
	)
	#rules = (
	#	Rule(LinkExtractor(allow=('_.lc\.asp\?CatId=[0-9]+$', ),deny=('SearchTools')), callback='parse_categories', follow= True),
	#	Rule(LinkExtractor(allow=('category\/super.asp?Id=', ))),
	#	Rule(LinkExtractor(allow=('item-details\.asp\?EdpNo=[0-9]*\&[cC]at[iI]d=[0-9]+$', ),deny=('searchtools')), callback='parse_items', follow= True),
	#)
	def parse_items(self, response):

			item['type'] = product
			item['crawlTimestamp'] = time.time()
			item['source'] = 'www.newegg.ca'
			item['productName'] = response.xpath('//span[contains(@id,"grpDescrip_0")]/text()')[0].extract()
			item['detailsLink'] = response.url

			# response.xpath('//*[@id="singleFinalPrice"]/strong/text()').extract()
			# response.xpath('//*[@id="singleFinalPrice"]/sup/text()').extract()
			#price = ''.join((dollar,decimal))

			#//*[@id="singleFinalPrice"]/strong
			#listPrice = scrapy.Field()
			#itemNo = scrapy.Field()
			#modelNo = scrapy.Field()
			#specifications = scrapy.Field()
			#source = scrapy.Field()

		return item