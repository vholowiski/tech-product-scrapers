import scrapy
import time
import re

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

#from tigerdirect.items import TigerdirectItem
#from tigerdirect.items import TigerDirectCategory
#from tigerdirect.items import SpecificationsItem
#from tigerdirect.items import PriceItem
#from tigerdirect.items import TigerDirectManufacturer
#from tig;erdirect.items import ItemSpecifications

#import parse_ that have been moved out to their own files
from tigerdirect.parse.Categories import parse_categories
from tigerdirect.parse.Items import parse_items

#from tigerdirect.spiders.categoryItemLoader import CategoryItemLoader
#from tigerdirect.spiders.mfgItemLoader import MfgItemLoader
#from tigerdirect.spiders.itemItemLoader import ItemItemLoader
#from tigerdirect.spiders.priceItemLoader import PriceItemLoader
#from tigerdirect.spiders.specificationItemLoader import SpecificationItemLoader

# In order to debug, scrape only one page, do the following:
# * comment out class TigerDirectSpider(CrawlSpider): 
# * uncomment class TigerDirectSpider(scrapy.Spider):
# * comment out start_urls and replace it with a start_urls with just one url, the one to crawl
# * comment out the rules block
# * comment out def parse_items(self, response):
# * uncomment def parse(self, response):


class TigerDirectSpider(CrawlSpider): 

	#def __init__(self, testURL = '', *args, **kwargs):
	#	super(TigerDirectSpider, self).__init__(*args, **kwargs)
	#	print "init"
		#self.testURL = testURL
                                                             		#if self.testURL:
	#	if self.testURL != '':
	#		print testURL

#class TigerDirectSpider(scrapy.Spider;):
	name = "tigerdirect"
	allowed_domains = ["www.tigerdirect.ca"]
	
	#start_urls = ["http://www.tigerdirect.ca/applications/SearchTools/item-details.asp?EdpNo=6894578&Sku=K102-1298"]

	#ssd specific start urls
	#start_urls = ["http://www.tigerdirect.ca/applications/Category/Category_tlc.asp?CatId=5298","http://www.tigerdirect.ca/applications/SearchTools/item-details.asp?EdpNo=8198962&Sku=H450-8419", "http://www.tigerdirect.ca/applications/SearchTools/item-details.asp?EdpNo=5774231&CatId=234","http://www.tigerdirect.ca/applications/SearchTools/item-details.asp?EdpNo=6894578&Sku=K102-1298"]
	
	#below start_urls is the right one to use in production
	start_urls = ["http://www.tigerdirect.ca/sectors/category/site-directory.asp",	"http://www.tigerdirect.ca/applications/Refurb/refurb_tlc.asp",	"http://www.tigerdirect.ca/applications/openbox/openbox_tlc.asp",	"http://www.tigerdirect.ca/applications/campaigns/deals.asp?campaignid=2835"]
	
	#rules for just ssd:
	#broken. wont crawl anything
	#rules = (
	#	Rule(LinkExtractor(allow=('_.lc\.asp\?CatId=5298+$', ),deny=('SearchTools')), callback='parse_categories', follow= True),
	#	Rule(LinkExtractor(allow=('item-details\.asp\?EdpNo=[0-9]*\&[cC]at[iI]d=[0-9]+$', ),deny=('searchtools')), callback='parse_items', follow= False),
	#)	

	rules = (
		Rule(LinkExtractor(allow=('_.lc\.asp\?CatId=[0-9]+$', ),deny=('SearchTools')), callback='parse_categories', follow= True),
		Rule(LinkExtractor(allow=('category\/super.asp?Id=', ))),
		Rule(LinkExtractor(allow=('item-details\.asp\?EdpNo=[0-9]*\&[cC]at[iI]d=[0-9]+$', ),deny=('searchtools')), callback='parse_items', follow= True),
	)

#	def parse_categories(self, response):

	#def parse(self, response):
#	def parse_items(self, response):
