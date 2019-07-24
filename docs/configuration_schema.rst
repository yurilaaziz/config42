====================
Configuration Schema
====================

.. _Configuration Schema:

name
====
*required*


description
===========
*optional*

Define the setting. This value is used by ArgParse handler to build the Command Help

Key
===
*required*

Define where the value will be stored

Choices
=======
*optional*

Define the allowed values

Sources
=======
*optional*

Contains additional parameters for Handlers.

.. list-table:: Source
   :widths: 25 25 25 50
   :header-rows: 1

   * - Name
     - Handler
     - Type
     - Description
   * - argv
     - Argparse
     - list
     - define the display name of the argument (['--format'])
   * - argv_options
     - Argparse
     - dict
     - define additional options for argparse.add_argument method


Required
========
*optional*

*default* : False

Specify if the value is required.

nullable
========
*optional*

*default* : False

Specify if the value is nullable.

default
========
*optional*

Specify if the default value if the setting is not set

type
========
*optional*

*default* : string

*Allowed values* : ['string', 'list', 'integer', 'boolean']

Specify the value's type.
