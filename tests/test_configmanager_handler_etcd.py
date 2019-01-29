from uuid import uuid1

import config42
from config42.handlers.etcd import Etcd


def test_load_empty_config():
    config_manager = config42.ConfigManager(handler=Etcd, keyspace='/absent_key_' + uuid1().hex)
    assert config_manager.handler.load() is not None


def test_load_and_dump_flush(sample_config):
    config_manager = config42.ConfigManager(handler=Etcd, keyspace='/absent_key_' + uuid1().hex)
    config_manager.set_many(sample_config, trigger_commit=False)
    assert len(config_manager.handler.load()) == 0
    assert config_manager.handler._updated is True
    config_manager.handler.dump()
    assert config_manager.handler._updated is False
    assert len(config_manager.handler.load()) > 0

    config_manager.handler.flush()
    assert len(config_manager.handler.load()) >= 0
    assert config_manager.handler._updated is True

    config_manager.handler.destroy()
    assert len(config_manager.handler.load()) == 0


def test_flush_db(sample_config):
    config_manager = config42.ConfigManager(handler=Etcd)
    assert config_manager.handler.load() is not None
