from unittest.mock import Mock

import pytest

from config42 import ConfigManager, Defaults


def test_config_manager_init():
    cfg = ConfigManager()
    assert cfg._load_handlers == []
    assert cfg._dump_handlers == []
    handler = Defaults({})
    cfg = ConfigManager(handler)
    assert cfg._load_handlers == [handler]
    assert cfg._dump_handlers == [handler]
    cfg = ConfigManager(handler, load_handlers=[Defaults({})],
                        dump_handlers=[Defaults({})])
    assert cfg._load_handlers == [handler]
    assert cfg._dump_handlers == [handler]
    defaults = {"key": "value"}
    cfg = ConfigManager(handler, defaults=defaults)
    assert cfg._load_handlers[0] is handler
    assert isinstance(cfg._load_handlers[1], Defaults)
    assert cfg._load_handlers[1].cfg == defaults
    assert cfg._dump_handlers == [handler]


def test_config_manager_load():
    handler = Defaults({"key": "value"})
    cfg = ConfigManager(handler, defaults={"key": "other", "key2": "value2"})
    assert cfg["key"] == "value"
    assert cfg["key2"] == "value2"
    cfg = ConfigManager(handler, autoload=False)
    with pytest.raises(AssertionError):
        _ = cfg["key"]
    cfg.load()
    assert cfg["key"] == "value"


def test_config_manager_dump():
    h1, h2 = Mock(), Mock()
    cfg = ConfigManager(dump_handlers=[h1, h2])
    cfg.dump()
    h1.dump.assert_called_once_with(cfg.cfg)
    h2.dump.assert_called_once_with(cfg.cfg)
    h1.reset_mock()
    h2.reset_mock()
    assert not cfg._updated
    cfg.dump(if_updated=True)
    h1.dump.assert_not_called()
    h2.dump.assert_not_called()
