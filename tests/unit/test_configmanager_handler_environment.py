from uuid import uuid1

import config42
from config42.handlers.environment import Environment


def test_load_empty_config():
    config_manager = config42.ConfigManager(handler=Environment, prefix='BARBEROUSSE' + uuid1().hex)
    assert config_manager.handler.load() is not None


def test_implicit_handler():
    config_manager = config42.ConfigManager(prefix='BARBEROUSSE')
    assert config_manager.handler.load() is not None


def test_load_configuration():
    import os
    env_vars = {"BARBEROUSSE_WORKER_CONFIG_HOST": "TEST1"}
    env_vars["BARBEROUSSE_WORKER_CONFIG_VERY_LONG_KEY_WITH_66_ENVIRONMENT_LENGTH"] = "66"
    env_vars["BARBEROUSSE2_NOKEY"] = "NOKEY"
    os.environ.update(env_vars)
    config_manager = config42.ConfigManager(prefix='BARBEROUSSE')
    for key, value in env_vars.items():
        if "BARBEROUSSE2" in key:
            assert config_manager.get(
                key.replace("BARBEROUSSE2_", "").replace("_", ".").lower()) is None
        else:
            assert value == config_manager.get(
                key.replace("BARBEROUSSE_", "").replace("_", ".").lower())
