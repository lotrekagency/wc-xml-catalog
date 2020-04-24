from settings import XML_SITE_NAME, XML_SITE_HOST, XML_FEED_DESCRIPTION
import settings
import pywoo

XML_SITE_NAME = settings.XML_SITE_NAME
XML_SITE_HOST = settings.XML_SITE_HOST
XML_FEED_DESCRIPTION = settings.XML_FEED_DESCRIPTION
XML_GOOGLE_PRODUCT_CATEGORY = settings.XML_GOOGLE_PRODUCT_CATEGORY

default_shippings = []
tax_rate = None

switcher_channel = {
    'title': XML_SITE_NAME,
    'link' : XML_SITE_HOST,
    'description': XML_FEED_DESCRIPTION
}

def get_shipping_method(method, location):
    method_price = '0'
    if method.settings.get('cost'):
        method_price = getattr(method.settings.get('cost'), 'value')
    shipping_method = {
        'g:country' : {
            'static' : location.code
        },
        'g:service' : {
            'static' : method.method_title
        },
        'g:price' : {
            'static' : method_price,
            'suffix' : ' EUR'
        }
    }
    return shipping_method

def get_default_value(reference_string):
    return globals().get(reference_string, None)
