from pywoo import Api
from writer import write_xml
from settings import REDIS_HOST, LANGUAGES, WOO_HOST, WOO_CONSUMER_KEY, WOO_CONSUMER_SECRET, XML_FEED_FILENAME
from utils import getShippingMethod, methods_list
from huey import RedisHuey, crontab

huey = RedisHuey('feedXML', host=REDIS_HOST)
api = Api(WOO_HOST, WOO_CONSUMER_KEY, WOO_CONSUMER_SECRET, console_logs=False)

@huey.periodic_task(crontab(hour="*/7"))
def createXML():
    print("\033[95m[Feed XML] Getting shipping methods...\033[0m")
    methods_list.clear()
    shipping_zones = api.get_shipping_zones()
    for zone in shipping_zones:
        zone_locations = api.get_shipping_zone_locations(shipping_zone_id=zone.id)
        zone_methods = api.get_shipping_zone_methods(shipping_zone_id=zone.id)
        for location in zone_locations:
            for method in zone_methods:
                methods_list.append(getShippingMethod(method, location))
    for language in LANGUAGES:
        print(("\033[95m[Feed XML] Getting products for language '{0}'...\033[0m").format(language))
        products_list = []
        products = api.get_products(lang=language)
        print(("\033[95m[Feed XML] Generating '{0}_{1}_products.xml'...\033[0m").format(XML_FEED_FILENAME, language))
        write_xml(products, language, 'products')
        print(("\033[95m[Feed XML] Getting variations for language '{0}'...\033[0m").format(language))
        for product in products:
            product_variations = api.get_product_variations(product_id=product.id, lang=language)
            for product_variation in product_variations:
                obj = api.get_products(id=product_variation.id)
                setattr(obj, 'parent_id', product.id)
                obj.short_description = product.short_description
                products_list.append(obj)
        print(("\033[95m[Feed XML] Generating '{0}_{1}_variations.xml'...\033[0m").format(XML_FEED_FILENAME, language))
        write_xml(products_list, language, 'variations')

