import pytest

import config42


@pytest.fixture
def default_config():
    return {
        'defaultkey1': 'simple',
        'defaultkey2': {'defaultkey2': 'simple'}
    }


@pytest.fixture
def config():
    return {
        'simple': 'value',
        'bool': True,
        'simple_dict': {'key': 'value'},
        'nested_dict': {'key': 'value', 'nested': {'key': 'value'}},
        'nested_list': [[''], ['value']]
    }


def test_default_handler():
    config_manager = config42.ConfigManager()
    assert isinstance(config_manager.handler, config42.handlers.memory.Memory)


def test_default_handler_dump():
    memory_handler = config42.handlers.memory.Memory()
    assert memory_handler.dump()
