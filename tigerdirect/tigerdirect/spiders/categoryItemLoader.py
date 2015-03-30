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
	
	def linkToMfgID(link):
		onclick = link.xpath("@onclick").extract()
		if onclick:
			mfgquery = re.compile('[Mm]fr[Ii]d=[0-9]+\"')
			mfgId = re.findall(mfgquery, onclick[0])
			if mfgId:
				mfgId = mfgId[0].replace("MfrId=","").replace("\"","")
				mfgId = mfgId.encode('utf-8')
				return mfgId

	default_input_processor = Identity()
	default_output_processor = Join()
	
	categoryName_in = TakeFirst()
	categoryName_out = Join()

	tdCategoryID_in = MapCompose(catIDfromURL)
	tdCategoryID_out = TakeFirst()

	manufacturers_in = MapCompose(linkToMfgID)
	manufacturers_out = Identity()