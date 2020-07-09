from pywoo.models.products import Product
import utils

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
        is_valid = True
        if value:
            if config.get('separator'):
                separator = config.get('separator')
                if isinstance(value, list):
                    processed_value = config.get('prefix', '') + str(value[0]) + config.get('suffix', '')
                    for element in value[1:]:
                        processed_value = processed_value + separator + config.get('prefix', '') + str(element) + config.get('suffix', '')
                    value = processed_value
            elif 'replacer' in config:
                replacer_switcher = config['replacer']
                value = replacer_switcher.get(str(value))
            if not type(value) in [dict, list]:
                value = config.get('prefix', '') + str(value) + config.get('suffix', '')
            if 'fatal' in config:
                fatal_value = config.get('fatal')
                if not isinstance(fatal_value, bool):
                    if isinstance(fatal_value, list):
                        fatal_value = list(map(str, fatal_value))
                        if not str(value) in fatal_value:
                            is_valid = False
                    elif not str(value) == str(fatal_value):
                        is_valid = False
        else:
            if config.get('fatal'):
                is_valid = False
        return value, is_valid, config.get('unique'), config.get('visible', True)

    def read_config_value(self, config):
        value = None
        if 'static' in config:
            value = config['static']
        elif 'default' in config:
            value = utils.get_default_value(config['default'])
        elif 'attribute' in config:
            try:
                value = self.get_value(config['attribute'])
            except AttributeError:
                pass
        elif 'parent' in config:
            try:
                if self._parent:
                    value = self._parent.get_value(config['parent'])
                else:
                    value = self.get_value(config['parent'])
            except AttributeError:
                pass
        return value

    def read_config(self, config):
        post_config = [dict([k]) for k in config.items()]
        value = None
        if post_config:
            value = self.read_config_value(post_config[0])
            for remaining_config in post_config[1:]:
                remaining_value = self.read_config_value(remaining_config)
                if remaining_value:
                    value = value + ', ' + remaining_value
        return self.process_value(value, config)

    def get_taxed_price(self, value, rate):
        try:
            return str(round(float(value) + ((float(value) / 100) * float(rate)), 2))
        except Exception:
            return None

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

