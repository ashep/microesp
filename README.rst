MicroESP
========

**MicroESP** is a wrapper library over `Adafruit MicroPython Tool (ampy)`_. MicroESP is meant to be a simple convenient
Python library with clear API to manipulate files and run code on ESP8266 MicroPython powered boards.


Installation
------------

.. sourcecode:: bash

    python -m venv ./env
    source ./env/bin/activate
    pip install -r ./requirements.txt


Usage examples
--------------

Connect to a board via ``/dev/ttyUSB0`` port on ``115200`` baud rate:

.. sourcecode:: python

    from microesp.esp8266 import ESP8266

    dev = ESP8266()
    dev.open()
    dev.close()

Or using ``with`` statement:

.. sourcecode:: python

    from microesp.esp8266 import ESP8266

    with ESP8266() as dev:
        pass


.. _Adafruit MicroPython Tool (ampy): https://github.com/scientifichackers/ampy
