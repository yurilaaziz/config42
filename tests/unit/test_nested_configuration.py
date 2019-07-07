import os

from config42 import ConfigManager


def test_configuration_content(cwd):
    defaults = {'config42': {'file': {'path': cwd + "/files/nested-config.yml"}}}
    os.environ.update({"BARBEROUSSE_ENV1": "TEST1"})
    config_manager = ConfigManager(defaults=defaults)

    assert config_manager.get('config42') is not None
    assert len(config_manager.get('config42')) > 1
    assert config_manager.get('env1') == "TEST1"
    assert config_manager.get('nested') == "value"


def test_change_nesting_key(cwd):
    defaults = {'config43': {'file': {'path': cwd + "/files/nested-config.yml"}}}
    config_manager = ConfigManager(defaults=defaults, nested_configuration_key="config43")
    assert config_manager.get('config43') is not None
    assert config_manager.get('nested') == "value"
