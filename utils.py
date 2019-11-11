import settings
import pywoo

methods_list = []

switcher_channel = {
    'title': settings.XML_SITE_NAME,
    'link' : settings.XML_SITE_HOST,
    'description': settings.XML_FEED_DESCRIPTION
}

switcher_item = {
    'g:brand' : {
        'static' : settings.XML_SITE_NAME
    },
    'g:id' : {
        'attribute' : 'id'
    },
    'g:title' : {
        'attribute' : 'name'
    },
    'g:description' : {
        'attribute' : 'description' 
    },
    'g:link' : {
        'attribute' : 'permalink'
    },
    'g:image_link' : {
        'path' : 'images[0]',
        'attribute' : 'src'
    },
    'g:google_product_category' : {
        'static' : settings.XML_GOOGLE_PRODUCT_CATEGORY
    },
    'g:availability' : {
        'attribute' : 'stock_status'
    },
    'g:mpn' : {
        'attribute' : 'sku'
    },
    'g:price' : {
        'attribute' : 'price',
        'suffix' : ' EUR'
    },
    'g:condition': {
        'static' : 'New'
    },
    'g:shipping' : {
        'list' : methods_list
    },
    'g:sale_price' : {
        'attribute' : 'sale_price',
        'optional' : True
    },
    'g:identifier_exists' : {
        'static' : 'yes'
    }
}

def getShippingMethod(method, location):
    method_price = '0'
    if 'cost' in method.settings.keys():
        method_price = getattr(method.settings['cost'], 'value')
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

def split_path(path):
    path_splitted = path.split('.')
    return path_splitted if path_splitted else path

def get_index(path):
    path_splitted = path.replace(']', '[').split('[')
    if isinstance(path_splitted, list):
        return path_splitted[0], path_splitted[-2]
    else:
        return path_splitted, None

