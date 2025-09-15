weather-api
===========

.. image:: https://github.com/amikrop/weather-api/actions/workflows/main.yml/badge.svg
   :target: https://github.com/amikrop/weather-api/actions/
   :alt: Workflows

This is a demo backend providing basic weather station and measurement management, made using Django REST Framework.

It is tested for Python versions 3.8 - 3.12.

Usage
-----

Build and run the Docker containers:

.. code-block:: bash

   $ docker compose up --build

Schema
------

API schema documentation can be accessed at:

- `http://localhost:8000/schema/`
- `http://localhost:8000/schema/swagger-ui/`
- `http://localhost:8000/schema/redoc/`

Unit tests
----------

Multiple Python versions
************************

Run the tests for all supported Python versions found in your system, using `tox <https://tox.wiki/>`_:

.. code-block:: bash

   $ cd app
   $ tox

In-container
************

Once you have started the Docker app, you can run the tests for the containerized deployment:

.. code-block:: bash

   $ docker compose run web pytest

Settings
--------

There are two groups of configuration settings:

- **Application settings**: values that control app logic (e.g. valid ranges for temperature or rainfall).
- **Infrastructure settings**: values required for Django and its services to run (database, secret key, debug flags, etc.).

Priority of sources
*******************

Settings are resolved in the following order (highest priority first):

1. Explicit values in ``settings.py``
   A developer may define a ``WEATHER = {...}`` dictionary to override application settings.

2. Environment variables
   Variables prefixed with ``WEATHER_`` override the defaults for individual application settings.
   Standard Django-related environment variables (``SECRET_KEY``, ``DEBUG``, ``SQL_*``) configure infrastructure.

3. Defaults
   If nothing else is provided, built-in defaults are used.

Environment files
*****************

- When running outside Docker, the project automatically reads a local ``.env`` file (if present).
  This file is not versioned and is intended for developer convenience.

- When running in Docker, ``docker-compose.yml`` is configured to load ``.env.dev`` (versioned).
  This provides a working baseline for local development in containers.
  Developers may still provide additional runtime environment variables to override these defaults.

Application settings
********************

These control domain validation logic used by serializers and models.

=================== ============================== ======== ==================================================
Name                Environment variable           Default  Description
=================== ============================== ======== ==================================================
``ELEVATION_MIN``   ``WEATHER_ELEVATION_MIN``      ``-500`` Minimum elevation (meters) allowed for a station
``ELEVATION_MAX``   ``WEATHER_ELEVATION_MAX``      ``9000`` Maximum elevation (meters) allowed for a station
``TEMPERATURE_MIN`` ``WEATHER_TEMPERATURE_MIN``    ``-90``  Minimum temperature (°C) allowed for a measurement
``TEMPERATURE_MAX`` ``WEATHER_TEMPERATURE_MAX``    ``60``   Maximum temperature (°C) allowed for a measurement
``WIND_SPEED_MAX``  ``WEATHER_WIND_SPEED_MAX``     ``100``  Maximum wind speed (m/s) allowed for a measurement
``RAINFALL_MAX``    ``WEATHER_RAINFALL_MAX``       ``500``  Maximum rainfall (mm) allowed for a measurement
=================== ============================== ======== ==================================================

Infrastructure settings
***********************

These are standard Django configuration values.
They are normally set via environment variables and rarely need to be overridden directly in ``settings.py``.

=============================== ======================== =================================================
Name                            Environment variable     Default
=============================== ======================== =================================================
``SECRET_KEY``                  ``SECRET_KEY``           ``" "`` (must be set in production)
``DEBUG``                       ``DEBUG``                ``True``
``ALLOWED_HOSTS``               ``DJANGO_ALLOWED_HOSTS`` ``[]``
``SQL_ENGINE``                  ``SQL_ENGINE``           ``"django.db.backends.sqlite3"``
``SQL_USER``                    ``SQL_USER``             ``""``
``SQL_PASSWORD``                ``SQL_PASSWORD``         ``""``
``SQL_DATABASE``                ``SQL_DATABASE``         ``"db.sqlite3"`` (or in-memory for tests)
``SQL_HOST``                    ``SQL_HOST``             ``""``
``SQL_PORT``                    ``SQL_PORT``             ``""``
``REST_FRAMEWORK["PAGE_SIZE"]`` ``DJANGO_PAGE_SIZE``     ``100`` (default page size for paginated results)
=============================== ======================== =================================================
