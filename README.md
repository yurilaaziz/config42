[![Latest version on](https://badge.fury.io/py/config42.svg)](https://badge.fury.io/py/config42)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/config42.svg)](https://pypi.org/project/config42/)
[![Travis Pipelines build status](https://img.shields.io/travis/com/yurilaaziz/config42.svg)](https://travis-ci.com/yurilaaziz/config42/)
[![codecov](https://codecov.io/gh/yurilaaziz/config42/branch/master/graph/badge.svg)](https://codecov.io/gh/yurilaaziz/config42)
# Config42

Config42  is a complete configuration reader and manager. It aims to read the configuration from different sources: a memory Dict object, an external file ( YAML, JSON, INI, PYTHON Object ), an SQL database (Postgres, MySQL, Oracle) 
alternatively, Key-value data store ( Etcd )

It is designed to be extensible. Different handlers could support another data store. 
All PR are welcome. 

## Install 

**From sources:**  (Bleeding edge)

`pip install git+https://github.com/yurilaaziz/config42`

**From PyPi:** (Stable)

`pip install config42`

## Getting started
Config42 abstract loading configuration complexity. Let config42 manage your configuration for you.

### Using environment variables 
Most of the containerised applications change behaviour from environment variables to change their behaviour. config42 handle it easily.
 
Here a working sample [examples/docker](examples/docker)

```python
from config42 import ConfigManager
env_config = ConfigManager(prefix="MYAPP")
# Access to configuration via the ConfigManager getter
print("username : {}".format(env_config.get('username')))
print("nested key  : {}".format(env_config.get('secret.one')))
```

Export variables to system environment 
```bash
export MYAPP_USERNAME=yuri
export MYAPP_SECRET_ONE=password
python app.py
```

Export variables to process environment 

```bash
MYAPP_USERNAME=yuri2 python app.py
```

Once you build you docker image, you may run the application by export variables into the container environment
```bash
docker run  -e MYAPP_USERNAME=yuri -e MYAPP_SECRET_ONE=secret testconfig42:latest
```


### Using Etcd  Handler 
To load configuration from Etcd data store, you need to specify the *keyspace* where the configuration is located, Etcd host(s) and port(s).

```python
from config42 import ConfigManager
from config42.handlers import Etcd

config = ConfigManager(handler=Etcd, keyspace='/config')
# config = ConfigManager(handler=Etcd, keyspace='/config', port=4001)
# config = ConfigManager(handler=Etcd, keyspace='/config', host='127.0.0.1', port=4001)
# config = ConfigManager(handler=Etcd, keyspace='/config', host=(('127.0.0.1', 4001), ('127.0.0.1', 4002), ('127.0.0.1', 4003)))

```
Note : Etcd handler use [python-etcd](https://github.com/jplana/python-etcd) client 
All args after keyspace are passed to Etcd.Client class. 


### Using Filehandler, Load configuration from file 
```python
from pprint import pprint
from config42 import ConfigManager
from config42.handlers import FileHandler

# Yaml files
config = ConfigManager(handler=FileHandler, path='files/config1.yml')
#config = ConfigManager(handler=FileHandler, path='files/config1.yaml')

# Json file 
#config = ConfigManager(handler=FileHandler, path='files/config1.json')

#INI structure support only one level of nesting (Sections = { key: value }) 
#config = ConfigManager(handler=FileHandler, path='files/config.ini')

CONFIG = config.as_dict()

print("Configuration has been loaded")
pprint(CONFIG)

# Access to configuration via the ConfigManager getter
print("application_name : {}".format(config.get('application_name')))
print("nested key : {}".format(config.get('nested.nestedkey.key2')))

# Access to configuration via the as dict utility; it will dump configuration file to data store if updated
print("user : {}".format(config.as_dict()['user']))

# Access to configuration via the classic CONFIG global variable
print("application_name : {}".format(CONFIG['application_name']))
print("nested key : {}".format(CONFIG['nested']['nestedkey']['key2']))
````

## Real use case
Below is a real use from Instabot-Py project that uses this library as a configuration manager.

config42 handles 4 sources of configuration data in order of priority:

* Default configuration from Dict Object
* Environment variables prefixed by INSTABOT
* Local file where value located in config.file (INSTABOT_CONFIG_FILE)
* Etcd data-store

ref : [https://github.com/yurilaaziz/instabot.py](https://github.com/yurilaaziz/instabot.py)
ref : [https://github.com/instabot-py/instabot.py](https://github.com/instabot-py/instabot.py) 

```python
import logging.config
import os

from config42 import ConfigManager

from instabot_py.default_config import DEFAULT_CONFIG

env_config = ConfigManager(prefix="INSTABOT")
logging.basicConfig(level=logging.DEBUG if env_config.get("debug") else logging.INFO)
LOGGER = logging.getLogger(__name__)
config = ConfigManager()
config.set_many(DEFAULT_CONFIG)

config.set_many(env_config.as_dict())
config_file = config.get("config.file")
config_etcd = config.get("config.etcd")

if config_file:
    if config_file.startswith("/"):
        config_path = config_file
    else:
        cwd = os.getcwd()
        config_path = cwd + "/" + config_file
    config.set_many(ConfigManager(path=config_path.replace('//', '/')).as_dict())
    LOGGER.info("Setting configuration from {} : OK".format(config_file))

if config_etcd:
    if not config_etcd.get("keyspace"):
        raise Exception("etcd Keyspace is mandatory")
    try:
        config.set_many(ConfigManager(**config_etcd).as_dict())
        LOGGER.info(
            "Setting external configuration from {} : OK".format(config_file))
    except Exception as exc:
        LOGGER.error(
            "Setting external configuration from ({}) : NOT OK".format(
                ",".join({key + "=" + value for key, value in config_etcd.item() or {}})
            ))

        LOGGER.exception(exc)
        raise exc

logging.config.dictConfig(config.get("logging"))

``` 


## Requirements
### Yaml configuration files

```bash
pip install Pyaml
```

### Etcd data store 
```bash
pip install python-etcd
```

### DEV 
The following packages are needed to run tests and coverage

```bash
pip install tox pytest-cov pytest flake8
```

or 

```bash
pip install -r requirements/ci.txt
pip install -r requirements/tests.txt
```


## Usage examples

* [from-etcd.py](examples/from-etcd.py)
* [from-yaml.py](examples/from-yaml.py)


## TODO
* readthedoc with sphinx

## Releases

#### 0.3.1
* Add set default variables feature
#### 0.3
* Add Environment Handler

#### 0.2

* Add Etcd Handler
* Add Ini Yaml, Json Handlers