from bottle import run, route
from pywoo import Api
from writer import createXML
from settings import WOO_HOST, WOO_CONSUMER_KEY, WOO_CONSUMER_SECRET

api = Api(WOO_HOST, WOO_CONSUMER_KEY, WOO_CONSUMER_SECRET)

products = api.get_products(lang='en')
createXML(products)
print(products)
for product in products:
    print(product.name)
