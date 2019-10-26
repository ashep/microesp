"""MicroESP Core Tests
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pytest
import time
from microesp.esp8266 import ESP8266
from microesp.esp8266.wlan import WLAN
from microesp.esp8266.error import DeviceNotConnectedError, DeviceCodeExecutionError
from ampy.files import Files


class TestCore:
    def test_open_close(self):
        # Using context manager
        with ESP8266() as dev:
            assert isinstance(dev.unique_id, str)
            assert isinstance(dev.files, Files)
            assert isinstance(dev.wlan_ap, WLAN)
            assert isinstance(dev.wlan_sta, WLAN)

    def test_exec(self):
        # Try to execute code on a non-connected device
        dev = ESP8266()
        with pytest.raises(DeviceNotConnectedError):
            dev.exec('print()')

        with ESP8266() as dev:
            # Execute without response evaluation
            assert dev.exec("print('Hello world')") == 'Hello world\r\n'

            # Execute with response evaluation
            for v in (None, True, False, 1, 1.0, -1, -1.0, 'a', list(), tuple(), set(), dict()):
                assert dev.exec("print(repr({}), end='')".format(repr(v)), True) == v

            # Syntax error
            with pytest.raises(DeviceCodeExecutionError):
                dev.exec("Erroneous code")

    def test_exec_file(self):
        # Try to execute code on a non-connected device
        dev = ESP8266()
        with pytest.raises(DeviceNotConnectedError):
            dev.exec_file('tests/mock_code.py')

        with ESP8266() as dev:
            assert dev.exec_file('tests/mock_code.py') == 'Hello world\r\n'

            with pytest.raises(DeviceCodeExecutionError):
                dev.exec_file('tests/mock_bad_code.py')

    def test_freq(self):
        with ESP8266() as dev:
            assert dev.freq() == 80000000
            assert dev.freq(160000000) == 160000000
            assert dev.freq(80000000) == 80000000  # Switch back to 80MHz to prevent power wasting during next tests

    def test_reset(self):
        with ESP8266() as dev:
            assert dev.reset() is None
            time.sleep(3)
