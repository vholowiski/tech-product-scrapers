from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from scrapy.contrib.loader.processor import Identity

import re
import string

class MfgItemLoader(ItemLoader):

	default_input_processor = Identity()
	default_output_processor = Join()

	mfgName_in = TakeFirst()
	mfgName_out = Join()