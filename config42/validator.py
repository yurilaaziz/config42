from cerberus import Validator


class ValidationError(Exception):
    """ Raised when the value of the configuration variable has the wrong format """

    def __init__(self, variable, errors):
        self.message = "Setting' value of '{}' is invalid : {}".format(variable, str(errors))

    def __str__(self):
        return (repr(self.message))


class ConfigurationSchemaError(Exception):
    """ Raised when the value of the configuration schema has the wrong format """

    def __init__(self, errors):
        self.messages = ""
        for error in errors:
            for key, value in error.items():
                self.messages += "Setting' schema #{} is invalid : {}".format(key, value)

    def __str__(self):
        return (repr(self.messages))


class DefaultValidator:
    _schema_row = {
        "name": {"type": "string", "required": True},
        "description": {"type": "string", "required": False},
        "key": {"type": "string", "required": True},
        "choices": {'type': 'list'},
        "source": {'type': 'dict',
                   'schema': {
                       'argv': {'type': 'list',
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
            if not validator.validate(
                    {'value': config_manager.get(item.get('key'))}):
                raise ValidationError(item['name'], validator.errors['value'])

    def cerberus_schema_helper(self, item):
        _schema = {'required': item.get('required', True),
                   'nullable': item.get('nullable', False),
                   }
        if item.get('choices', None):
            _schema['allowed'] = item['choices']
        if item.get('type', None):
            _schema['type'] = item['type']
        return {'value': _schema}
