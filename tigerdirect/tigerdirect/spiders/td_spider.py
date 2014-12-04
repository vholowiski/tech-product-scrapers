import scrapy
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
		#item ['_prodName'] = response.xpath('//div[@class="prodName"]').extract().strip()

		item['productName'] = response.xpath('//div[@class="prodName"]/h1/text()').extract()
		
		strItemNumber = response.xpath('//div[@class="prodName"]/span[@class="sku"]/text()')[0].extract()
		strItemNumber = strItemNumber.strip().replace("\n","").replace("|","").replace("\r","").replace("\u00a0","").strip()
		item['itemNo'] = strItemNumber

		strModelNumber = response.xpath('//div[@class="prodName"]/span[@class="sku"]/text()')[1].extract()
		strModelNumber = strModelNumber.strip().replace("\n","").replace("|","").replace("\r","").replace("\u00a0","").strip()
		item['modelNo'] = strModelNumber

		#item.modelNo = response.xpath('//div[@class="prodName"]/span[@class="sku"]/text()')[1].extract().strip()

		item['detailsLink'] = response.url

		return item
		#f.write(response.body)


		#products = response.xpath('//div[@class="product"]')
		#products.xpath('//p[@class="itemModel"]/text()').extract()
		#products.xpath('//h3[@class="itemName"]/a')
		#products.xpath('//h3[@class="itemName"]/a/text()')


