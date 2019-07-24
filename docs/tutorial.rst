=================
Config42 Tutorial
=================

.. currentmodule:: config42


Welcome to the Config42 tutorial in which we will refactor the `TinyURL`_ clone
of Werkzeug Tutorial that stores URLs in a Redis instance. Initially the application
contains a hardcoded configuration, like application server hostname and port and other Redis parameters.


You can use `pip` to install the required libraries.

.. code-block:: bash

    pip install config42 Jinja2 redis Werkzeug


Also make sure to have a Redis server running on your local machine.
you can run Redis server using docker :

.. code-block:: bash

    docker run -p 6379:6379 redis



Introducing Shortly
-------------------

    In this tutorial, we will together create a simple URL shortener service
    with Werkzeug.  Please keep in mind that Werkzeug is not a framework, it's
    a library with utilities to create your own framework or application and
    as such is very flexible.  The approach we use here is just one of many you
    can use.

    As data store, we will use `redis`_ here instead of a relational database
    to keep this simple and because that's the kind of job that `redis`_
    excels at.

    Source : `Werkzeug Tutorial`_

The final result will look something like this:

.. image:: _static/shortly.png
    :alt: a screenshot of shortly

.. _Werkzeug Tutorial : https://werkzeug.palletsprojects.com/en/master/tutorial/#introducing-shortly
.. _TinyURL: https://tinyurl.com/
.. _Jinja: http://jinja.pocoo.org/
.. _redis: https://redis.io/

Step 0: Instantiate config42 manager
------------------------------------

.. code-block:: python

   from config42 import ConfigManager
   config = ConfigManager(path="local.yml")

ConfigManager loads the ``local.yml`` file as YAML content.

Not specifying an extension ie:(yaml, yml, ini, json), config42 loads the file as text.
the content is retrievable by calling ``config.get(<FILE_NAME>)``

.. code-block:: python

   config = ConfigManager(path="mykey.key")
   config.get('mykey.key')


let suppose the local.yml contains the configuration below:

*local.yml*:

.. sourcecode:: yaml

   ---
   hostname: localhost
   port: 5000
   redis:
     host: 127.0.0.1
     port: 6379



Step 1: Use config42
--------------------
Let's refactor the code to use config42 instead of passing arguments to the Shortly class

.. code-block:: bash

     class Shortly(object):
    -    def __init__(self, config):
    -        self.redis = redis.Redis(config["redis_host"], config["redis_port"])
    +    def __init__(self):
    +        self.redis = redis.Redis(**config.get('redis'))


And in the client class, we remove the configuration mapping, As we don't need it anymore

.. code-block:: bash

    -   def create_app(redis_host="localhost", redis_port=6379, with_static=True):
    -       app = Shortly({"redis_host": redis_host, "redis_port": redis_port})
    +   def create_app(with_static=True):
    +       app = Shortly()


the method `run_simple` definition is not part of our code. It takes the hostname and port as method arguments.
let's skip the other parameters for now.

.. code-block:: bash

    -    run_simple("127.0.0.1", 5000, app, use_debugger=True, use_reloader=True)
    +    run_simple(config.get('hostname'), config.get('port'), app, use_debugger=True, use_reloader=True)


.. code-block:: bash

    chmod a+x shortly.py
    ./shortly.py

Yes it works fine

Step 2: Register a default configuration
----------------------------------------
It's common to have a default configuration builtin with the application.
It allows running the application with a default conf if the local.yml is absent.

.. code-block:: python

   DEFAULT_CONF = {
      "port": 5001,
      "hostname": "localhost",
      "redis": {
        "host": "127.0.0.1",
        "port": 6379
      }
    }

   config = ConfigManager(path="local.yml", defaults=DEFAULT_CONF)

Step 3: Register a nested configuration
----------------------------------------

Config42 can configure itself. it can include/load other configurations.
Image you have 3 configurations files:

* local.yml
* production.yml
* development.yml

and both ``production.yml`` and ``development.yml`` overload settings in ``local.yml``

*development.yml*:

.. sourcecode:: yaml

   ---
   redis:
     host: redis-dev.local

*production.yml*:

.. sourcecode:: yaml

   ---
   port: 8080
   redis:
     host: redis-prd.local


*local.yml*:

.. sourcecode:: yaml

   ---
   config42:
     file:
       path: production.yml

Now the application will load ``local.yml`` first and ``production.yml`` second.
Note that you can load multiple configuration files.

*local.yml*:

.. sourcecode:: yaml

   ---
   config42:
     file:
       path: production.yml
     another_file_1:
       path: production2.yml
     json_file:
       path: production3.json


** You can use Config42 Defaults to load nested configuration too. I will explain different usage of it later


.. code-block:: python

   DEFAULT_CONF = {
      "config42" : {
            "file1": {
                "path": "local.yml"
            },
            "file2": {
                "path": "local.json"
            }
       },
      "port": 5001,
      "hostname": "localhost",
      "redis": {
        "host": "127.0.0.1",
        "port": 6379
      }
    }

   config = ConfigManager(defaults=DEFAULT_CONF)

You can use OrderedDict to ensure configuration overriding order.

.. code-block:: python

   from collections import OrderedDict
   nested_config = {'config42': OrderedDict(
                           [

                               ('file1', {'path': 'local.yml'}),
                               ('file2', {'path': '/etc/myapp/default.json'}),
                           ]
                       )
              }

Settings in the first handler ``('file1', {'path': 'local.yml'})`` overrides the others

Step 3: Configuration Validation
--------------------------------

Config42 uses Cerberus module to validate configuration content for you.
The config42 configuration schema is a list of dictionaries defining each setting.


.. code-block:: python

    schema = [
        dict(
            name="Hostname",
            key="hostname",
            description="HTTP Server Binding Hostname",
            required=False,
            default="localhost"
        ), dict(
            name="Application Port",
            key="port",
            type="integer",
            default=5000,
            description="HTTP Server biding port",
            required=False
        ), dict(
            name="Redis host",
            key="redis.host",
            description="Redis host",
            required=True,
            default="localhost"
        ), dict(
            name="Redis Port",
            key="redis.port",
            default=6379,
            type="integer",
            description="Redis Port",
            required=False
        )
    ]
    config = ConfigManager(schema=schema, defaults=DEFAULT_CONF)

See more :ref:`Configuration Schema`


Step 4: Run multiple instances of Shortly
-----------------------------------------

.. code-block:: bash

    ./shortly.py & ./shortly.py
    [1] 12345
    OSError: [Errno 48] Address already in use

You will get OSError, Telling you that the (address + port) are already in use
The issue is releated to our design, config42 is reading configuration only from
the default file  ``local.yml``

To do that we can keep the local.yml as a default configuration and override settings
from environments variables or command arguments.
*Default configuration file could be moved to* ``/etc/myapp/default.json``

Let's refactor the code to allow setting overload :

**From environment variables**

.. code-block:: bash

    C42_PORT=5002 ./shortly.py &
    C42_PORT=5003 ./shortly.py


**From command arguments**

.. code-block:: bash

    ./shortly.py --port=5002 &
    ./shortly.py --port=5003


We will use Environment and ArgParse Handler to read settings from environment variables
 and from command arguments.

ArgParse Handler uses the builtin **argparse** module


.. code-block:: python

   from collections import OrderedDict
   from config42.handlers import ArgParse
   nested_config = {'config42': OrderedDict(
                           [
                               ('argv', dict(handler=ArgParse, schema=schema)),
                               ('env', {'prefix': 'C42'}),
                               ('file', {'path': 'local.yml'}),
                           ]
                       )
              }
    config = ConfigManager(schema=schema, defaults=nested_config)

Our application will show help message if you call it with ``-h`` argument

.. code-block:: bash

    ./shortly.py -h

let's try to override the port number

.. code-block:: bash

    ./shortly.py --port 8081



Step 5: Run the application in docker container
-----------------------------------------------

Let's build a docker image for shortly.py.

`Please note that I made additional refactoring to the app.`

.. code-block:: bash

    docker build -t shortly .


Run Redis in docker

.. code-block:: bash

    docker run --rm -d -p6379:6379 redis


.. code-block:: bash

    docker run --rm --name shortly -e C42_VERBOSITY=2 -e C42_PORT=8080 -e C42_HOSTNAME=0.0.0.0 -p8080:8080  shortly
    # or using --env-file
    docker run --rm --name shortly --env-file shortly-docker-env -p8080:8080  shortly

Let's store the configuration in ETCD database.


.. code-block:: bash

    docker pull quay.io/coreos/etcd:v2.3.8
    docker run -d -v /usr/share/ca-certificates/:/etc/ssl/certs -p 4001:4001 -p 2380:2380 -p 2379:2379  --name etcd quay.io/coreos/etcd:v2.3.8  -name etcd0  -advertise-client-urls http://127.0.0.1:2379,http://127.0.0.1:4001  -listen-client-urls http://0.0.0.0:2379,http://0.0.0.0:4001  -initial-advertise-peer-urls http://127.0.0.1:2380  -listen-peer-urls http://0.0.0.0:2380  -initial-cluster-token etcd-cluster-1  -initial-cluster etcd0=http://127.0.0.1:2380  -initial-cluster-state new

let's set the Redis configuration and change the background color to green.

.. code-block:: bash

    config42 -l redis.host=172.17.0.3  redis.port=6379 hostname=0.0.0.0 port=8080 color=green -c etcd --etcd-keyspace=/shortly -a apply
    # Show the stored  configuration
    config42 -c etcd --etcd-keyspace=/shortly

.. code-block:: bash

    docker run --rm --name shortly -e C42_CONFIG42_ETCD_HOST=172.17.0.2 -e C42_CONFIG42_ETCD_KEYSPACE=/shortly -e C42_VERBOSITY=2 -p8080:8080  shortly

