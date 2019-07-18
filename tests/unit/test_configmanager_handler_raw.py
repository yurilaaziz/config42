import config42
from config42.handlers.raw import RawHandler


def test_raw_handler_file(cwd):
    handler = RawHandler(path=cwd + "/files/raw/foo")
    config = handler.load()
    assert config.get('foo') == 'bar'
    assert config.get('bar') is None


def test_raw_handler_directory(cwd):
    handler = RawHandler(path=cwd + "/files/raw")
    config = handler.load()
    assert config is not None
    assert config.get('foo') == 'bar'
    assert config.get('bar') == 'foo'
    assert config.get('foobar') == 'foobar'


def test_raw_handler_directory_configmanager(cwd):
    config_manager = config42.ConfigManager(path=cwd + "/files/raw")
    assert config_manager.get('foo') == 'bar'
    assert config_manager.get('bar') == 'foo'
    assert config_manager.get('foobar') == 'foobar'
