==============
Config Manager
==============

.. module:: config42.config_manager

Config42  is a complete configuration reader and manager. It aims to read the configuration from different sources: a memory Dict object, an external file ( YAML, JSON, INI, PYTHON Object ), an SQL database (Postgres, MySQL, Oracle)
alternatively, Key-value data store ( Etcd )

It is designed to be extensible. Different handlers could support another data store.


.. autoclass:: ConfigManager
   :members:


