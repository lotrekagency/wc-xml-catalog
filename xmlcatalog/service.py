import json
from pywoo import Api
import settings
import utils
from writer import write_xml
from products import FeedProduct

def get_products(api, language, products=[], page=1):
    current_products = [FeedProduct(product) for product in api.get_products(lang=language, page=page)]
    if not current_products:
        return products
    return get_products(api, language, (products + current_products), (page + 1))

def get_product_variations(api, language, product_id, variations=[], page=1):
    current_variations = api.get_product_variations(product_id=product_id, lang=language, page=page)
    if not current_variations:
        return variations
    return get_product_variations(api, language, product_id, (variations + current_variations), (page + 1))

def get_variations(api, language, products, variations=[]):
    for product in products:
        product_variations = get_product_variations(api, language, product.id)
        for variation in product_variations:
            variations.append(FeedProduct(api.get_products(id=variation.id), product))
    return variations

def get_tax_rates(api, tax_rates=[], page=1):
    current_tax_rates = api.get_tax_rates(page=page)
    if not current_tax_rates:
        utils.set_tax_rates(tax_rates)
        return tax_rates
    return get_tax_rates(api, (tax_rates + current_tax_rates), (page + 1))

def create_xml():
    api = Api(settings.WOO_HOST, settings.WOO_CONSUMER_KEY, settings.WOO_CONSUMER_SECRET, console_logs=False)
    print("\033[95m[Feed XML] Getting shipping methods...\033[0m")
    utils.default_shippings.clear()
    shipping_zones = api.get_shipping_zones()
    for zone in shipping_zones:
        zone_locations = api.get_shipping_zone_locations(shipping_zone_id=zone.id)
        zone_methods = api.get_shipping_zone_methods(shipping_zone_id=zone.id)
        for location in zone_locations:
            for method in zone_methods:
                utils.default_shippings.append(utils.get_shipping_method(method, location))
    print("\033[95m[Feed XML] Getting tax rates...\033[0m")
    get_tax_rates(api)
    for language in settings.LANGUAGES:
        print(("\033[95m[Feed XML] Getting products for language '{0}'...\033[0m").format(language))
        products = get_products(api, language)
        print(("\033[95m[Feed XML] Getting variations for language '{0}'...\033[0m").format(language))
        variations = get_variations(api, language, products)
        products = products + variations

        print(("\033[95m[Feed XML] Generating '{0}_{1}_products.xml'...\033[0m").format(settings.XML_FEED_FILENAME, language))
        selected_products = filter(lambda product: product.type in settings.XML_TYPES_IN_PRODUCTS, products)
        write_xml(selected_products, language, 'products')
        print(("\033[95m[Feed XML] Generating '{0}_{1}_variations.xml'...\033[0m").format(settings.XML_FEED_FILENAME, language))
        selected_variations = filter(lambda product: product.type in settings.XML_TYPES_IN_VARIATIONS, products)
        write_xml(selected_variations, language, 'variations')

        products.clear()
        variations.clear()
