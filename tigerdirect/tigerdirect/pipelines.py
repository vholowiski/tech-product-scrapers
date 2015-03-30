# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#import json
from scrapy.exceptions import DropItem
#from pymongo import MongoClient
import datetime
from scrapy import log
import json

class CategoryPipeline(object):
    #def process_item(self, item, spider):
    #    return item

	def process_item(self, item, spider):
		#if item:
		#	if hasattr(item, 'id'):
		#		item['id'] = 'shazbot'
		#	return item
		#else:
		#	raise DropItem("Shitballs. Did nto get item.")
		return item

class WriteMongo(object):
	def process_item(self, item, spider):
		if item:
			#mongo stuff
			client = MongoClient('mongodb://localhost:27017/')
			if client:
				db = client.techProducts
				if db:
					collection = db.tigerDirect
					if collection:
						post = dict(item)
						#post = json.dumps(dict(item))
						#post = dict('itemType': 'manufacturer', 'mfgID': '7488', 'mfgName': 'Allure')
						#post = dict(one=1, two=2, three=3)
						log.msg("item converted to dict", level=log.DEBUG, spider=spider)
						#log.msg(post, level=log.DEBUG, spider=spider)
						collection.insert(post)
						#end mongo stuff
		return item

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