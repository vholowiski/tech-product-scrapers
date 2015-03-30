# -*- coding: utf-8 -*-

# Scrapy settings for tigerdirect project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'tigerdirect'

SPIDER_MODULES = ['tigerdirect.spiders']
NEWSPIDER_MODULE = 'tigerdirect.spiders'
DOWNLOAD_DELAY = 0.25
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tigerdirect (+http://www.yourdomain.com)'
ITEM_PIPELINES = { 
	'tigerdirect.pipelines.CategoryPipeline': 600,
	'tigerdirect.pipelines.WriteMongo': 900,
	}