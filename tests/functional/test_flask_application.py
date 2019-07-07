from flask import Flask

import config42


def test_flask_configuration(cwd):
    app = Flask(__name__)
    config_manager = config42.ConfigManager(app, path=cwd + "/files/flask-app.yml")
    assert config_manager.get('NAME') == app.config.get('NAME')


def test_flask_configuration_init_app(cwd):
    config_manager = config42.ConfigManager(path=cwd + "/files/flask-app.yml")
    app = Flask(__name__)
    config_manager.init_app(app)
    assert config_manager.get('NAME') is not None
    assert config_manager.get('NAME') == app.config.get('NAME')
