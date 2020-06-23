import os

WOO_HOST = os.environ.get('WOO_HOST')

#Languages for requests
LANGUAGES = os.environ.get('LANGUAGES', 'it').split(',')

#WooCommerce key credentials
WOO_CONSUMER_KEY = os.environ.get('WOO_CONSUMER_KEY')
WOO_CONSUMER_SECRET = os.environ.get('WOO_CONSUMER_SECRET')

#XML feed fields and settings
XML_FEED_FILENAME = os.environ.get('XML_FEED_FILENAME', 'feedXML')
XML_SITE_NAME = os.environ.get('XML_SITE_NAME')
XML_SITE_HOST = os.environ.get('XML_SITE_HOST')
XML_FEED_DESCRIPTION = os.environ.get('XML_FEED_DESCRIPTION', 'Feed XML autogenerated')
XML_CONFIG_PATH = os.environ.get('XML_CONFIG_PATH', 'config.json')

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')

SENTRY_URL = os.environ.get('SENTRY_URL')

try:
    from local_settings import *
except ImportError:
    pass

if SENTRY_URL:
    import sentry_sdk
    sentry_sdk.init(SENTRY_URL)
