import settings

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
    'g:image_link' : '',
    'g:availability' : 'stock_status',
    'g:price' : 'price',
    'g:condition': 'New',
    'g:shipping' : [],
    'g:sale_price' : 'sale_price',
    'g:identifier_exists' : 'yes'
}

def addStaticDict(dict_key, static_dict):
    switcher_item[dict_key].append(static_dict)

def checkForGoogleRules(text, attribute):
    if(attribute == 'g:price'):
        return 'EUR ' + text
    return text