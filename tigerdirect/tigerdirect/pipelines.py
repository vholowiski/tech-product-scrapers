# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

class CategoryPipeline(object):
    #def process_item(self, item, spider):
    #    return item

	def process_category(self, item, spider):
		if item['name']:
			raise DropItem("something somethign item: %s" % item)
		else:
			raise DropItem("Missing price in %s" % item)