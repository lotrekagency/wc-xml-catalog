import xml.etree.ElementTree as ET
import os
from settings import XML_FEED_FILENAME, XML_SITE_NAME, XML_SITE_HOST, XML_FEED_DESCRIPTION
from utils import switcher_channel, switcher_item, split_path, get_index

current_product_id = ''

def write_xml(products, language):
    rss = ET.Element('rss')
    rss.set('version', '2.0')
    rss.set('xmlns:g', 'http://base.google.com/ns/1.0')
    channel = ET.SubElement(rss, 'channel')

    for attribute in switcher_channel:
        item = ET.SubElement(channel, attribute)
        item.text = switcher_channel[attribute]
    for product in products:
        item = ET.SubElement(channel, 'item')
        get_switcher_attribute(switcher_item, item, product)
    root = ET.ElementTree(rss)
    os.makedirs('feeds', exist_ok=True)
    root.write('feeds/{0}_{1}.xml'.format(XML_FEED_FILENAME, language))
    print(("\033[95m\033[1m[Feed XML] '{0}_{1}.xml' generated.\033[0m").format(XML_FEED_FILENAME, language))

def get_switcher_attribute(switcher, item, product):
    for attribute in switcher:
        if 'static' in switcher[attribute]:
            value = switcher[attribute]['static']
            write_xml_attribute(value, item, attribute, switcher[attribute], product)
        if 'attribute' in switcher[attribute]:
            value = switcher[attribute]['attribute']
            if 'path' in switcher[attribute]:
                value = getattr(get_path(product, switcher[attribute]['path']), value)
                write_xml_attribute(value, item, attribute, switcher[attribute], product)
            elif hasattr(product, value):
                write_xml_attribute(getattr(product, value), item, attribute, switcher[attribute], product)
        if 'list' in switcher[attribute]:
            for element in switcher[attribute]['list']:
                product_attribute = ET.SubElement(item, attribute)
                get_switcher_attribute(element, product_attribute, product)

def write_xml_attribute(value, item, attribute, switcher, product):
    if value:
        product_attribute = ET.SubElement(item, attribute)
        product_attribute.text = switcher.get('prefix', '') + str(value) + switcher.get('suffix', '')
    elif not ('logs' in switcher and not switcher['logs']):
        print(("\033[91m[Feed XML] Error: '{0}' has empty value (product ID {1}).\033[0m").format(attribute, product.id))

def get_path(current_location, path):
    attribute, index = get_index(path)
    if index:
        return getattr(current_location, attribute)[int(index)]
    return attribute
