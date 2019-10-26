"""MicroESP Errors
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ESP8266Error(Exception):
    pass


class DeviceNotConnectedError(ESP8266Error):
    pass

class DeviceCodeExecutionError(ESP8266Error):
    pass
