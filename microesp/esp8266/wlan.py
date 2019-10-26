"""ESP8266 WLAN Interface Abstraction
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import binascii
from typing import List, Tuple
from enum import IntEnum

IF_AP = 'AP_IF'
IF_STA = 'STA_IF'


class IfStatus(IntEnum):
    """Interface status
    """



class WLAN:
    def __init__(self, esp8266, if_type: str):
        """
        :type esp8266: microesp.esp8266.ESP8266
        """
        self._dev = esp8266

        if if_type not in (IF_AP, IF_STA):
            raise ValueError('Invalid interface type: {}'.format(if_type))

        self._if_name = 'wlan_{}'.format(if_type.replace('_IF', '').lower())
        self._dev.exec('import network;{}=network.WLAN(network.{});'.format(self._if_name, if_type))

    def is_active(self) -> bool:
        """Check whether interface is active
        """
        return self._dev.exec('print({}.active())'.format(self._if_name), True)

    def activate(self):
        """Activate interface interface
        """
        self._dev.exec('print(wlan_if.active(True))'.format(self._if_name), True)

    def deactivate(self):
        """Deactivate interface
        """
        self._dev.exec('print(wlan_if.active(False))'.format(self._if_name), True)

    def is_connected(self) -> bool:
        """Check if the interface is connected to a network
        """
        return self._dev.exec('print(wlan_if.isconnected())'.format(self._if_name), True)

    def config(self, param: str = None, **kwargs):
        """Get interface configuration parameter
        """
        if param:
            return self._dev.exec("print({}.config('{}'))".format(self._if_name, param))
        else:
            kwargs_str = ','.join("{}={}".format(k, repr(v)) for k, v in kwargs.items())
            return self._dev.exec("print({}.config({}))".format(self._if_name, kwargs_str))

    def status(self):
        """Get status of the interface
        """
        return self._dev.exec("print({}.status())".format(self._if_name), True)

    def connect(self, ap: str, passwd: str):
        """Connect to a network
        """
        return self._dev.exec('{}.connect("{}", "{}")'.format(self._if_name, ap, passwd))

    def disconnect(self):
        """Disconnect from the network
        """
        self._dev.exec('{}.disconnect()'.format(self._if_name))

    def ifconfig(self) -> Tuple[str, str, str, str]:
        """Get interface configuration

        Return value fields: IP address, subnet mask, gateway, DNS server
        """
        return self._dev.exec('print({}.ifconfig())'.format(self._if_name), True)

    def scan(self) -> List[Tuple[bytes, bytes, int, int, int, bool]]:
        """Scan for available access points

        Return value fields: SSID, BSSID, channel, RSSI, auth mode, hidden
        """
        ret = []
        for row in self._dev.exec('print({}.scan())'.format(self._if_name), True):
            ret.append((
                row[0].decode('utf-8'),  # SSID
                binascii.hexlify(row[1]).decode('utf-8'),  # BSSID
                row[2],  # Channel
                row[3],  # RSSI
                row[4],  # Auth mode
                bool(row[5]),  # Hidden
            ))

        return ret
