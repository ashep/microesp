"""ESP8266 WLAN Interface Abstraction
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import binascii
from typing import List, Tuple
from enum import Enum, IntEnum


class IfType(Enum):
    AP = 'AP_IF'
    STA = 'STA_IF'


class IfStatus(IntEnum):
    """Interface statuses
    """
    STAT_UNKNOWN = -1
    STAT_IDLE = 0
    STAT_CONNECTING = 1
    STAT_WRONG_PASSWORD = 2
    STAT_NO_AP_FOUND = 3
    STAT_CONNECT_FAIL = 4
    STAT_GOT_IP = 5


class NetStatus(IntEnum):
    """WiFi network statuses
    """
    VISIBLE = 0
    HIDDEN = 1


class NetAuthMode(IntEnum):
    """WiFi network authentication modes
    """
    OPEN = 0
    WEP = 1
    WPA_PSK = 2
    WPA2_PSK = 3
    WPA_WPA2_PSK = 4


class IfConfigParam(Enum):
    MAC = 'mac'
    ESSID = 'essid'
    CHANNEL = 'channel'
    HIDDEN = 'hidden'
    AUTHMODE = 'authmode'
    PASSWORD = 'password'
    DHCP_HOSTNAME = 'dhcp_hostname'


class WLAN:
    def __init__(self, esp8266, if_type: IfType):
        """
        :type esp8266: microesp.esp8266.ESP8266
        """
        self._dev = esp8266
        self._if_type = if_type
        self._if_name = 'wlan_{}'.format(if_type.value.rstrip('_IF').lower())
        self._dev.exec('import network;{}=network.WLAN(network.{});'.format(self._if_name, if_type.value))

    @property
    def if_type(self) -> IfType:
        """Get interface type
        """
        return self._if_type

    @property
    def is_active(self) -> bool:
        """Check whether interface is active
        """
        return self._dev.exec('print({}.active())'.format(self._if_name), True)

    @property
    def status(self) -> IfStatus:
        """Get status of the interface
        """
        return IfStatus(self._dev.exec("print({}.status())".format(self._if_name), True))

    def activate(self):
        """Activate interface interface
        """
        self._dev.exec('print({}.active(True))'.format(self._if_name), True)

    def deactivate(self):
        """Deactivate interface
        """
        self._dev.exec('print({}.active(False))'.format(self._if_name), True)

    def is_connected(self) -> bool:
        """Check if the interface is connected to a network
        """
        return self._dev.exec('print({}.isconnected())'.format(self._if_name), True)

    def connect(self, ap: str, passwd: str):
        """Connect to a network
        """
        if self._if_type != IfType.STA:
            raise TypeError('Only STA interface may use connect() method')

        return self._dev.exec('{}.connect("{}", "{}")'.format(self._if_name, ap, passwd))

    def disconnect(self):
        """Disconnect from the network
        """
        if self._if_type != IfType.STA:
            raise TypeError('Only STA interface may use connect() method')

        self._dev.exec('{}.disconnect()'.format(self._if_name))

    def get_config(self, param: IfConfigParam):
        """Get interface configuration parameter
        """
        if param in (IfConfigParam.PASSWORD,):
            raise TypeError('{} config parameter cannot be gotten'.format(param.name))

        only_sta = (IfConfigParam.DHCP_HOSTNAME,)
        if self._if_type != IfType.STA and param in only_sta:
            raise TypeError('Only STA interface can return {} config parameter'.format(param.name))

        only_ap = (IfConfigParam.CHANNEL, IfConfigParam.HIDDEN, IfConfigParam.AUTHMODE)
        if self._if_type != IfType.AP and param in only_ap:
            raise TypeError('Only AP interface can return {} config parameter'.format(param.name))

        return self._dev.exec("print(repr({}.config('{}')))".format(self._if_name, param.value), True)

    def set_config(self, param: IfConfigParam, value):
        """Set interface configuration parameter
        """
        if self._if_type != IfType.AP:
            raise TypeError('Only AP interface can set {} config parameter'.format(param.name))

        code = "print({}.config({}={}))".format(self._if_name, param.value, repr(value))  # pragma: no cover
        return self._dev.exec(code)  # pragma: no cover

    def ifconfig(self) -> Tuple[str, str, str, str]:
        """Get interface configuration

        Return value fields: IP address, subnet mask, gateway, DNS server
        """
        return self._dev.exec('print({}.ifconfig())'.format(self._if_name), True)

    def scan(self) -> List[Tuple[str, str, int, int, int, bool]]:
        """Scan for available access points

        Return value fields: SSID, BSSID, channel, RSSI, auth mode, hidden
        """
        if self._if_type != IfType.STA:
            raise TypeError('Only STA interface may use scan() method')

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
