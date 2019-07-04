from pprint import pprint

from config42 import ConfigManager
from config42.handlers import FileHandler

config = ConfigManager(handler=FileHandler, path='files/config1.yml')
CONFIG = config.handler.as_dict()

print("Configuration has been loaded")
pprint(CONFIG)

# Access to configuration via the ConfigManager getter
print("application_name : {}".format(config.get('application_name')))
print("nested key : {}".format(config.get('nested.nestedkey.key2')))

# Access to configuration via the as dict utility; it will dump configuration file to data store if updated
print("user : {}".format(config.handler.as_dict()['user']))

# Access to configuration via the classic CONFIG global variable
print("application_name : {}".format(CONFIG['application_name']))
print("nested key : {}".format(CONFIG['nested']['nestedkey']['key2']))
