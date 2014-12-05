import scrapy
import time
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from tigerdirect.items import TigerdirectItem

class TigerDirectSpider(CrawlSpider): 
	name = "tigerdirect"
	allowed_domains = ["www.tigerdirect.ca"]
	#start_urls = ["http://www.tigerdirect.ca/applications/category/category_slc.asp?Recs=30&Nav=|c:6957|&Sort=4",
	#"http://www.tigerdirect.ca/applications/category/category_slc.asp?page=2&Nav=|c:6957|&Sort=4&Recs=30",
	#"http://www.tigerdirect.ca/applications/category/category_slc.asp?page=3&Nav=|c:6957|&Sort=4&Recs=30",
	#"http://www.tigerdirect.ca/applications/category/category_slc.asp?page=4&Nav=|c:6957|&Sort=4&Recs=30"
	#]
	#start_urls = ["http://www.tigerdirect.ca/applications/SearchTools/item-details.asp?EdpNo=9516609&CatId=6957"]
	start_urls = ["http://www.tigerdirect.ca/applications/category/category_slc.asp?CatId=6845"]
	#one page, for rules: http://www.tigerdirect.ca/applications/category/category_slc.asp?CatId=6845
	#and item details: http://www.tigerdirect.ca/applications/SearchTools/item-details.asp?EdpNo=9561721&CatId=6845
	rules = (
		Rule(LinkExtractor(allow=('category_slc\.asp\?CatId', ))),
		Rule(LinkExtractor(allow=('item-details\.asp\?EdpNo=', )), callback='parse_items'),
	)

	def parse_items(self, response):
		#filename = response.url.split("/")[-2]
		#with open(filename, 'wb') as f:
		item = TigerdirectItem()

		item['crawlTimestamp'] = time.time()
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
		salePrice = ''.join(response.xpath('//dd[contains(@class, "salePrice")]/descendant::*/text()').extract())
		salePrice = salePrice.strip().replace(" ","").replace("$","")
		item['_td_salePrice'] = salePrice

		priceRebateArray = response.xpath('//dd[contains(@class, "priceRebate")]/text()').extract()
		if priceRebateArray:
			priceRebate = priceRebateArray[0]
			priceRebate = priceRebate.strip().replace("\n","").replace("\r","").replace(" ","").replace("$","")
			item['_td_priceRebate'] = priceRebate

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
			item['_td_priceFinal'] = price
		
		item['detailsLink'] = response.url
		return item
		#f.write(response.body)
		#products = response.xpath('//div[@class="product"]')
		#products.xpath('//p[@class="itemModel"]/text()').extract()
		#products.xpath('//h3[@class="itemName"]/a')
		#products.xpath('//h3[@class="itemName"]/a/text()')