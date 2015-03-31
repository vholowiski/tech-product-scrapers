import scrapy
import time
import re

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from tigerdirect.items import TigerdirectItem
from tigerdirect.items import TigerDirectCategory
from tigerdirect.items import SpecificationsItem
from tigerdirect.items import PriceItem
from tigerdirect.items import TigerDirectManufacturer

from tigerdirect.spiders.categoryItemLoader import CategoryItemLoader
from tigerdirect.spiders.mfgItemLoader import MfgItemLoader
from tigerdirect.spiders.itemItemLoader import ItemItemLoader
from tigerdirect.spiders.priceItemLoader import PriceItemLoader

class TigerDirectSpider(CrawlSpider): 
	name = "tigerdirect"
	allowed_domains = ["www.tigerdirect.ca"]
	start_urls = ["http://www.tigerdirect.ca/sectors/category/site-directory.asp",
	"http://www.tigerdirect.ca/applications/Refurb/refurb_tlc.asp",
	"http://www.tigerdirect.ca/applications/openbox/openbox_tlc.asp",
	"http://www.tigerdirect.ca/applications/campaigns/deals.asp?campaignid=2835"]
	#one page, for rules: http://www.tigerdirect.ca/applications/category/category_slc.asp?CatId=6845
	#and item details: http://www.tigerdirect.ca/applications/SearchTools/item-details.asp?EdpNo=9561721&CatId=6845
	rules = (
		Rule(LinkExtractor(allow=('_.lc\.asp\?CatId=[0-9]+$', ),deny=('SearchTools')), callback='parse_categories', follow= True),
		Rule(LinkExtractor(allow=('category\/super.asp?Id=', ))),
		Rule(LinkExtractor(allow=('item-details\.asp\?EdpNo=[0-9]*\&[cC]at[iI]d=[0-9]+$', ),deny=('searchtools')), callback='parse_items', follow= True),
	)

	def parse_categories(self, response):
		l = CategoryItemLoader(TigerDirectCategory(), response)
		l.add_value('itemType', 'category')
		l.add_value('categoryName', response.xpath('//a[@class="crumbCat"]/text()').extract())
		l.add_value('tdCategoryID', response.url)
		#manufacturers
		for link in response.xpath('//ul[@class="filterItem"]/li/a'):
			l.add_value('manufacturers', link)
		l.add_value('uri', response.url)
		itemProcessedCatetory = TigerDirectCategory(l.load_item())
		yield itemProcessedCatetory

		#this spews manufacturers
		mfgLinksList = [response.xpath('//ul[@class="filterItem"]/li/a'), response.xpath('//ul[@class="filterItem"]/span/li/a')]
		for mfgLinks in mfgLinksList:
			for link in mfgLinks:
				l = MfgItemLoader(TigerDirectManufacturer(), response)
				l.add_value('mfgName', link.xpath("text()").extract()[0])
				l.add_value('itemType', 'manufacturer')
				l.add_value('mfgID', link)
				itemManufacturer = TigerDirectManufacturer(l.load_item())
				yield itemManufacturer

	def parse_items(self, response):
		l = ItemItemLoader(TigerdirectItem(), response)
		item = TigerdirectItem()
		l.add_value('itemType', 'product')
		l.add_value('crawlTimestamp', unicode(time.time()))
		l.add_value('source', 'www.tigerdirect.ca')
		l.add_xpath('productName', ('//div[@class="prodName"]/h1/text()'))
		l.add_value('itemNo', response.xpath('//div[@class="prodName"]/span[@class="sku"]/text()')[0].extract())
		l.add_value('modelNo', response.xpath('//div[@class="prodName"]/span[@class="sku"]/text()')[1].extract())
		l.add_value('tdCategoryID', response.url)
		itemItem = TigerdirectItem(l.load_item())
		yield itemItem

		l = PriceItemLoader(PriceItem(), response)
		l.add_value('itemType', 'price')

		pricing = PriceItem()
		#pricing['itemType'] = 'price'
		l.add_xpath('salePrice', ('//dd[contains(@class, "salePrice")]/descendant::*/text()'))

		salePrice = ''.join(response.xpath('//dd[contains(@class, "salePrice")]/descendant::*/text()').extract())
		salePrice = salePrice.strip().replace(" ","").replace("$","")
		
		#item['_td_salePrice'] = salePrice
		pricing['salePrice'] = salePrice

		l.add_xpath('rebateAmount', ('//dd[contains(@class, "priceRebate")]/text()'))
		
		priceRebateArray = response.xpath('//dd[contains(@class, "priceRebate")]/text()').extract()
		if priceRebateArray:
			priceRebate = priceRebateArray[0]
			priceRebate = priceRebate.strip().replace("\n","").replace("\r","").replace(" ","").replace("$","")
			#item['_td_priceRebate'] = priceRebate
			pricing['rebateAmount'] = priceRebate

		#ugh. Messy. Dunno if this will work...
		isThereaFinalPrice = response.xpath('//dd[contains(@class, "priceFinal")]')
		if isThereaFinalPrice:
			dollar = ""
			decimal = ""
			price = ""
			priceFinalDollarArray = response.xpath('//dd[contains(@class, "priceFinal")]/span/text()')
			if priceFinalDollarArray:
				dollar = priceFinalDollarArray[0].extract()
			
			priceFinalDecimal = response.xpath('//dd[contains(@class, "priceFinal")]/span/descendant::*/text()').extract()
			if priceFinalDecimal:
				decimal = ''.join(priceFinalDecimal).strip().replace("\n","").replace("\r","").replace(" ","").replace("$","").replace("*","")
			
			price = ''.join((dollar,decimal))
			pricing['finalPrice'] = price
			#item['_td_priceFinal'] = price
		pricing['purchaseURL'] = response.url
		pricing['crawlTimestamp'] = time.time()
		pricing['source'] = 'www.tigerdirect.ca'
		#and add the pricing to the pricings object
		item['pricings'] = pricing

		priceItem = PriceItem(l.load_item())
		yield priceItem

		#specs:
		#from the spec table
		#th = key : response.xpath('//table[contains(@class, "prodSpec")]/tbody/tr/th/text()').extract()
		#td = value : response.xpath('//table[contains(@class, "prodSpec")]/tbody/tr/td/text()').extract()  
		specifications = []
		specKeys = response.xpath('//table[contains(@class, "prodSpec")]/tbody/tr/th/text()')
		if specKeys:
			i = 0
			for key in specKeys:
				value = response.xpath('//table[contains(@class, "prodSpec")]/tbody/tr/td/text()')[i]
				s1 = SpecificationsItem(
					)
				s1['specName'] = key.extract()
				s1['specValue'] = value.extract()
				specifications.append(s1)
				i = i + 1
			specifications['itemType'] = 'specifications'
			item['specifications'] = specifications
		item['detailsLink'] = response.url
		#return item
		#f.write(response.body)
		#products = response.xpath('//div[@class="product"]')
		#products.xpath('//p[@class="itemModel"]/text()').extract()
		#products.xpath('//h3[@class="itemName"]/a')
		#products.xpath('//h3[@class="itemName"]/a/text()')