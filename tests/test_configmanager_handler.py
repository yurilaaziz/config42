from unittest.mock import Mock

import pytest

from config42.handlers.databases.handler import DatabaseHandler

try:
    from tests.handler_config import handlers
except ImportError:
    handlers = {}


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
        'simple_dict': {'key': 'value'},
        'nested_dict': {'key': 'value', 'nested': {'key': 'value'}},
        'simple_list': ['', 'value'],
        'nested_list': [[''], ['value']]
    }


@pytest.fixture
def db_config():
    return {
        ('simple', 'value'),
        ('simple_dict.key', 'value'),
        ('nested_dict.key', 'value'),
        ('nested_dict.nested.key', 'value'),
        ('simple_list.0', ''),
        ('simple_list.1', 'value'),
        ('nested_list.0.0', ''),
        ('nested_list.1.0', 'value'),
    }


def test_database_handler(config, db_config):
    table = "config"
    handler = DatabaseHandler(table=table)
    handler._query = Mock(return_value=db_config)
    handler._delete_insert = Mock()
    assert handler.load() == config
    handler.dump(config)
    handler._delete_insert.assert_called_once()
    args = set(handler._delete_insert.call_args[0][0])
    assert args == db_config


# Generic test, using handlers declared in 'handler_config.py'
def test():
    for handler_cls, kwargs in handlers.items():
        handler = handler_cls(**kwargs)
        handler.create()
        store = {
            "simple":      "v1",
            "bool":        True,
            "simple_dict": {"key": "v2"},
            "nested_dict": {"key": "v3", "nested": {"key": "v4"}},
            "simple_list": ["", "v5"],
            "nested_list": [[""], ["v6"]]
        }
        handler.dump(store)
        assert handler.load() == store
        handler.destroy()
