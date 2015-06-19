from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from scrapy.contrib.loader.processor import Identity

import re
import string

class SpecificationItemLoader(ItemLoader):

	def capacityStrToBytes(strCapacity):
		print "-----parsecapacity"
		def capacityGetMultiplier(unit):
			multiplier = 0
			#TODO : recognize the difference betweent B and b. maybe?
			tbQuery = re.compile('[Tt][Bb]')
			if re.findall(tbQuery, unit):
				#is TB 1000000000000 bytes
				multiplier = 1000000000000
			gbQuery = re.compile('[Gg][Bb]')
			if re.findall(gbQuery, unit):
				#is TB 1000000000000 bytes
				multiplier = 1000000000
			mbQuery = re.compile('[Mm][Bb]')
			if re.findall(mbQuery, unit):
				#is TB 1000000000000 bytes
				multiplier = 1000000
			kbQuery = re.compile('[Kk][Bb]')
			if re.findall(kbQuery, unit):
				#is TB 1000000000000 bytes
				multiplier = 1000
			return multiplier
		
		print strCapacity
		capcityNumberQuery = re.compile('[0-9]')
		capacityMeasureQuery = re.compile('[TtGgMmKk][Bb]')
		capacityNumber = int(''.join(re.findall(capcityNumberQuery, strCapacity)))
		capacityMeasure = ''.join(re.findall(capacityMeasureQuery, strCapacity))
		#now, is it kb, gb or tb?
		bytes = 0
		multiplier = capacityGetMultiplier(capacityMeasure)
		bytes = capacityNumber* multiplier
		bytes = str(bytes)
		print "----done parsedrivecapcacity"
		return bytes
	def parseDriveMedium(string):
		print "------parsemedia"
		ssdQuery = re.compile('([Ss]olid [Ss]tate [Dd]rive)|([Ss][Ss][Dd])')
		medium = re.findall(ssdQuery, string)
		print medium
		mediumType = 'spinning'
		if medium:
			mediumType = 'ssd'
		return mediumType

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
	def lowerString(string):
		return string.lower()
	default_input_processor = Identity()
	default_output_processor = Join()

	driveBytesCapacity_in = MapCompose(capacityStrToBytes)
	driveBytesCapacity_out =TakeFirst()

	driveType_in = MapCompose(lowerString)
	driveType_out = TakeFirst()

	driveMedium_in = MapCompose(parseDriveMedium)
	driveMedium_out = TakeFirst()

