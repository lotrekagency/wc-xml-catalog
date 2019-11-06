import settings
import pywoo

switcher_channel = {
    'title': settings.XML_SITE_NAME,
    'link' : settings.XML_SITE_HOST,
    'description': settings.XML_FEED_DESCRIPTION
}
switcher_item = {
    'g:brand' : settings.XML_SITE_NAME,
    'g:id' : 'id',
    'g:title' : 'name',
    'g:description' : 'description',
    'g:link' : 'permalink',
    'g:image_link' : 'images',
    'g:availability' : 'stock_status',
    'g:price' : 'price',
    'g:condition': 'New',
    'g:shipping' : [],
    'g:sale_price' : 'sale_price',
    'g:identifier_exists' : 'yes'
}

def addStaticDict(dict_key, static_dict):
    switcher_item[dict_key].append(static_dict)

def checkStrings(text, attribute):
    if(attribute == 'g:price'):
        return text + ' EUR'
    else:
        if isinstance(text, list) and text and isinstance(text[0], pywoo.models.products.ProductImage):
            return text[0].src
    return text