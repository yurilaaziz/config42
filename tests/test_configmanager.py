import pytest

import config42


@pytest.fixture
def default_config():
    return {
        'defaultkey1': 'simple',
        'defaultkey2':{'defaultkey2': 'simple'}
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




def test_configuration_content(config):
    config_manager = config42.ConfigManager()
    config_manager.set_many(config)
    assert_configuration_content(config_manager, config)


def assert_configuration_content(config_manager, config):
    assert config['simple'] == config_manager.get('simple')
    assert config['bool'] == config_manager.get('bool')
    assert config['simple_dict']['key'] == config_manager.get('simple_dict.key')
    assert config['nested_dict']['nested']['key'] == config_manager.get('nested_dict.nested.key')
    assert config['nested_list'][0][0] == config_manager.get('nested_list.0.0')
    assert config['nested_list'][1][0] == config_manager.get('nested_list.1.0')
    assert config_manager.get('notindict') is None


def test_configuration_setting(config):
    config_manager = config42.ConfigManager()
    for key, value in config.items():
        config_manager.set(key, value)

    assert_configuration_content(config_manager, config)


def test_configuration_setting_nested_keys(config):
    config_manager = config42.ConfigManager()
    config_manager.set_many(config)
    config_manager.set('key1', 'simple')
    config_manager.set('key2.key2', 'simple')
    config_manager.set('key3.key3.key3', 'simple')

    assert 'simple' == config_manager.get('key1')
    assert 'simple' == config_manager.get('key2.key2')
    assert 'simple' == config_manager.get('key3.key3.key3')


def test_configuration_content_absent_keys():
    config_manager = config42.ConfigManager()
    assert config_manager.get('absentkey1') is None
    assert config_manager.get('absentkey2.absentkey2') is None
    assert config_manager.get('absentkey3.absentkey3.absentkey3') is None


def test_configuration_default_values(default_config):
    config_manager = config42.ConfigManager(defaults=default_config)

    assert default_config['defaultkey1'] == config_manager.get('defaultkey1')
    assert default_config['defaultkey2']['defaultkey2'] == config_manager.get('defaultkey2.defaultkey2')
    assert config_manager.get('absentkey3.absentkey3.absentkey3') is None

