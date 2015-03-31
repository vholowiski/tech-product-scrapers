from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from scrapy.contrib.loader.processor import Identity

import re
import string

class ItemItemLoader(ItemLoader):
	def parseItemNo(itemin):
		#srItemNumber = itemin.extract()
		strItemNumber = itemin.strip().replace("\n","").replace("|","").replace("\r","").replace("\u00a0","").strip()
		return strItemNumber

	def parseModelNo(itemin):
		strModelNumber = itemin.strip().replace("\n","").replace("|","").replace("\r","").replace("\u00a0","").strip()
		return strModelNumber

	def catIDfromURL(url):
		itemIdQuery = re.compile('[Cc]at[Ii]d=[0-9]+')
		categoryIDtxt = re.findall(itemIdQuery, url)[0]
		categoryID = categoryIDtxt.replace("CatId=", "")
		return categoryID

	default_input_processor = Identity()
	default_output_processor = Join()

	productName_in = MapCompose(unicode.title)
	productName_out = Join()

	itemNo_in = MapCompose(parseItemNo)
	itemNo_out = Join()

	modelNo_in = MapCompose(parseModelNo)
	modelNo_out = Join()

	tdCategoryID_in = MapCompose(catIDfromURL)
	tdCategoryID_out = Identity()