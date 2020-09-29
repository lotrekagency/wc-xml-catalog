import xml.etree.ElementTree as ET
import os
import settings
from settings import XML_FEED_FILENAME, XML_SITE_NAME, XML_SITE_HOST, XML_FEED_DESCRIPTION
import utils
from products import FeedProduct

def write_xml(products, languages, filename, config):
    rss = ET.Element('rss')
    rss.set('version', '2.0')
    rss.set('xmlns:g', 'http://base.google.com/ns/1.0')
    channel = ET.SubElement(rss, 'channel')
    for attribute in utils.switcher_channel:
        item = ET.SubElement(channel, attribute)
        item.text = utils.switcher_channel[attribute]
    for product in products:
        product_dict = product.parse_dict(config[product.type])
        fill_item(product_dict, channel)
    root = ET.ElementTree(rss)
    path_list = ['feeds'] + filename
    path_list_directory = ('/'.join(path_list[:-1]))
    os.makedirs(path_list_directory, exist_ok=True)
    root.write('%s/%s_%s_%s.xml' % (path_list_directory, XML_FEED_FILENAME, ('_').join(languages), path_list[-1]))
    print(("\033[92m\033[1m[Feed XML] '%s/%s_%s_%s.xml' generated.\033[0m") % (path_list_directory, XML_FEED_FILENAME, ('_').join(languages), path_list[-1]))

def fill_item(config, parent, key='item'):
    item = ET.Element(key)
    if isinstance(config, dict):
        for tag in config.keys():
            fill_item(config[tag], item, tag)
    elif isinstance(config, list):
        for config_element in config:
            fill_item(config_element, parent, key)
    else:
        item.text = config
    if len(item) or item.text:
        parent.append(item)
