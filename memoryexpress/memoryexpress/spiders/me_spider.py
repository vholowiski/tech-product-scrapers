import scrapy
import time
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from tigerdirect.items import MemoryexpressItem

class MemoryexpressSpider(CrawlSpider): 
	name = "memoryexpress"
	allowed_domains = ["http://www.memoryexpress.com/"]
	
	start_urls = ["http://www.memoryexpress.com/"]
	#one page, for rules: http://www.tigerdirect.ca/applications/category/category_slc.asp?CatId=6845
	#and item details: http://www.tigerdirect.ca/applications/SearchTools/item-details.asp?EdpNo=9561721&CatId=6845
	rules = (
		Rule(LinkExtractor(allow=('\/[cC]ategory', ),deny=('\/Checkout',))),
		Rule(LinkExtractor(allow=('\/[Pp]roducts/.+[^\/]$', ))), callback='parse_items', follow= True),
	)

	def parse_items(self, response):
			item MemoryexpressItem()
			item['crawlTimestamp'] = time.time()
			item['source'] = 'www.memoryexpress.com'
			item['detailsLink'] = response.url

			