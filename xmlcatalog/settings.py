import os

WOO_HOST = os.environ.get('WOO_HOST')

#Languages for requests
LANGUAGES = os.environ.get('LANGUAGES', 'it').split(',')

#WooCommerce key credentials
WOO_CONSUMER_KEY = os.environ.get('WOO_CONSUMER_KEY')
WOO_CONSUMER_SECRET = os.environ.get('WOO_CONSUMER_SECRET')

#Types of products displayed in products and variations file
XML_TYPES_IN_PRODUCTS = os.environ.get('XML_TYPES_IN_PRODUCTS', 'variable').split(',')
XML_TYPES_IN_VARIATIONS = os.environ.get('XML_TYPES_IN_VARIATIONS', 'variation').split(',')

#XML feed fields and settings
XML_FEED_FILENAME = os.environ.get('XML_FEED_FILENAME', 'feedXML')
XML_SITE_NAME = os.environ.get('XML_SITE_NAME')
XML_SITE_HOST = os.environ.get('XML_SITE_HOST')
XML_FEED_DESCRIPTION = os.environ.get('XML_FEED_DESCRIPTION', 'Feed XML autogenerated')
XML_GOOGLE_PRODUCT_CATEGORY = os.environ.get('XML_GOOGLE_PRODUCT_CATEGORY')
XML_CONFIG_PATH = os.environ.get('XML_CONFIG_PATH', 'config.json')
XML_USE_TAXES = os.environ.get('XML_USE_TAXES', False)

if isinstance(XML_USE_TAXES, str):
    if XML_USE_TAXES.lower() == 'true':
        XML_USE_TAXES = True
    elif XML_USE_TAXES.lower() == 'false':
        XML_USE_TAXES = False
    else:
        XML_USE_TAXES = None

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')

try:
    from local_settings import *
except ImportError:
    pass
