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
}