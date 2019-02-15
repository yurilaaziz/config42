from pprint import pprint

from config42 import ConfigManager
from config42.handlers import Etcd

config = ConfigManager(handler=Etcd, keyspace='/config')
# config = ConfigManager(handler=Etcd, keyspace='/config', port=4001)
# config = ConfigManager(handler=Etcd, keyspace='/config', host='127.0.0.1', port=4001)
# config = ConfigManager(handler=Etcd, keyspace='/config',
#                       host=(('127.0.0.1', 4001), ('127.0.0.1', 4002), ('127.0.0.1', 4003)))

print("Configuration has been loaded")
pprint(config.handler.as_dict())
