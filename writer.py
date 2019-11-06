import xml.etree.ElementTree as ET
from settings import XML_FEED_FILENAME, XML_SITE_NAME, XML_SITE_HOST, XML_FEED_DESCRIPTION
from utils import switcher_channel, switcher_item, checkStrings

def writeXML(products):
    rss = ET.Element('rss')
    rss.set('xmlns:g', "http://base.google.com/ns/1.0")
    channel = ET.SubElement(rss, 'channel')
    for attribute in switcher_channel:
        item = ET.SubElement(channel, attribute)
        item.text = switcher_channel[attribute]
    for product in products:
        item = ET.SubElement(channel, 'item')
        getSwitcherAttribute(switcher_item, item, product)
    root = ET.ElementTree(rss)
    root.write('feeds/{0}.xml'.format(XML_FEED_FILENAME))

def getSwitcherAttribute(switcher, item, product):
    for attribute in switcher:
        if isinstance(switcher[attribute], list):
            for nested_dict in switcher[attribute]:
                product_attribute = ET.SubElement(item, attribute)
                getSwitcherAttribute(nested_dict, product_attribute, product)
        else:
            product_attribute = ET.SubElement(item, attribute)
            if hasattr(product, switcher[attribute]):
                if str(getattr(product, switcher[attribute])):
                    product_attribute.text = str(checkStrings(getattr(product, switcher[attribute]), attribute))
                else:
                    item.remove(product_attribute)
            else:
                product_attribute.text = switcher[attribute]
