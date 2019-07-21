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


def test_raw_handler_destroy(tmp_path):
    dir = tmp_path / "raw"
    dir.mkdir()
    key_file = dir / "key"
    key2_file = dir / "key2"
    key_file.write_text("value")
    key2_file.write_text("value2")

    config_manager_dir = config42.ConfigManager(path=str(dir))
    assert config_manager_dir.get('key') == 'value'
    assert config_manager_dir.get('key2') == 'value2'
    config_manager_file = config42.ConfigManager(path=str(key_file))
    assert config_manager_file.get('key') == 'value'
    config_manager_file.handler.destroy()

    config_manager_dir = config42.ConfigManager(path=str(dir))
    assert config_manager_dir.get('key') is None
    assert config_manager_dir.get('key2') == 'value2'
    config_manager_dir.handler.destroy()

    config_manager_dir = config42.ConfigManager(path=str(dir))
    assert config_manager_dir.get('key2') is None
