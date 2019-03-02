from flask import Flask

import config42


def test_flask_configuration():
    app = Flask(__name__)
    config_manager = config42.ConfigManager(app, path="files/flask-app.yml")
    assert config_manager.get('DEBUG') == app.config.get('DEBUG')
    assert config_manager.get('NAME') == app.config.get('NAME')


def test_flask_configuration_init_app():
    config_manager = config42.ConfigManager(path="files/flask-app.yml")
    app = Flask(__name__)
    config_manager.init_app(app)
    assert config_manager.get('DEBUG') == app.config.get('DEBUG')
    assert config_manager.get('NAME') == app.config.get('NAME')
