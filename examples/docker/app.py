from config42 import ConfigManager
env_config = ConfigManager(prefix="MYAPP")
# Access to configuration via the ConfigManager getter
print("username : {}".format(env_config.get('username')))
print("nested key  : {}".format(env_config.get('secret.one')))