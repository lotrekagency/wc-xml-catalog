from pywoo.models.products import Product
import utils

class FeedProduct(Product):

    def __init__(self, product, parent=None):
        self._product = product
        self._parent = parent

    def __getattr__(self, attr):
        try:
            return getattr(self._product, attr)
        except AttributeError as exception:
            raise type(exception)(("{0} at product ID {1} with attribute '{2}'").format(exception, self.id, attr))

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
                            if obj.get(key, None) == value:
                                return obj, True
                    return None, True
            return path, False

        path = self
        for fieldname in fieldnames[:-1]:
            path, conditions = select(path, fieldname)
            if not conditions:
                path = getattr(path, fieldname)
        fieldname = fieldnames[-1]
        value = None
        if isinstance(path, dict):
            value = path.get(fieldname)
        elif isinstance(path, list):
            value = [getattr(obj, fieldname) for obj in path]
        else:
            value = getattr(path, fieldname)
        return str(value)

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
        else:
            if config.get('fatal'):
                is_valid = False
        return value, is_valid, config.get('unique')

    def read_config_value(self, config):
        value = None
        if 'static' in config:
            value = config['static']
        elif 'default' in config:
            value = utils.get_default_value(config['default'])
        elif 'attribute' in config:
            value = self.get_value(config['attribute'])
        elif 'parent' in config:
            if self._parent:
                value = self._parent.get_value(config['parent'])
            else:
                value = self.get_value(config['parent'])
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


