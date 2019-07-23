import os

import pytest
from cerberus import Validator

from config42 import ConfigManager
from config42.validator import DefaultValidator, ConfigurationSchemaError, ValidationError


def test_validation_schema():
    _ = Validator(DefaultValidator._schema)


def test_config_validation():
    v = Validator(DefaultValidator._schema_row)
    assert v.validate({
        "name": "Super user name",
        "description": "User description",
        "key": "superuser",
        "choices": ["admin", "administrator"],
        "default": "admin",
        "type": "string"}
    )
    assert v.validate({
        "name": "Super user name",
        "description": "User description",
        "key": "superuser",
        "choices": ["admin", "administrator"],
        "default": "admin",
        "type": "stringz"}
    ) is False
    assert v.validate({
        "name": "Super user name",
        # "description": "User description", # not required
        "key": "superuser",
        # "choices": ["admin", "administrator"], # not required
        # "default": "admin", # not required
        # "type": "stringz" # not required
    }
    ) is True

    assert v.validate({
        "name": "Super user name",
        "key": "superuser.nested",
    }
    ) is True

    assert v.validate({
        "name": "user id ",
        "key": "superuser.id",
        "type": "integer"
    }
    ) is True


def test_document_validation():
    assert DefaultValidator([{
        "name": "Super user name",
        "description": "User description",
        "key": "superuser",
        "choices": ["admin", "administrator"],
        "default": "admin",
        "type": "string"}]
    )
    with pytest.raises(ConfigurationSchemaError):
        DefaultValidator([{
            "name": "Super user name",
            "description": "User description",
            "key": "superuser",
            "choices": ["admin", "administrator"],
            "default": "admin",
            "type": "stringz"}]
        )

    assert DefaultValidator([{
        "name": "Super user name",
        # "description": "User description", # not required
        "key": "superuser",
        # "choices": ["admin", "administrator"], # not required
        # "default": "admin", # not required
        # "type": "stringz" # not required
    }]
    )

    assert DefaultValidator([{
        "name": "Super user name",
        "key": "superuser.nested",
    }]
    )

    assert DefaultValidator([{
        "name": "user id ",
        "key": "superuser.id",
        "type": "integer"
    }]
    )


def test_validation_with_configmanager():
    schema = [{
        "name": "user id ",
        "key": "user.id",
        "type": "integer",
        "required": True
    }, {
        "name": "user name ",
        "key": "user.name",
        "type": "string",
        "required": True
    }
    ]
    config_sample = {'user': {'id': 1234, 'name': 'user'}}

    config_manager = ConfigManager(schema=schema, defaults=config_sample)
    assert config_manager.get('user.name') == 'user'

    with pytest.raises(ValidationError):
        _ = ConfigManager(schema=schema, defaults={})

    # Disable validator
    _ = ConfigManager(schema=schema, validator=False, defaults={})


def test_validation_with_nested_configmanager():
    schema = [{
        "name": "user id ",
        "key": "user.id",
        "type": "integer",
        "required": True
    }, {
        "name": "user name ",
        "key": "user.name",
        "type": "string",
        "required": True
    }
    ]
    config_sample = {'user': {'id': 1234}}
    with pytest.raises(ValidationError):
        _ = ConfigManager(schema=schema, defaults=config_sample)

    os.environ.update({"BARBEROUSSE_USER_NAME": "user"})
    config_manager = ConfigManager(schema=schema, prefix="BARBEROUSSE", defaults=config_sample)
    assert config_manager.get('user.name') == 'user'
    assert config_manager.get('user.id') == 1234

    config_sample.update({'config42': {'env': {'prefix': 'BARBEROUSSE'}}})
    config_manager = ConfigManager(schema=schema, defaults=config_sample)

    assert config_manager.get('user.name') == 'user'
    assert config_manager.get('user.id') == 1234


def test_validation_defaults_configmanager():
    schema = [{
        "name": "user id ",
        "key": "user.id",
        "type": "integer",
        "default": 1234
    }, {
        "name": "user name ",
        "key": "user.name",
    }
    ]

    with pytest.raises(ValidationError):
        _ = ConfigManager(schema=schema)

    config_manager = ConfigManager(schema=schema, defaults={'user': {'name': 'user'}})
    assert config_manager.get('user.name') == 'user'
    assert config_manager.get('user.id') == 1234


def test_validation_casting():
    schema = [{
        "name": "user id ",
        "key": "user.id",
        "type": "integer",
    }, {
        "name": "user code ",
        "key": "user.code",
        "type": "string"
    }
    ]

    config_manager = ConfigManager(schema=schema, defaults={'user': {'id': '12345', 'code': 12345}})
    assert config_manager.get('user.code') == '12345'
    assert config_manager.get('user.id') == 12345
