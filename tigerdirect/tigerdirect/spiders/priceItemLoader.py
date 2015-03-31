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
	def parseFinalPrice(priceIn):
		#print priceIn
		dollarQuery = re.compile('(?:[Ss]ale[Pp]rice.+?)([0-9]+)') #this regex should get just the numeric dollar amount
		dollar = re.findall(dollarQuery, priceIn)[0]
		
		decimalQuery = re.compile('(?:[pP]rice[dD]ecimal[mM]ark.*)[0-9]+')
		decimal = re.findall(decimalQuery, priceIn)[0]
		secondDecimalQuery = re.compile('[0-9]+')
		decimal = re.findall(secondDecimalQuery, priceIn)[0]
		finalPrice = '.'.join((dollar,decimal))
		return finalPrice

	default_input_processor = Identity()
	default_output_processor = Join()

	salePrice_in = MapCompose(parseSalePrice)
	salePrice_out = Join()

	finalPrice_in = MapCompose(parseFinalPrice)
	finalPrice_out = Join()







	# isThereaFinalPrice = response.xpath('//dd[contains(@class, "priceFinal")]')
	# 	if isThereaFinalPrice:
	# 		dollar = ""
	# 		decimal = ""
	# 		price = ""
	# 		priceFinalDollarArray = response.xpath('//dd[contains(@class, "priceFinal")]/span/text()')
	# 		if priceFinalDollarArray:
	# 			dollar = priceFinalDollarArray[0].extract()
			
	# 		priceFinalDecimal = response.xpath('//dd[contains(@class, "priceFinal")]/span/descendant::*/text()').extract()
	# 		if priceFinalDecimal:
	# 			decimal = ''.join(priceFinalDecimal).strip().replace("\n","").replace("\r","").replace(" ","").replace("$","").replace("*","")
			
	# 		price = ''.join((dollar,decimal))
	# 		pricing['finalPrice'] = price