#general libraries
import scrapy
import re

#item definitions
from tigerdirect.items import TigerdirectItem
from tigerdirect.items import SpecificationsItem
from tigerdirect.items import PriceItem


#item loaders
from tigerdirect.spiders.itemItemLoader import ItemItemLoader
from tigerdirect.spiders.priceItemLoader import PriceItemLoader
from tigerdirect.spiders.specificationItemLoader import SpecificationItemLoader

def parse_items(self, response):
	print "parse_items - begin"
        #print("**********************")
        l = ItemItemLoader(TigerdirectItem(), response)
        item = TigerdirectItem()
        l.add_value('itemType', 'product')
        l.add_value('crawlTimestamp', unicode(time.time()))
        l.add_value('source', 'www.tigerdirect.ca')
        l.add_xpath('productName', ('//div[@class="prodName"]/h1/text()'))
        l.add_value('itemNo', response.xpath('//div[@class="prodName"]/span[@class="sku"]/text()')[0].extract())
        l.add_value('modelNo', response.xpath('//div[@class="prodName"]/span[@class="sku"]/text()')[1].extract())
        l.add_value('tdCategoryID', response.url)
        l.add_value('link', response.url)

        itemItem = TigerdirectItem(l.load_item())
        yield itemItem

        l = PriceItemLoader(PriceItem(), response)
        l.add_value('_td_priceBox', response.xpath('//dl[@class="priceBox"]').extract())

        #pricing['itemType'] = 'price'
        l.add_value('itemType', 'price')

        pricing = PriceItem()

        l.add_xpath('salePrice', ('//dd[contains(@class, "salePrice")]/descendant::*/text()'))
        l.add_xpath('rebateAmount', ('//dd[contains(@class, "priceRebate")]/text()'))

        l.add_value('finalPrice', response.xpath('//dd[contains(@class, "priceFinal")]').extract())
        l.add_value('purchaseURL', response.url)
        #l.add_value('crawlTimestamp', time.time())
        l.add_value('source', 'wwww.tigerdirect.ca')

        l.add_value('itemID', itemItem['itemNo'])
        #l.addx('itemMongoID', bot)

        #TODO get price for 'add to car to see price'
        #http://www.tigerdirect.ca/applications/SearchTools/item-details.asp?CatId=5739&EdpNo=9641093
        #its in the javascript!

        priceItem = PriceItem(l.load_item())
        priceItem['crawlTimestamp']=time.time()
        yield priceItem

        #some ssd drives:
        #http://www.tigerdirect.ca/applications/SearchTools/item-details.asp?EdpNo=9099634&Sku=KIN-102513377
        #http://www.tigerdirect.ca/applications/SearchTools/item-details.asp?EdpNo=9640807&Sku=KNY-102878750
        #specifications?
        hasSpecifications = response.xpath('//span[contains(text(), "pecifications")]')
        if hasSpecifications:
                l = SpecificationItemLoader(SpecificationsItem(), response)
                l.add_value('itemID', itemItem['itemNo'])
                l.add_value('itemType', 'specifications')
                #get the keys (specificatin types) in the table
                specKeys = response.xpath('//table[contains(@class, "prodSpec")]/tbody/tr/th/text()')
                #print "found this many spec keys:"
                #print len(specKeys)
                #first recognize canonical specs
                i = 0
                genericSpecs = [] #set up an empty array for specs not canonical
                if len(specKeys) > 0:
                        for key in specKeys:
                                canonicalKeyFound = False
                                valueArray = response.xpath('//table[contains(@class, "prodSpec")]/tbody/tr/td/text()')
                                if valueArray:
                                        value = valueArray[i]
                                        #value = response.xpath('//table[contains(@class, "prodSpec")]/tbody/tr/td/text()')[i]
                                        key = key.extract()
                                        value = value.extract()

                                        #cleanKeyQuery = re.compile('[A-Za-z0-9 .-]')
                                        cleanKeyQuery = re.compile('[A-Za-z0-9 ]') #note- period and dash not allowed in key!
                                        cleanValueQuery = re.compile('[A-Za-z0-9 .",\'!-]')
                                        cleanKey = ''.join(re.findall(cleanKeyQuery, key))
                                        cleanValue = ''.join(re.findall(cleanValueQuery, value))

                                        #now, look for canonical
                                        #capacity, in bytes
                                        capacityQuery = re.compile('[Cc]apacity$')
                                        if re.findall(capacityQuery, cleanKey):
                                                l.add_value('driveBytesCapacity', cleanValue)
                                                canonicalKeyFound = True
                                        #internal, external?
                                        driveTypeQuery = re.compile('[Dd]rive [Tt]ype')
                                        if re.findall(driveTypeQuery, cleanKey):
                                                l.add_value('driveType', cleanValue)
                                                canonicalKeyFound = True
                                        #ssd or spinning?
                                        prodName = response.xpath('//div[@class="prodName"]/h1/text()').extract()[0]
                                        #TODO: Instead of searching for 'ssd' i shoud just be checking if this is a hard drive
                                                #and then setting it to ssd or spinning
                                                #but i need to build a function for that
                                                #for now, no ssd means its spinning
                                        ssdQuery = re.compile('([Ss]olid *[Ss]tate *[Dd]rive)|([Ss][Ss][Dd])')
                                        ssdQueryResult = re.findall(ssdQuery, prodName)
                                        if ssdQueryResult:
                                                #print "-----inside ssdQueryResult"
                                                #print ssdQueryResult[0]
                                                l.add_value('driveMedium', ssdQueryResult[0])
                                                #print "----after addv_value"
                                                #print l
                                                #l.add_xpath('driveMedium', ('([Ss]olid [Ss]tate [Dd]rive)|([Ss][Ss][Dd])'))
                                                canonicalKeyFound = True

                                        i = i + 1
                                        if not canonicalKeyFound:
                                                addSpec = {cleanKey: cleanValue}
                                                genericSpecs +=[addSpec]
        #print "----about to load SpecificationsItem"
        #print l["driveMedium"]
        itemSpecifications = SpecificationsItem(l.load_item())
        itemSpecifications['genericSpecs'] = genericSpecs
        yield itemSpecifications
        #yield itemSpecifications
        #then create the item
        #then loop through the rest, and create them as non canonical
