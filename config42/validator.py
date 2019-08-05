from cerberus import Validator

from config42.utils import builtin_types


class ValidationError(Exception):
    """ Raised when the value of the configuration variable has the wrong format """

    def __init__(self, variable, errors):
        self.message = "The configuration value of '{}' is invalid : {}".format(variable, str(errors))

    def __str__(self):
        return str(self.message)


class ValueTypeError(Exception):
    """ Raised when the value of the configuration variable has the wrong type"""

    def __init__(self, variable, expected_type):
        self.message = "The configuration value of '{}' is invalid : Type expected {}".format(variable, expected_type)

    def __str__(self):
        return self.message


class ConfigurationSchemaError(Exception):
    """ Raised when the value of the configuration schema has the wrong format """

    def __init__(self, errors):
        self.messages = ""
        for error in errors:
            for key, value in error.items():
                self.messages += "The configuration schema contains invalid value in #{}: {}".format(key, value)

    def __str__(self):
        return str(self.messages)


class DefaultValidator:
    _schema_row = {
        "name": {"type": "string", "required": True},
        "description": {"type": "string", "required": False},
        "key": {"type": "string", "required": True},
        "choices": {'type': 'list'},
        "source": {'type': 'dict',
                   'schema': {
                       'argv': {'type': 'list',
                                'required': False},
                       'argv_options': {'type': 'dict',
                                        'required': False}
                   }},
        "required": {'type': 'boolean'},
        "nullable": {'type': 'boolean'},
        "default": {"type": ['string', 'list', 'integer', 'boolean'], "required": False},
        'type': {"type": "string", "allowed": ['string', 'list', 'integer', 'boolean']}
    }
    _schema = {
        'document': {'type': 'list', 'schema': {'type': 'dict', 'schema': _schema_row}}
    }

    def __init__(self, config_schema):
        validator = Validator(self._schema)
        if validator.validate({'document': config_schema}):
            self.config_schema = config_schema
        else:
            raise ConfigurationSchemaError(validator.errors['document'])

    def validate(self, config_manager):
        for item in self.config_schema:
            validator = Validator(self.cerberus_schema_helper(item))
            value = config_manager.get(item.get('key'))
            key_type = item.get('type')
            if value and key_type and not isinstance(value, builtin_types.get(key_type)):
                try:
                    value = builtin_types.get(item.get('type'), str)(value)
                    config_manager.set(item.get('key'), value)
                except (TypeError, ValueError):

                    raise ValueTypeError(value, key_type)

            if not validator.validate({'value': value}):
                raise ValidationError(item['name'], validator.errors['value'])

    def cerberus_schema_helper(self, item):
        _schema = {'required': item.get('required', True),
                   'nullable': item.get('nullable', False),
                   }
        if item.get('choices', None):
            _schema['allowed'] = item['choices']
        if item.get('type', None):
            _schema['type'] = item['type']
        if item.get('required', None):
            _schema['required'] = item['required']

        if not _schema['required']:
            _schema['nullable'] = True
        return {'value': _schema}
