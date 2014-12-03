import scrapy

class TigerDirectSpider(scrapy.Spider): 
	name = "tigerdirect"
	allowed_domains = ["www.tigerdirect.ca"]
	start_urls = ["http://www.tigerdirect.ca/applications/category/category_slc.asp?Recs=30&Nav=|c:6957|&Sort=4",
	"http://www.tigerdirect.ca/applications/category/category_slc.asp?page=2&Nav=|c:6957|&Sort=4&Recs=30",
	"http://www.tigerdirect.ca/applications/category/category_slc.asp?page=3&Nav=|c:6957|&Sort=4&Recs=30",
	"http://www.tigerdirect.ca/applications/category/category_slc.asp?page=4&Nav=|c:6957|&Sort=4&Recs=30"
	]

	def parse(self, response):
		filename = response.url.split("/")[-2]
		with open(filename, 'wb') as f:
			f.write(response.body)


			#products = response.xpath('//div[@class="product"]')
			#products.xpath('//p[@class="itemModel"]').extract()
			