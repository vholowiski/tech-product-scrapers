# -*- coding: utf-8 -*-

# Scrapy settings for tigerdirect project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'

SPIDER_MODULES = ['tigerdirect.spiders']
NEWSPIDER_MODULE = 'tigerdirect.spiders'
DOWNLOAD_DELAY = 0.32
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tigerdirect (+http://www.yourdomain.com)'

ITEM_PIPELINES = { 
 	'tigerdirect.pipelines.manufacturerPipeline': 500,
 	'tigerdirect.pipelines.WriteMongo': 900,
 	}

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "techProducts_development"
MONGODB_COLLECTION = "stuff"