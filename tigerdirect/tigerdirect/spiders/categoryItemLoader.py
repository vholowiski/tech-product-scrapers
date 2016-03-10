from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from scrapy.contrib.loader.processor import Identity

import re
import string

class CategoryItemLoader(ItemLoader):
	def catIDfromURL(url):
		#needs to be put in a utility file, because this is also used in td_spider.py
		itemIdQuery = re.compile('[Cc]at[Ii]d=[0-9]+$')
		categoryIDtxt = re.findall(itemIdQuery, url)[0]
		categoryID = categoryIDtxt.replace("CatId=", "")
		return int(categoryID)
	
	def catLevelfromURL(url):
		#needs to be put in a utility file, because this is also used in td_spider.py
		catLevelQuery = re.compile('(?:category\_)([st])(?:lc)')
		catLevelArry = re.findall(catLevelQuery, url)
		if catLevelArry:
			catLevel = catLevelArry[0]
			if catLevel == 't':
				#top level - level 1
				return 1
			if catLevel == 's':
				#second level - level 2
				return 2

	def linkToMfgID(link):
		onclick = link.xpath("@onclick").extract()
		if onclick:
			mfgquery = re.compile('[Mm]fr[Ii]d=[0-9]+\"')
			mfgId = re.findall(mfgquery, onclick[0])
			if mfgId:
				mfgId = mfgId[0].replace("MfrId=","").replace("\"","")
				mfgId = mfgId.encode('utf-8')
				return int(mfgId)

	default_input_processor = Identity()
	default_output_processor = Join()
	
	categoryName_in = TakeFirst()
	categoryName_out = Join()

	tdCategoryID_in = MapCompose(catIDfromURL)
	tdCategoryID_out = TakeFirst()

	tdCategoryParent_in = Identity()
	tdCategoryParent_out = Identity()

	tdCategoryLevel_in = MapCompose(catLevelfromURL)
	tdCategoryLevel_out = TakeFirst()

	manufacturers_in = MapCompose(linkToMfgID)
	manufacturers_out = Identity()

