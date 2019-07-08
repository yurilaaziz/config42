import os

import pytest

import config42
from config42.handlers.files import FileHandler


def test_default_handler():
    config_manager = config42.ConfigManager()
    assert isinstance(config_manager.handler, config42.handlers.memory.Memory)


def assert_configuration_content(config_manager, config):
    assert config['simple'] == config_manager.get('simple')
    assert config['bool'] == config_manager.get('bool')
    assert config['simple_dict']['key'] == config_manager.get('simple_dict.key')
    assert config['nested_dict']['nested']['key'] == config_manager.get('nested_dict.nested.key')
    assert config['nested_list'][0][0] == config_manager.get('nested_list.0.0')
    assert config['nested_list'][1][0] == config_manager.get('nested_list.1.0')
    assert config_manager.get('notindict') is None


def test_default_handler_destroy():
    config_manager = config42.ConfigManager()
    assert config_manager.handler.destroy()


def test_default_handler_flush():
    config_manager = config42.ConfigManager()
    assert config_manager.handler.flush()
    assert config_manager.handler._updated is True


def test_default_handler_dump():
    memory_handler = config42.handlers.memory.Memory()
    assert memory_handler.dump()


def test_ini_init_without_file_path():
    with pytest.raises(TypeError):
        _ = config42.ConfigManager(handler=FileHandler)


def test_ini_not_supported_nesting(sample_config):
    file_path = ".test.config.ini"
    config_manager = config42.ConfigManager(handler=FileHandler, path=file_path)
    with pytest.raises(AttributeError):
        config_manager.set_many(sample_config)


def test_ini_content(tmp_path, sample_config_ini_with_sections):
    file_path = str(tmp_path) + "/test.config.ini"
    config_manager = config42.ConfigManager(handler=FileHandler, path=file_path)
    config_manager.set_many(sample_config_ini_with_sections)
    assert sample_config_ini_with_sections['section1']['key1'] == config_manager.get('section1.key1')
    assert sample_config_ini_with_sections['section2']['key2'] == config_manager.get('section2.key2')


def test_json_configuration_content(tmp_path, sample_config):
    file_path = str(tmp_path) + "/test.config.json"
    config_manager = config42.ConfigManager(handler=FileHandler, path=file_path)
    config_manager.set_many(sample_config)
    assert_configuration_content(config_manager, sample_config)


def test_yaml_configuration_content(tmp_path, sample_config):
    file_path = str(tmp_path) + "/test.config.yml"
    config_manager = config42.ConfigManager(handler=FileHandler, path=file_path)
    config_manager.set_many(sample_config)
    assert_configuration_content(config_manager, sample_config)


def test_generic_init_with_file_path(tmp_path):
    file_path_base = str(tmp_path) + "/test.config."
    for extension in ['yml', 'yaml', 'ini', 'json']:
        file_path = file_path_base + extension
        config_manager = config42.ConfigManager(handler=FileHandler, path=file_path)
        config_manager.set("key.sub", "value")
        assert os.path.exists(file_path) is True
        config_manager.handler.destroy()
        assert os.path.exists(file_path) is False


def test_generic_init_without_explicit_handler(tmp_path):
    file_path_base = str(tmp_path) + "/test.config."
    for extension in ['yml', 'yaml', 'ini', 'json']:
        file_path = file_path_base + extension
        config_manager = config42.ConfigManager(path=file_path)
        config_manager.set("key.sub", "value")
        assert os.path.exists(file_path) is True
        config_manager.handler.destroy()
        assert os.path.exists(file_path) is False
