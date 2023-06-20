Core Main Registry App
======================

This Django reusable app contains the main functionalities for the registry core project.

Pre-requisites
==============

* Install git
* Install python
* Install pip
* Create a virtual env

Installation
============

Automated installation
----------------------

.. warning::

    *The automated installation is not yet available.*

Manual installation
-------------------

.. code:: bash

    $ git clone https://myrepo.com/core_main_registry_app.git
    $ cd core_main_registry_app
    $ python setup.py
    $ pip install sdist/*.tar.gz


Configuration
=============

1. Add "core_main_registry_app", "mptt" to your INSTALLED_APPS setting like this
---------------------------------------------------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
        ...
        "core_main_registry_app",
        "mptt",
    ]

2. Include the core_main_registry_app URLconf in your project urls.py like this
-------------------------------------------------------------------------------

.. code:: python

    url(r'^', include("core_main_registry_app.urls")),


3. Launch migration: create table and constraints.
--------------------------------------------------

    $ python manage.py migrate
