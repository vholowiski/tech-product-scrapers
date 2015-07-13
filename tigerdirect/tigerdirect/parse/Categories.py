#parses categories and manufacturers

#general libraries
import scrapy
import re

#item definitions
from tigerdirect.items import TigerDirectCategory
from tigerdirect.items import TigerDirectManufacturer

#item loaders
from tigerdirect.spiders.categoryItemLoader import CategoryItemLoader
from tigerdirect.spiders.mfgItemLoader import MfgItemLoader

def parse_categories(self, response):
	#print("111111111def parse_items(self, response):111111111111")
	if response.xpath('//a[@class="crumbCat"]/text()'):
		l = CategoryItemLoader(TigerDirectCategory(), response)
		l.add_value('itemType', 'category')
		l.add_value('categoryName', response.xpath('//a[@class="crumbCat"]/text()').extract())
		l.add_value('tdCategoryID', response.url)
		#manufacturers
		#print("222222222222222222")
		for link in response.xpath('//ul[@class="filterItem"]/li/a'):
			#print("333333333333333333")
			l.add_value('manufacturers', link)
		l.add_value('uri', response.url)
		itemProcessedCatetory = TigerDirectCategory(l.load_item())
		yield itemProcessedCatetory

		#this spews manufacturers
		mfgLinksList = [response.xpath('//ul[@class="filterItem"]/li/a'), response.xpath('//ul[@class="filterItem"]/span/li/a')]
		#print("4444444444444444")
		for mfgLinks in mfgLinksList:
			#print("55555555555555555")
			for link in mfgLinks:
				#print("666666666666666666")
				l = MfgItemLoader(TigerDirectManufacturer(), response)
				l.add_value('mfgName', link.xpath("text()").extract()[0])
				l.add_value('itemType', 'manufacturer')
				l.add_value('mfgID', link)
				itemManufacturer = TigerDirectManufacturer(l.load_item())
				#print("7777777777777777")
				yield itemManufacturer
				#print("8888888888888888")
