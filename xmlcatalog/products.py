from pywoo.models.products import Product
import utils
import copy

MAIN_KEYS = set(['static', 'attribute', 'parent', 'default'])
EXTRA_KEYS = set(['unique', 'suffix', 'prefix', 'separator', 'replacer', 'fatal', 'visible'])

class FeedProduct(Product):

    def __init__(self, product, parent=None):
        self._product = product
        self._parent = parent

    def __getattr__(self, attr):
        return getattr(self._product, attr)

    def get_value(self, fieldname):
        fieldnames = fieldname.split('.')

        def select(path, fieldname):
            if ']' in fieldname:
                fieldname_split = fieldname.replace(']', '[').split('[')
                return getattr(path, fieldname_split[0])[int(fieldname_split[-2])], True
            if '(' in fieldname:
                fieldname_split = fieldname.replace(')', '(').split('(')
                attribute = fieldname_split[0]
                condition = fieldname_split[-2]
                if '=' in condition:
                    condition_splitted = condition.split('=')
                    key = condition_splitted[0]
                    value = condition_splitted[-1]
                    current_location = getattr(path, attribute)
                    if isinstance(current_location, list):
                        for obj in current_location:
                            if isinstance(obj, dict):
                                if obj.get(key, None) == value:
                                    return obj, True
                            else:
                                if getattr(obj, key, None) == value:
                                    return obj, True
                    return None, True
            return path, False

        try:
            path = self

            for field in fieldnames[:-1]:
                path, conditions = select(path, field)
                if not conditions:
                    path = getattr(path, field)

            field = fieldnames[-1]
            value = None

            if isinstance(path, dict):
                value = path.get(field)
            elif isinstance(path, list):
                value = [getattr(obj, field) for obj in path]
            else:
                value, conditions = select(path, field)
                if not conditions:
                    value = getattr(value, field)

            return value
        except Exception as exception:
            raise type(exception)(("{0} at product ID {1} with attribute '{2}'").format(exception, self.id, fieldname))


    def process_value(self, value, config):
        value = [str(value_element) if not isinstance(value_element, dict) else value_element for value_element in value if value_element]

        if 'replacer' in config:
            replacer_dict = config['replacer']
            value = [replacer_dict[value_element] if value_element in replacer_dict else replacer_dict.get('replacer_fail', value_element) for value_element in value]

        try:
            value = config.get('prefix', '') + (config.get('separator', ', ')).join(value) + config.get('suffix', '')
        except TypeError:
            pass

        if not config.get('visible', True):
            value = {}

        return value

    def read_config_value(self, key, value):
        value_list = [value] if not isinstance(value, list) else value
        returned_value = []
        retrieved_value = None

        for value_item in value_list:
            if key == 'static':
                retrieved_value = value_item
            elif key == 'default':
                retrieved_value = utils.get_default_value(value_item)
            elif key == 'attribute':
                try:
                    retrieved_value = self.get_value(value_item)
                except AttributeError:
                    pass
            elif key == 'parent':
                try:
                    if self._parent:
                        retrieved_value = self._parent.get_value(value_item)
                    else:
                        retrieved_value = self.get_value(value_item)
                except AttributeError:
                    pass
            if retrieved_value:
                returned_value.append(retrieved_value) if not isinstance(retrieved_value, list) else returned_value.extend(retrieved_value)

        return returned_value


    def read_config(self, config):
        value = []

        for key, key_config in list(config.items()):
            if not isinstance(key_config, dict):
                value_read = self.read_config_value(key, key_config)
                if value_read:
                    value.extend(value_read)

        is_valid = self.check_valid_value(value, config)

        if value:
            return self.process_value(value, config), is_valid

        if list(set(config.keys()) & MAIN_KEYS):
            config = {}

        return config, is_valid

    def get_taxed_price(self, value, rate):
        try:
            return str(round(float(value) + ((float(value) / 100) * float(rate)), 2))
        except Exception:
            return None
        
    def check_valid_value(self, value, config):
        is_valid = True

        if 'fatal' in config:
            fatal_value = config.get('fatal', False)

            if not isinstance(fatal_value, bool):
                fatal_value = [fatal_value] if not isinstance(fatal_value, list) else fatal_value
                if not list(set(map(str, value)) & set(map(str, fatal_value))):
                    is_valid = False
            else:
                if fatal_value and not value:
                    is_valid = False

        return is_valid

    def parse_dict(self, config):
        config = copy.deepcopy(config)

        for key in config.keys():
            config[key] = [config[key]] if not isinstance(config[key], list) else config[key]
            for index in range(len(config[key])):
                config[key][index], is_valid = self.read_config(config[key][index])
                if isinstance(config[key][index], dict):
                    config[key][index] = self.parse_dict(config[key][index])
                if not is_valid:
                    return {}
                    
        return config

    @property
    def price(self):
        if not self._product.price:
            return
        return '{0:.2f}'.format(float(self._product.price))
    
    @property
    def sale_price(self):
        if not self._product.sale_price:
            return
        return '{0:.2f}'.format(float(self._product.sale_price))

    @property
    def taxed_price(self):
        taxed_price = self.get_taxed_price(self._product.price, utils.current_tax_rate)
        if not taxed_price:
            return
        return '{0:.2f}'.format(float(taxed_price))

    @property
    def taxed_sale_price(self):
        taxed_sale_price = self.get_taxed_price(self._product.sale_price, utils.current_tax_rate)
        if not taxed_sale_price:
            return
        return '{0:.2f}'.format(float(taxed_sale_price))

