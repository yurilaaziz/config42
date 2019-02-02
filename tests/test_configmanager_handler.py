import config42
from config42.handlers.files import FileHandler


def test_default_handler():
    config_manager = config42.ConfigManager()
    assert isinstance(config_manager.handler, config42.handlers.memory.Memory)


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
