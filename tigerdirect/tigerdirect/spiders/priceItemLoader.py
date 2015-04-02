from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from scrapy.contrib.loader.processor import Identity

import re
import string

class PriceItemLoader(ItemLoader):
	def cleanString(string):
		cleanQuery=re.compile('[A-Za-z0-9 .",\'!-]')
		string=''.join(re.findall(cleanQuery, string))
		return string
	def parseSalePrice(priceIn):
		salePrice = priceIn.strip().replace(" ","").replace("$","")
		return salePrice
	def parseRebateAmount(rebateIn):
		priceRebate = rebateIn.strip().replace("\n","").replace("\r","").replace(" ","").replace("$","")
		return priceRebate
	def parseFinalPrice(priceIn):
		#print priceIn
		query = re.compile('[0-9\.]')
		price = re.findall(query, priceIn)
		if price:
			finalPrice = ''.join(price)
		return finalPrice

	default_input_processor = Identity()
	default_output_processor = Join()

	
	salePrice_in = MapCompose(parseSalePrice)
	salePrice_out = Join()

	finalPrice_in = MapCompose(parseFinalPrice)
	finalPrice_out = Join()

