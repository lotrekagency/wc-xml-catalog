from settings import XML_SITE_NAME, XML_SITE_HOST, XML_FEED_DESCRIPTION
import pywoo

methods_list = []

switcher_channel = {
    'title': XML_SITE_NAME,
    'link' : XML_SITE_HOST,
    'description': XML_FEED_DESCRIPTION
}

switcher_google = {}

switcher_item = {}

def get_shipping_method(method, location):
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
    path_splitted = path
    if ']' in path:
        path_splitted = path_splitted.replace(']', '[').split('[')
    if isinstance(path_splitted, list):
        return path_splitted[0], path_splitted[-2]
    else:
        return path_splitted, None

def check_for_path(switcher, product):
    if 'path' in switcher:
        return get_path(product, switcher['path'])
    else:
        return product

def check_for_replace(switcher, value):
    if 'replace' in switcher:
        switcher_replace = check_variables(switcher['replace'])
        if str(value) in switcher_replace:           
            return switcher_replace[str(value)]
        return ''
    return value

def check_path_conditions(path):
    if ']' in path or '(' in path:
        return True
    return False

def get_path_by_condition(current_location, path):
    if ']' in path:
        path_splitted = path.replace(']', '[').split('[')
        return getattr(current_location, path_splitted[0])[int(path_splitted[-2])]
    if '(' in path:
        path_splitted = path.replace(')', '(').split('(')
        attribute = path_splitted[0]
        condition = path_splitted[-2]
        if '=' in condition:
            condition_splitted = condition.split('=')
            key = condition_splitted[0]
            value = condition_splitted[-1]
            current_location = get_attribute(current_location, attribute)
            if isinstance(current_location, list):
                for obj in current_location:
                    if obj.get(key, None) == value:
                        return obj
            return None

def get_path(current_location, path):
    if check_path_conditions(path):
        return get_path_by_condition(current_location, path)
    return getattr(current_location, path)

def get_attribute(path, value, separator=''):
    return_value = None
    if isinstance(path, dict):
        return_value = path.get(value, None)
    elif isinstance(path, list):
        return_value = str(get_attribute(path[0], value))
        for path_element in path[1:]:
            return_value = str(return_value) + separator + str(get_attribute(path_element, value))
    elif hasattr(path, value):
        return_value = getattr(path, value)
    return return_value
                            
def get_reference(reference_string):
    if '.' in reference_string:
        references = reference_string.split('.')
        for reference in references:
            try:
                module = __import__(reference)
            except Exception:
                return getattr(module, reference) if hasattr(module, reference) else None

def fetch_switchers(json):
    module = __import__('utils')
    for switcher in json:
        switcher_dict = getattr(module, switcher)
        switcher_dict.update(json[switcher])

def check_variables(switcher):
    if isinstance(switcher, dict) and 'variable' in switcher:
        return get_reference(switcher['variable'])
    return switcher

def get_conf_attribute(attribute_dict, obj, obj_fields):
    value = None
    if isinstance(attribute_dict, list):
        value = str(get_attribute(check_for_path(attribute_dict[0], check_conf_parent(attribute_dict[0], obj, obj_fields)), attribute_dict[0]['field']))
        for dict_element in attribute_dict[1:]:
            value = str(value) + ', ' + str(get_attribute(check_for_path(dict_element, check_conf_parent(dict_element, obj, obj_fields)), dict_element['field']))
    else:
        value = get_attribute(check_for_path(attribute_dict, check_conf_parent(attribute_dict, obj, obj_fields)), attribute_dict['field'], attribute_dict.get('separator', ''))
    return value

def check_conf_parent(dict_element, obj, obj_fields):
    if dict_element.get('from', None) != 'parent':
                obj_fields = obj
    return obj_fields