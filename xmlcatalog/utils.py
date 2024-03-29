from settings import XML_SITE_NAME, XML_SITE_HOST, XML_FEED_DESCRIPTION
import settings
import pywoo

XML_SITE_NAME = settings.XML_SITE_NAME
XML_SITE_HOST = settings.XML_SITE_HOST
XML_FEED_DESCRIPTION = settings.XML_FEED_DESCRIPTION

default_shippings = []
default_tax_rates = []
current_language = ''
current_tax_rate = None

switcher_channel = {
    'title': XML_SITE_NAME,
    'link' : XML_SITE_HOST,
    'description': XML_FEED_DESCRIPTION
}

def get_shipping_method(method, location):
    method_price = '0'
    if method.settings.get('cost'):
        method_price = getattr(method.settings.get('cost'), 'value')
        if isinstance(method_price, str):
            method_price = method_price.replace(',', '.')
    shipping_method = {
        'g:country' : location.code,
        'g:service' : method.method_title,
        'g:price' : '{0:.2f} EUR'.format(float(method_price))
    }
    return shipping_method

def set_tax_rates(rates):
    for rate in rates:
        default_tax_rates.append(
            {
                'g:country' : rate.country,
                'g:rate' : rate.rate,
                'g:tax_ship' : 'yes' if rate.shipping else 'no'
            }
        )

def get_default_value(reference_string):
    return globals().get(reference_string, None)
