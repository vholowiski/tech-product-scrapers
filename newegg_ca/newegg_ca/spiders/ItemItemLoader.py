from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from scrapy.contrib.loader.processor import Identity

import re
import string

class ItemItemLoader(ItemLoader):
	default_input_processor = Identity()
	default_output_processor = Join()

	def itemIDfromURL(url):
		#Item=[a-zA-Z0-9]*
		itemQuery = re.compile('Item=[a-zA-Z0-9]*')
		itemString = re.findall(itemQuery, url)
		print itemString
		if itemString[0]:
			print itemString[0]
			return itemString[0].replace("Item=", "")

	itemNo_in = MapCompose(itemIDfromURL)
	itemNo_out = Join()