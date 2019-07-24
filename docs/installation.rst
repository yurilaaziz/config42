.. _installation:

Installation
============


Python Version
--------------

We recommend using the latest version of Python 3. Config42 supports
only Python 3.4 and newer.


Dependencies
------------

Config42 have direct dependencies with
* Pyyaml for YAML parsing
* Jinja2: for configuration templating
* Cerberus : for configuration content and content validation


Virtual environments
--------------------

Use a virtual environment to manage the dependencies for your project,
both in development and in production.


Install Config42
----------------

Within the activated environment, use the following command to install
config42:

.. code-block:: sh

    pip install config42


Living on the edge
~~~~~~~~~~~~~~~~~~

If you want to work with the latest Config42 code before it's released,
install or update the code from the master branch:

.. code-block:: sh

    pip install -U https://github.com/yurilaaziz/config42/archive/master.tar.gz


.. _install-install-virtualenv:
