from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from scrapy.contrib.loader.processor import Identity

import re
import string

class MfgItemLoader(ItemLoader):
	def linkToMfgID(link):
		onclick = link.xpath("@onclick").extract()
		if onclick:
			mfgquery = re.compile('[Mm]fr[Ii]d=[0-9]+\"')
			mfgId = re.findall(mfgquery, onclick[0])
			if mfgId:
				mfgId = mfgId[0].replace("MfrId=","").replace("\"","")
				mfgId = mfgId.encode('utf-8')
				return mfgId

	def parsemfgName(link):
		#mfgName = link.xpath("text()").extract()[0]
		mfgName = link.encode('utf-8').strip()
		return mfgName

	default_input_processor = Identity()
	default_output_processor = Join()

	mfgName_in = MapCompose(parsemfgName)
	mfgName_out = Identity()

	mfgID_in = MapCompose(linkToMfgID)
	mfgID_out = Join()