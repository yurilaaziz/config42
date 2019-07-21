from uuid import uuid1

import config42
from config42.handlers.etcd import Etcd


def test_load_empty_config():
    config_manager = config42.ConfigManager(handler=Etcd, keyspace='/absent_key_' + uuid1().hex)
    assert config_manager.handler.load() is not None


def test_no_explicit_handler():
    config_manager = config42.ConfigManager(keyspace='/absent_key_' + uuid1().hex)
    assert config_manager.handler.load() is not None


def test_load_and_dump_flush(sample_config):
    config_manager = config42.ConfigManager(handler=Etcd, keyspace='/absent_key_' + uuid1().hex)
    config_manager.set_many(sample_config, trigger_commit=False)
    assert len(config_manager.handler.load()) == 0
    assert config_manager.handler.updated is True
    config_manager.handler.dump()
    assert config_manager.handler.updated is False
    assert len(config_manager.handler.load()) > 0

    config_manager.handler.flush()
    assert len(config_manager.handler.load()) >= 0
    assert config_manager.handler.updated is True

    config_manager.handler.destroy()
    assert len(config_manager.handler.load()) == 0


def test_load_content(sample_config):
    keyspace = '/new_key_' + uuid1().hex
    config_manager = config42.ConfigManager(handler=Etcd, keyspace=keyspace)
    assert len(config_manager.handler.load()) == 0
    config_manager.set_many(sample_config, trigger_commit=False)
    config_manager.handler.dump()
    config_manager = config42.ConfigManager(handler=Etcd, keyspace=keyspace)
    assert sample_config['simple'] == config_manager.get('simple')
    assert sample_config['bool'] != config_manager.get('bool')
    assert sample_config['bool'] == bool(config_manager.get('bool'))
    assert sample_config['simple_dict']['key'] == config_manager.get('simple_dict.key')
    assert sample_config['nested_dict']['nested']['key'] == config_manager.get('nested_dict.nested.key')
    assert sample_config['nested_list'][0][0] == config_manager.get('nested_list.0.0')
    assert sample_config['nested_list'][1][0] == config_manager.get('nested_list.1.0')
    assert config_manager.get('notindict') is None


def test_handler_keyspace():
    keyspace = 'no_slash' + uuid1().hex
    config_manager = config42.ConfigManager(handler=Etcd, keyspace=keyspace)
    config_manager.set('key', 'value')
    config_manager.set('key2.key', 'value')
    config_manager = config42.ConfigManager(handler=Etcd, keyspace=keyspace)
    assert config_manager.get('key') == 'value'
    assert config_manager.get('key2.key') == 'value'


def test_flush_db():
    config_manager = config42.ConfigManager(handler=Etcd)
    assert config_manager.handler.load() is not None
