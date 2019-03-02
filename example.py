from flask import Flask
from config42 import ConfigManager

app = Flask(__name__)
ConfigManager(app)
