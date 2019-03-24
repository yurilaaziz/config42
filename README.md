[![Latest version on](https://badge.fury.io/py/config42.svg)](https://badge.fury.io/py/config42)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/config42.svg)](https://pypi.org/project/config42/)
[![Travis Pipelines build status](https://img.shields.io/travis/com/yurilaaziz/config42.svg)](https://travis-ci.com/yurilaaziz/config42/)
[![codecov](https://codecov.io/gh/yurilaaziz/config42/branch/master/graph/badge.svg)](https://codecov.io/gh/yurilaaziz/config42)
# Config42

The config-manager package is a complete configuration reader and manager. It aims to read the configuration data 
from different sources :a memory dict object, an external file ( YAML, JSON, INI, PYTHON Object ), an SQL data base (postgres, mysql, oracle) 
or Key value data store data store ( Etcd )

It is designed to be extensible. Other data store could be supported by different handlers, All PR are welcome. 

## Install 

**From sources:**  (Bleeding edge)

`pip install git+https://github.com/yurilaaziz/config42`

**From PyPi:** (Stable)

`pip install config42`

## Getting started
### Using Etcd  Handler 
To load configuration from Etcd data store, you need to specify the *keyspace* where the configuration is located

```python
from config42 import ConfigManager
from config42.handlers import Etcd

config = ConfigManager(handler=Etcd, keyspace='/config')
# config = ConfigManager(handler=Etcd, keyspace='/config', port=4001)
# config = ConfigManager(handler=Etcd, keyspace='/config', host='127.0.0.1', port=4001)
# config = ConfigManager(handler=Etcd, keyspace='/config', host=(('127.0.0.1', 4001), ('127.0.0.1', 4002), ('127.0.0.1', 4003)))

```
Note : Etcd handler use [python-etcd](https://github.com/jplana/python-etcd) client 
All args after keypsace are passed to etcd.Client class. 

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

#### 0.3
* Add Environment Handler

#### 0.2

* Add Etcd Handler
* Add Ini Yaml, Json Handlers