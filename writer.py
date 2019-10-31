import xml.etree.ElementTree as ET
from settings import XML_FEED_FILENAME, XML_SITE_NAME, XML_SITE_HOST, XML_FEED_DESCRIPTION
from utils import switcher_channel, switcher_item

def createXML(products):
    rss = ET.Element('rss')
    rss.set('xmlns:g', "http://base.google.com/ns/1.0")
    channel = ET.SubElement(rss, 'channel')
    for attribute in switcher_channel:
        item = ET.SubElement(channel, attribute)
        item.text = switcher_channel[attribute]

    for product in products:
        item = ET.SubElement(channel, 'item')
        for attribute in switcher_item:
            product_attribute = ET.SubElement(item, attribute)
            if hasattr(product, switcher_item[attribute]):
                product_attribute.text = str(product.__getattribute__(switcher_item[attribute]))
            else:
                product_attribute.text = switcher_item[attribute]
    root = ET.ElementTree(rss)
    root.write('feeds/{0}.xml'.format(XML_FEED_FILENAME))