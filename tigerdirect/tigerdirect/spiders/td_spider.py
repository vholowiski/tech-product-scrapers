import scrapy
import time
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from tigerdirect.items import TigerdirectItem
from tigerdirect.items import TigerDirectCategory
from tigerdirect.items import SpecificationsItem
from tigerdirect.items import PriceItem
import re

class TigerDirectSpider(CrawlSpider): 
	name = "tigerdirect"
	allowed_domains = ["www.tigerdirect.ca"]
	#start_urls = ["http://www.tigerdirect.ca/applications/category/category_slc.asp?Recs=30&Nav=|c:6957|&Sort=4",
	#"http://www.tigerdirect.ca/applications/category/category_slc.asp?page=2&Nav=|c:6957|&Sort=4&Recs=30",
	#"http://www.tigerdirect.ca/applications/category/category_slc.asp?page=3&Nav=|c:6957|&Sort=4&Recs=30",
	#"http://www.tigerdirect.ca/applications/category/category_slc.asp?page=4&Nav=|c:6957|&Sort=4&Recs=30"
	#]
	#start_urls = ["http://www.tigerdirect.ca/applications/SearchTools/item-details.asp?EdpNo=9516609&CatId=6957"]
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
		item = TigerDirectCategory()
		item['type'] = "category"
		item['name'] = response.xpath('//a[@class="crumbCat"]/text()').extract()
		#item['id'] = 
		catHrefs = response.xpath('//a[@class="crumbCat"]/@href')
		if catHrefs:	
			categoriesAccumulated = [];
			i = 0
			for categories in catHrefs:
				hCat = TigerDirectCategory()
				catQuery = re.compile('CatId=[0-9]+$')
				hCat['id'] = re.findall(catQuery, categories.extract())[0].replace("CatId=","")
				#hCat['id'] = re.findall(catQuery, categories.extract().replace("CatId=","")
				hCat['name'] = response.xpath('//a[@class="crumbCat"]/text()')[i].extract()
				categoriesAccumulated.append(hCat)
			item['hierarchy'] = categoriesAccumulated
		return item

	def parse_items(self, response):
		#filename = response.url.split("/")[-2]
		#with open(filename, 'wb') as f:
		item = TigerdirectItem()
		item['type'] = "product"
		item['crawlTimestamp'] = time.time()
		item['source'] = 'www.tigerdirect.ca'
		#item ['_prodName'] = response.xpath('//div[@class="prodName"]').extract().strip()

		item['productName'] = response.xpath('//div[@class="prodName"]/h1/text()').extract()

		strItemNumber = response.xpath('//div[@class="prodName"]/span[@class="sku"]/text()')[0].extract()
		strItemNumber = strItemNumber.strip().replace("\n","").replace("|","").replace("\r","").replace("\u00a0","").strip()
		item['itemNo'] = strItemNumber

		strModelNumber = response.xpath('//div[@class="prodName"]/span[@class="sku"]/text()')[1].extract()
		strModelNumber = strModelNumber.strip().replace("\n","").replace("|","").replace("\r","").replace("\u00a0","").strip()
		item['modelNo'] = strModelNumber

		#item.modelNo = response.xpath('//div[@class="prodName"]/span[@class="sku"]/text()')[1].extract().strip()
		pricebox = response.xpath('//dl[@class="priceBox"]')
		item['_td_priceBox'] = pricebox.extract() #just saving for later re-parsing

		#this is no good but getting close:
		#dds = pricebox.xpath('//dt/following::dd')
		#i need the dd of the dt class priceSale

		#pricebox.xpath('//dt[contains(@class,"priceSale")]').extract()
		#this gets me the dt right before the dd that I need
		#pricebox.xpath('//dd/following::dt') #gets the dd after a dt
		#this is the exact oposite of what I want: pricebox.xpath('//dd/preceding::dt[@class="priceSale priceToday"]').extract()
		#pricebox.xpath('"//dt[@class="priceSale priceToday"]::following/dd')
		#i think this one is right: pricebox.xpath('//dt/following::dd[@class="salePrice priceToday"]').extract()
		#salePriceNode = pricebox.xpath('//dt/following::dd[@class="salePrice priceToday"]')
		#node0 = salePriceNode[0]
		#price: ''.join(response.xpath('//dd[contains(@class, "salePrice")]/descendant::*/text()').extract())
		
		#create a new pricing object:
		pricing = PriceItem()

		salePrice = ''.join(response.xpath('//dd[contains(@class, "salePrice")]/descendant::*/text()').extract())
		salePrice = salePrice.strip().replace(" ","").replace("$","")
		
		#item['_td_salePrice'] = salePrice
		pricing['salePrice'] = salePrice

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
			item['specifications'] = specifications
		item['detailsLink'] = response.url
		return item
		#f.write(response.body)
		#products = response.xpath('//div[@class="product"]')
		#products.xpath('//p[@class="itemModel"]/text()').extract()
		#products.xpath('//h3[@class="itemName"]/a')
		#products.xpath('//h3[@class="itemName"]/a/text()')