from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from scrapy.contrib.loader.processor import Identity

import re
import string

class SpecificationItemLoader(ItemLoader):

	def cleanKey(key):
			cleanQuery=re.compile('[A-Za-z0-9 .-]')
			string=''.join(re.findall(cleanQuery, key))
			return string
	def cleanValue(value):
		cleanQuery=re.compile('[A-Za-z0-9 .",\'!-]')
		string=''.join(re.findall(cleanQuery, value))
		return value
	def cleanKV(specificationKV):
		returnKV={}
		for key, value in specificationKV.items():
			returnKV[cleanKey(key)]=cleanValue(value)
		return specificationKV
	def isSpecial(specificationKV):
		isspecial=false
		for key, value in specificationKV.items():
			if key=="Capactity":
				isspecial=true
		return isspecial

	default_input_processor = Identity()
	default_output_processor = Join()