# -*- coding: utf-8 -*-

# Scrapy settings for newegg_ca project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'

SPIDER_MODULES = ['newegg_ca.spiders']
NEWSPIDER_MODULE = 'newegg_ca.spiders'
DOWNLOAD_DELAY = 0.82

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'newegg_ca (+http://www.yourdomain.com)'
