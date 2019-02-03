from unittest.mock import Mock

import pytest

import config42
from config42.handlers.databases import DatabaseHandler
from config42.handlers.files import FileHandler


@pytest.fixture
def default_config():
    return {
        'defaultkey1': 'simple',
        'defaultkey2': {'defaultkey2': 'simple'}
    }


@pytest.fixture
def config():
    return {
        'simple':      'value',
        'bool':        True,
        'simple_dict': {'key': 'value'},
        'nested_dict': {'key': 'value', 'nested': {'key': 'value'}},
        'simple_list': ['', 'value'],
        'nested_list': [[''], ['value']]
    }


@pytest.fixture
def db_config():
    return [
        ('simple', 'value'),
        ('bool', True),
        ('simple_dict.key', 'value'),
        ('nested_dict.key', 'value'),
        ('nested_dict.nested.key', 'value'),
        ('simple_list.0', ''),
        ('simple_list.1', 'value'),
        ('nested_list.0.0', ''),
        ('nested_list.1.0', 'value'),
    ]


def test_default_handler():
    config_manager = config42.ConfigManager()
    assert isinstance(config_manager.handler, config42.handlers.memory.Memory)


def test_default_handler_dump():
    memory_handler = config42.handlers.memory.Memory()
    assert memory_handler.dump()


def test_file_handler_init_with_file_path():
    with pytest.raises(TypeError):
        config42.ConfigManager(handler=FileHandler)
    config42.ConfigManager(handler=FileHandler, path="path")


def test_database_handler(config, db_config):
    table = "config"
    handler = DatabaseHandler(table=table)
    handler._config = config
    handler._query = Mock(return_value=db_config)
    handler._delete_insert = Mock()
    print()
    assert handler.load() == config
    assert handler.dump()
    handler._delete_insert.assert_called_once_with(db_config)


def test_database_handler_with_mixed_subkeys():
    handler = DatabaseHandler(table="")
    with pytest.raises(TypeError, match=DatabaseHandler.MIXED_KEYS_ERROR % "key"):
        handler._query = Mock(return_value=[("key.0", "v1"), ("key.other", "v2")])
        handler.load()
