from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from scrapy.contrib.loader.processor import Identity

import re
import string

class PriceItemLoader(ItemLoader):
	def parseSalePrice(priceIn):
		salePrice = priceIn.strip().replace(" ","").replace("$","")
		return salePrice
	def parseRebateAmount(rebateIn):
		priceRebate = rebateIn.strip().replace("\n","").replace("\r","").replace(" ","").replace("$","")
		return priceRebate

	default_input_processor = Identity()
	default_output_processor = Join()

	salePrice_in = MapCompose(parseSalePrice)
	salePrice_out = Join()

	