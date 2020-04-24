import xml.etree.ElementTree as ET
import os
import json
import settings
from settings import XML_FEED_FILENAME, XML_SITE_NAME, XML_SITE_HOST, XML_FEED_DESCRIPTION
import utils
from products import FeedProduct

def write_xml(products, language, product_type):
    rss = ET.Element('rss')
    rss.set('version', '2.0')
    rss.set('xmlns:g', 'http://base.google.com/ns/1.0')
    channel = ET.SubElement(rss, 'channel')
    config = json.load(open(settings.XML_CONFIG_PATH))
    for attribute in utils.switcher_channel:
        item = ET.SubElement(channel, attribute)
        item.text = utils.switcher_channel[attribute]
    for product in products:
        item, is_valid = create_subelement(config[product.type], product)
        if is_valid:
            channel.append(item)
    root = ET.ElementTree(rss)
    os.makedirs('feeds', exist_ok=True)
    root.write('feeds/{0}_{1}_{2}.xml'.format(XML_FEED_FILENAME, language, product_type))
    print(("\033[92m\033[1m[Feed XML] '{0}_{1}_{2}.xml' generated.\033[0m").format(XML_FEED_FILENAME, language, product_type))

def create_subelement(config, product):
    item = ET.Element('item')
    is_valid = get_switcher_attribute(config, item, product)
    return item, is_valid

def get_switcher_attribute(config, item, product):
    is_valid = True
    for attribute in config:
        value, is_valid = product.read_config(config[attribute])
        if not is_valid:
            break
        if value:
            write_xml_attribute(value, item, attribute, product)
    return is_valid

def write_xml_attribute(value, item, attribute, product):
    if isinstance(value, list):
        for element in value:
            main_attribute = ET.SubElement(item, attribute)
            get_switcher_attribute(element, main_attribute, product)
    else:
        product_attribute = ET.SubElement(item, attribute)
        product_attribute.text = value
