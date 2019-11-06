from bottle import run, route
from pywoo import Api
from writer import writeXML
from settings import WOO_HOST, WOO_CONSUMER_KEY, WOO_CONSUMER_SECRET
from utils import addStaticDict

api = Api(WOO_HOST, WOO_CONSUMER_KEY, WOO_CONSUMER_SECRET)
 
products = api.get_products(lang='en')
shipping_zones = api.get_shipping_zones()
for zone in shipping_zones:
    zone_locations = api.get_shipping_zone_locations(shipping_zone_id=zone.id)
    zone_methods = api.get_shipping_zone_methods(shipping_zone_id=zone.id)
    for location in zone_locations:
        for method in zone_methods:
            method_price = '0'
            if 'cost' in method.settings.keys():
                method_price = getattr(method.settings['cost'], 'value')
            shipping_dict = {
                'g:country' : location.code,
                'g:service' : method.method_title,
                'g:price' : method_price + ' EUR'
            }
            addStaticDict('g:shipping', shipping_dict)
writeXML(products)