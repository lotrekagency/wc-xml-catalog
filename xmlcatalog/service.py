import json
from pywoo import Api
from settings import REDIS_HOST, LANGUAGES, WOO_HOST, WOO_CONSUMER_KEY, WOO_CONSUMER_SECRET, XML_FEED_FILENAME
from utils import get_conf_attribute, fetch_switchers, get_shipping_method, methods_list
from huey import RedisHuey, crontab
from writer import write_xml

huey = RedisHuey('feedXML', host=REDIS_HOST)
try:
    fetch_switchers(json.load(open('../config/mapping.json')))
except:
    fetch_switchers(json.load(open('../default_mapping.json')))
try:
    conf = json.load(open('../config/config.json'))
except:
    conf = json.load(open('../default_config.json'))
    
api = Api(WOO_HOST, WOO_CONSUMER_KEY, WOO_CONSUMER_SECRET, console_logs=False)

def apply_conf(obj, obj_fields, conf_path):
    if 'attributes' in conf[conf_path]:
        attributes = conf[conf_path]['attributes']
        for attribute in attributes:
            if 'attribute' in attributes[attribute]:
                value = get_conf_attribute(attributes[attribute]['attribute'], obj, obj_fields)
                setattr(obj, attribute, value)
            if 'fatal' in attributes[attribute] and attributes[attribute]['fatal']:
                if not getattr(obj, attribute):
                    return None
    return obj

@huey.periodic_task(crontab(hour="*/7"))
def createXML(api):
    print("\033[95m[Feed XML] Getting shipping methods...\033[0m")
    methods_list.clear()
    shipping_zones = api.get_shipping_zones()
    for zone in shipping_zones:
        zone_locations = api.get_shipping_zone_locations(shipping_zone_id=zone.id)
        zone_methods = api.get_shipping_zone_methods(shipping_zone_id=zone.id)
        for location in zone_locations:
            for method in zone_methods:
                methods_list.append(get_shipping_method(method, location))
    for language in LANGUAGES:
        print(("\033[95m[Feed XML] Getting products for language '{0}'...\033[0m").format(language))
        products = []
        variations = []
        page_index = 1
        products_request = api.get_products(lang=language, page=page_index)
        while products_request:
            for product in products_request:
                obj = apply_conf(product, None, 'products')
                if obj:
                    products.append(obj)
            page_index += 1
            products_request = api.get_products(lang=language, page=page_index)
        print(("\033[95m[Feed XML] Generating '{0}_{1}_products.xml'...\033[0m").format(XML_FEED_FILENAME, language))
        write_xml(products, language, 'products')
        print(("\033[95m[Feed XML] Getting variations for language '{0}'...\033[0m").format(language))
        for product in products:
            if product:
                product_variations = api.get_product_variations(product_id=product.id, lang=language, per_page=100)
                for product_variation in product_variations:
                    obj = apply_conf(api.get_products(id=product_variation.id), product, 'variations')
                    if obj:
                        variations.append(obj)
        print(("\033[95m[Feed XML] Generating '{0}_{1}_variations.xml'...\033[0m").format(XML_FEED_FILENAME, language))
        write_xml(variations, language, 'variations')