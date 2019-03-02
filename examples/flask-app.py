from flask import Flask

from config42 import ConfigManager

app = Flask(__name__)
# flask application configuration
ConfigManager(app, path='./tests/files/flask-app.yml')

# Concrete application config
CONF = ConfigManager(path='./tests/files/book-list.yml')


@app.route('/conf')
def dump_conf():
    return str(app.config)


@app.route('/books')
def books():
    return str(CONF.as_dict())
