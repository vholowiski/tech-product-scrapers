# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#import json
from scrapy.exceptions import DropItem
import pymongo
from datetime import datetime
#from pymongo import MongoClient
import datetime
from scrapy import log
import json

from scrapy.conf import settings

class manufacturerPipeline(object):
	def process_item(self, item, spider):
		if item["itemType"] == "manufacturer":
			if 'mfgName' in item:
				if 'mfgID' in item:
					return item
			else:
				raise DropItem("incomplete manufacturer" % item)
		else:
			return item

class WriteMongo(object):
	def __init__(self):
		connection = pymongo.Connection(
			settings['MONGODB_SERVER'],
			settings['MONGODB_PORT']
		)
		self.db = connection[settings['MONGODB_DB']]

	def process_item(self, item, spider):
		if item:

			#if it's a manufacturer, save to mongo, or update
			if (item['itemType'] == "manufacturer") or (item['itemType'] == 'category') or (item['itemType'] == 'product'):
				seenAt = datetime.datetime.utcnow()
				#convert scrapy item to dict
				mfg = dict(item)
				mfg['firstSeen'] = seenAt
				mfg['lastSeen'] = seenAt

				log.msg("item converted to dict", level=log.DEBUG, spider=spider)

				#select the collection
				colname = "td_" + item['itemType']
				print item['itemType']
				print colname
				collection = self.db[colname]
				
				#check if the mfg exists
				if item['itemType'] == "manufacturer":
					mfgID = item['mfgID']
					foundMFG = collection.find_one({'mfgID': mfgID})
					if foundMFG:
						#lastSeen = datetime.datetime.utcnow()
						foundMFG['lastSeen'] = seenAt
						collection.save(foundMFG)
						print "Updated manufacturer"
					else:
						result = collection.insert(mfg)
						print "Added new manufacturer"
				if item['itemType'] == 'category':
					tdCategoryID = item['tdCategoryID']
					foundCategory = collection.find_one({'tdCategoryID': tdCategoryID})
					if foundCategory:
						#lastSeen = datetime.datetime.utcnow()
						foundCategory['lastSeen'] = seenAt
						collection.save(foundCategory)
						print "Updated category"
					else:
						result = collection.insert(mfg)
						print "Added new category"
				if item['itemType'] == 'product':
					#TODO: special case for product, to update category and url arrays
					tdItemNo = item['itemNo']
					foundItem = collection.find_one({'itemNo': tdItemNo})
					if foundItem:
						#lastSeen = datetime.datetime.utcnow()
						foundItem['lastSeen'] = seenAt
						collection.save(foundItem)
						print "Updated item"
					else:
						result = collection.insert(mfg)
						print "Added new item"

			if item['itemType'] == 'price':
				price = dict(item)
				seenAt = datetime.datetime.utcnow()
				price['seenAt'] = seenAt
				collection = self.db['td_price']
				result = collection.insert(price)
				if result:
					print "Saved Price"
				else:
					print "FAILED to save price"

			#if it's a item, save or update
			#if item['itemType'] == product:

#class JsonWriterPipeline(object):
#	def __init__(self):
#		self.file = open('items.jl', 'wb')
#	def process_item(self, item, spider):
#		line = json.dumps(dict(item)) + "\n"
#		self.file.write(line)
#		return item


#if hasattr(item, 'type'):
#	#if item['type'] == 'product':
#	print "yup"
#		#raise DropItem("something somethign item: %s" % item)
#	#else:
#		#print "nope"
#		#raise DropItem("Missing price in %s" % item)