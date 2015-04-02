from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from scrapy.contrib.loader.processor import Identity

import re
import string

#from tigerdirect.utils.specificationUtils import *
#import tigerdirect.utils.specificationUtils
#from tigerdirect.stuff.specificationUtils import ParseSpecifications

class ItemItemLoader(ItemLoader):
	def cleanString(string):
		cleanQuery=re.compile('[A-Za-z0-9 .",\'!-]')
		string=''.join(re.findall(cleanQuery, string))
		return string
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
	def parseSpecification(specificationKV):
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

		returnVal = cleanKV(specificationKV)
		if isSpecial(returnVal):
			print "CAPACAITY"
			print "CAPACAITY"
			print "CAPACAITY"
			print "CAPACAITY"
			print "CAPACAITY"
			print "CAPACAITY"
			print "CAPACAITY"
			print "CAPACAITY"
			print "CAPACAITY"
			print "CAPACAITY"
			print "CAPACAITY"
			print "CAPACAITY"
			print "CAPACAITY"
			print "CAPACAITY"
			print "CAPACAITY"
			print "CAPACAITY"
			print "CAPACAITY"
			print "CAPACAITY"
			print "CAPACAITY"
			print "CAPACAITY"
			print "CAPACAITY"
			print "CAPACAITY"
			print "CAPACAITY"
			
		return returnVal
		#kv because it comes in as key/value dict

	default_input_processor = Identity()
	default_output_processor = Join()

	productName_in = MapCompose(unicode.title, cleanString)
	productName_out = Join()

	itemNo_in = MapCompose(parseItemNo)
	itemNo_out = Join()

	modelNo_in = MapCompose(parseModelNo)
	modelNo_out = Join()

	tdCategoryID_in = MapCompose(catIDfromURL)
	tdCategoryID_out = Identity()

	specifications_in = MapCompose(parseSpecification)
	specifications_out = Identity()