#general libraries
import scrapy
#import re

#item definitions
#from tigerdirect.items import TigerDirectCategory
#from tigerdirect.items import TigerDirectManufacturer

#item loaders
from tigerdirect.spiders.categoryItemLoader import CategoryItemLoader
from tigerdirect.spiders.mfgItemLoader import MfgItemLoader

def test_test():
	print "YAY TEST"
