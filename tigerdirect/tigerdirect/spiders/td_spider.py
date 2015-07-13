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
#from tigerdirect.items import ItemSpecifications

from tigerdirect.spiders.categoryItemLoader import CategoryItemLoader
from tigerdirect.spiders.mfgItemLoader import MfgItemLoader
from tigerdirect.spiders.itemItemLoader import ItemItemLoader
from tigerdirect.spiders.priceItemLoader import PriceItemLoader
from tigerdirect.spiders.specificationItemLoader import SpecificationItemLoader

# In order to debug, scrape only one page, do the following:
# * comment out class TigerDirectSpider(CrawlSpider): 
# * uncomment class TigerDirectSpider(scrapy.Spider):
# * comment out start_urls and replace it with a start_urls with just one url, the one to crawl
# * comment out the rules block
# * comment out def parse_items(self, response):
# * uncomment def parse(self, response):


class TigerDirectSpider(CrawlSpider): 
#class TigerDirectSpider(scrapy.Spider):
	name = "tigerdirect"
	allowed_domains = ["www.tigerdirect.ca"]
	
	#start_urls = ["http://www.tigerdirect.ca/applications/SearchTools/item-details.asp?EdpNo=6894578&Sku=K102-1298"]

	#start_urls = ["http://www.tigerdirect.ca/applications/Category/Category_tlc.asp?CatId=5298","http://www.tigerdirect.ca/applications/SearchTools/item-details.asp?EdpNo=8198962&Sku=H450-8419", "http://www.tigerdirect.ca/applications/SearchTools/item-details.asp?EdpNo=5774231&CatId=234","http://www.tigerdirect.ca/applications/SearchTools/item-details.asp?EdpNo=6894578&Sku=K102-1298"]
	
	#below start_urls is the right one to use in production
	start_urls = ["http://www.tigerdirect.ca/sectors/category/site-directory.asp",	"http://www.tigerdirect.ca/applications/Refurb/refurb_tlc.asp",	"http://www.tigerdirect.ca/applications/openbox/openbox_tlc.asp",	"http://www.tigerdirect.ca/applications/campaigns/deals.asp?campaignid=2835"]
	
	rules = (
		Rule(LinkExtractor(allow=('_.lc\.asp\?CatId=[0-9]+$', ),deny=('SearchTools')), callback='parse_categories', follow= True),
		Rule(LinkExtractor(allow=('category\/super.asp?Id=', ))),
		Rule(LinkExtractor(allow=('item-details\.asp\?EdpNo=[0-9]*\&[cC]at[iI]d=[0-9]+$', ),deny=('searchtools')), callback='parse_items', follow= True),
	)

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

	#def parse(self, response):
	def parse_items(self, response):
		#print("**********************")
		l = ItemItemLoader(TigerdirectItem(), response)
		item = TigerdirectItem()
		l.add_value('itemType', 'product')
		l.add_value('crawlTimestamp', unicode(time.time()))
		l.add_value('source', 'www.tigerdirect.ca')
		l.add_xpath('productName', ('//div[@class="prodName"]/h1/text()'))
		l.add_value('itemNo', response.xpath('//div[@class="prodName"]/span[@class="sku"]/text()')[0].extract())
		l.add_value('modelNo', response.xpath('//div[@class="prodName"]/span[@class="sku"]/text()')[1].extract())
		l.add_value('tdCategoryID', response.url)
		l.add_value('link', response.url)

		#are there specifications?
		#specifications = response.xpath('//div[@id="DetailedSpecs"]')
		# if response.xpath('//div[@id="DetailedSpecs"]'):
		# 	specKeys = response.xpath('//table[contains(@class, "prodSpec")]/tbody/tr/th/text()')
		# 	if specKeys:
		# 		i = 0
		# 		for key in specKeys:
		# 			value = response.xpath('//table[contains(@class, "prodSpec")]/tbody/tr/td/text()')[i]
		# 			s1={}
		# 			s1[key.extract()]=value.extract()
		# 			#s1['specName'] = key.extract()
		# 			#s1['specValue'] = value.extract()
		# 			l.add_value('specifications', s1)
		# 			i = i + 1

		itemItem = TigerdirectItem(l.load_item())
		yield itemItem

		l = PriceItemLoader(PriceItem(), response)
		l.add_value('_td_priceBox', response.xpath('//dl[@class="priceBox"]').extract())
		
		#pricing['itemType'] = 'price'
		l.add_value('itemType', 'price')

		pricing = PriceItem()
		
		l.add_xpath('salePrice', ('//dd[contains(@class, "salePrice")]/descendant::*/text()'))
		l.add_xpath('rebateAmount', ('//dd[contains(@class, "priceRebate")]/text()'))
		
		#priceRebateArray = response.xpath('//dd[contains(@class, "priceRebate")]/text()').extract()
		#if priceRebateArray:
		#	priceRebate = priceRebateArray[0]
		#	priceRebate = priceRebate.strip().replace("\n","").replace("\r","").replace(" ","").replace("$","")
		#	#item['_td_priceRebate'] = priceRebate
		#	pricing['rebateAmount'] = priceRebate

		l.add_value('finalPrice', response.xpath('//dd[contains(@class, "priceFinal")]').extract())
		l.add_value('purchaseURL', response.url)
		#l.add_value('crawlTimestamp', time.time())
		l.add_value('source', 'wwww.tigerdirect.ca')

		l.add_value('itemID', itemItem['itemNo'])
		#l.addx('itemMongoID', bot)

		#TODO get price for 'add to car to see price'
		#http://www.tigerdirect.ca/applications/SearchTools/item-details.asp?CatId=5739&EdpNo=9641093
		#its in the javascript!
		
		priceItem = PriceItem(l.load_item())
		priceItem['crawlTimestamp']=time.time()
		yield priceItem

		#some ssd drives:
		#http://www.tigerdirect.ca/applications/SearchTools/item-details.asp?EdpNo=9099634&Sku=KIN-102513377
		#http://www.tigerdirect.ca/applications/SearchTools/item-details.asp?EdpNo=9640807&Sku=KNY-102878750
		#specifications?
		hasSpecifications = response.xpath('//span[contains(text(), "pecifications")]')
		if hasSpecifications:
			l = SpecificationItemLoader(SpecificationsItem(), response)
			l.add_value('itemID', itemItem['itemNo'])
			l.add_value('itemType', 'specifications')
			#get the keys (specificatin types) in the table
			specKeys = response.xpath('//table[contains(@class, "prodSpec")]/tbody/tr/th/text()')
			#print "found this many spec keys:"
			#print len(specKeys)
			#first recognize canonical specs
			i = 0
			genericSpecs = [] #set up an empty array for specs not canonical
			if len(specKeys) > 0:
				for key in specKeys:
					canonicalKeyFound = False
					valueArray = response.xpath('//table[contains(@class, "prodSpec")]/tbody/tr/td/text()')
					if valueArray:
						value = valueArray[i]
						#value = response.xpath('//table[contains(@class, "prodSpec")]/tbody/tr/td/text()')[i]
						key = key.extract()
						value = value.extract()

						#cleanKeyQuery = re.compile('[A-Za-z0-9 .-]')
						cleanKeyQuery = re.compile('[A-Za-z0-9 ]') #note- period and dash not allowed in key!
						cleanValueQuery = re.compile('[A-Za-z0-9 .",\'!-]')
						cleanKey = ''.join(re.findall(cleanKeyQuery, key))
						cleanValue = ''.join(re.findall(cleanValueQuery, value))
					
						#now, look for canonical
						#capacity, in bytes
						capacityQuery = re.compile('[Cc]apacity$')
						if re.findall(capacityQuery, cleanKey):
							l.add_value('driveBytesCapacity', cleanValue)
							canonicalKeyFound = True
						#internal, external?
						driveTypeQuery = re.compile('[Dd]rive [Tt]ype')
						if re.findall(driveTypeQuery, cleanKey):
							l.add_value('driveType', cleanValue)
							canonicalKeyFound = True
						#ssd or spinning?
						prodName = response.xpath('//div[@class="prodName"]/h1/text()').extract()[0]
						#TODO: Instead of searching for 'ssd' i shoud just be checking if this is a hard drive
							#and then setting it to ssd or spinning
							#but i need to build a function for that
							#for now, no ssd means its spinning
						#ssdQuery = re.compile('([Ss]olid [Ss]tate [Dd]rive)|([Ss][Ss][Dd])')
						#ssdQueryResult = re.findall(ssdQuery, prodName)
						#if ssdQueryResult:
						if re.findall(driveTypeQuery, cleanKey):
							#print "-----inside ssdQueryResult"
							#print ssdQueryResult[0]
							l.add_value('driveMedium', prodName)
							#l.add_value('driveMedium', ssdQueryResult[0])
							#print "----after addv_value"
							#print l
							#l.add_xpath('driveMedium', ('([Ss]olid [Ss]tate [Dd]rive)|([Ss][Ss][Dd])'))
							canonicalKeyFound = True

						i = i + 1
						if not canonicalKeyFound:
							addSpec = {cleanKey: cleanValue}
							genericSpecs +=[addSpec]
			#print "----about to load SpecificationsItem"
			#print l["driveMedium"]
			itemSpecifications = SpecificationsItem(l.load_item())
			itemSpecifications['genericSpecs'] = genericSpecs
			yield itemSpecifications
			#yield itemSpecifications
			#then create the item
			#then loop through the rest, and create them as non canonical	
