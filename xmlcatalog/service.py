import json
import settings
import utils
import requests_cache
from pywoo import Api
from writer import write_xml
from products import FeedProduct

requests_cache.install_cache('pywoo_cache', backend='sqlite')


def get_products(api, language, products=[], page=1):
    current_products = [FeedProduct(product, language) for product in api.get_products(lang=language, page=page, status=settings.PRODUCTS_STATUS_CODE)]
    if not current_products:
        return products
    return get_products(api, language, (products + current_products), (page + 1))

def get_product_variations(api, language, product_id, variations=[], page=1):
    current_variations = api.get_product_variations(product_id=product_id, lang=language, page=page, status=settings.PRODUCTS_STATUS_CODE)
    if not current_variations:
        return variations
    return get_product_variations(api, language, product_id, (variations + current_variations), (page + 1))

def get_variations(api, language, products, variations=[]):
    for product in products:
        product_variations = get_product_variations(api, language, product.id)
        for variation in product_variations:
            variations.append(FeedProduct(api.get_products(id=variation.id), language, product))
    return variations

def get_tax_rates(api, tax_rates=[], page=1):
    current_tax_rates = api.get_tax_rates(page=page)
    if not current_tax_rates:
        utils.set_tax_rates(tax_rates)
        return tax_rates
    return get_tax_rates(api, (tax_rates + current_tax_rates), (page + 1))

def get_products_and_variations(api, language):
    products = get_products(api, language)
    variations = get_variations(api, language, products)
    return products + variations

def create_xml():
    requests_cache.clear()
    api = Api(settings.WOO_HOST, settings.WOO_CONSUMER_KEY, settings.WOO_CONSUMER_SECRET, console_logs=False)
    config = json.load(open(settings.XML_CONFIG_FILENAME))
    print("\033[95m[Feed XML] Getting shipping methods...\033[0m")
    utils.default_shippings.clear()
    utils.default_tax_rates.clear()
    shipping_zones = api.get_shipping_zones()
    for zone in shipping_zones:
        zone_locations = api.get_shipping_zone_locations(shipping_zone_id=zone.id)
        zone_methods = api.get_shipping_zone_methods(shipping_zone_id=zone.id)
        for location in zone_locations:
            for method in zone_methods:
                utils.default_shippings.append(utils.get_shipping_method(method, location))
    print("\033[95m[Feed XML] Getting tax rates...\033[0m")
    taxes = get_tax_rates(api)
    for config_file_name, config_file  in config.items():
        config_file_languages = config_file.get('languages')
        config_file_types = config_file.get('types')

        if config_file_languages and config_file_types:
            for language_file, languages_in_file in config_file_languages.items():
                languages_in_file = [languages_in_file] if not isinstance(languages_in_file, list) else languages_in_file

                elements = []
                for language in languages_in_file:
                    print(("\033[95m[Feed XML] Getting products in language '%s'...\033[0m") % language)
                    elements.extend(get_products_and_variations(api, language))

                config_file_path = config_file_name.split('/')
                config_file_directory = ('/').join(['feeds'] + config_file_path[:-1])
                print(("\033[95m[Feed XML] Generating '%s/%s_%s_%s.xml'...\033[0m") % (config_file_directory, settings.XML_FEED_FILENAME, ('_').join(languages_in_file), config_file_path[-1]))
                selected_products = filter(lambda product: product.type in config_file_types.keys(), elements)
                write_xml(selected_products, languages_in_file, config_file_path, config_file_types)
    
    elements.clear()