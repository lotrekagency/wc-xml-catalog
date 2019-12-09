import xml.etree.ElementTree as ET
import os
from settings import XML_FEED_FILENAME, XML_SITE_NAME, XML_SITE_HOST, XML_FEED_DESCRIPTION
from utils import switcher_channel, switcher_item, check_for_replace, get_attribute, check_variables

def write_xml(products, language, product_type):
    rss = ET.Element('rss')
    rss.set('version', '2.0')
    rss.set('xmlns:g', 'http://base.google.com/ns/1.0')
    channel = ET.SubElement(rss, 'channel')
    for attribute in switcher_channel:
        item = ET.SubElement(channel, attribute)
        item.text = switcher_channel[attribute]
    for product in products:
        item = ET.SubElement(channel, 'item')
        if product:
            get_switcher_attribute(switcher_item, item, product)
    root = ET.ElementTree(rss)
    os.makedirs('feeds', exist_ok=True)
    root.write('feeds/{0}_{1}_{2}.xml'.format(XML_FEED_FILENAME, language, product_type))
    print(("\033[92m\033[1m[Feed XML] '{0}_{1}_{2}.xml' generated.\033[0m").format(XML_FEED_FILENAME, language, product_type))

def get_switcher_attribute(switcher, item, product):
    for attribute in switcher:
        if 'static' in switcher[attribute]:
            value = check_variables(switcher[attribute]['static'])
            write_xml_attribute(value, item, attribute, switcher[attribute], product)
        if 'attribute' in switcher[attribute]:
            value = switcher[attribute]['attribute']
            write_value = check_for_replace(switcher[attribute], get_attribute(product, value))
            write_xml_attribute(write_value, item, attribute, switcher[attribute], product)
        if 'list' in switcher[attribute]:
            list_element = check_variables(switcher[attribute]['list'])
            for element in list_element:
                product_attribute = ET.SubElement(item, attribute)
                get_switcher_attribute(element, product_attribute, product)

def write_xml_attribute(value, item, attribute, switcher, product):
    if value:
        product_attribute = ET.SubElement(item, attribute)
        product_attribute.text = switcher.get('prefix', '') + str(value) + switcher.get('suffix', '')
    elif not ('logs' in switcher and not switcher['logs']):
        print(("\033[93m[Feed XML] Warning: '{0}' has empty value (product ID {1}).\033[0m").format(attribute, product.id))


