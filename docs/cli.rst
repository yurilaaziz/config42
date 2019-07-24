=================
Config42 cli
=================

.. currentmodule:: config42

The config42 cli allows read, convert, update and delete configurations.


Display cli help
----------------

.. code-block:: bash

    config42 -h


Create a configuration file from literals
-----------------------------------------

.. code-block:: bash

    config42 -c output.yml -l user.name=Yuri user.id=1


You can create a JSON or INI file

.. code-block:: bash

    config42 -c output.json -l user.name=Yuri user.id=1
    config42 -c output.ini -l user.name=Yuri user.id=1

Create a configuration file from stdin
--------------------------------------

.. code-block:: bash

    cat output.json | config42 -c output.yml
    cat output.json | config42 -c output.ini



Read a configuration from etcd store
--------------------------------------

.. code-block:: bash

    config42 -c etcd --etcd-host=127.0.0.1 --etcd-port=4001 --etcd-keyspace=/config



Update a configuration to etcd store
--------------------------------------

.. code-block:: bash

    config42 -c etcd -f input.json --etcd-host=127.0.0.1 --etcd-port=4001  --etcd-keyspace=/config
    config42 -c etcd -f input.json -a merge --etcd-host=127.0.0.1 --etcd-port=4001  --etcd-keyspace=/config


Upload a configuration to etcd store
--------------------------------------

.. code-block:: bash

    config42 -c etcd -f input.json -a apply --etcd-host=127.0.0.1 --etcd-port=4001  --etcd-keyspace=/config


Remove a configuration from etcd store
--------------------------------------

.. code-block:: bash

    config42 -c etcd -a destroy --etcd-host=127.0.0.1 --etcd-port=4001  --etcd-keyspace=/config

