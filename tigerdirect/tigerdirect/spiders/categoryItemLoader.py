from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from scrapy.contrib.loader.processor import Identity

import re
import string

class CategoryItemLoader(ItemLoader):
	def catIDfromURL(url):
		itemIdQuery = re.compile('[Cc]at[Ii]d=[0-9]+$')
		categoryIDtxt = re.findall(itemIdQuery, url)[0]
		categoryID = categoryIDtxt.replace("CatId=", "")
		return categoryID

	default_input_processor = Identity()
	default_output_processor = Join()
	
	name_in = TakeFirst()
	name_out = Join()

	id_in = MapCompose(catIDfromURL)
	id_out = TakeFirst()