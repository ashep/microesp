"""MicroESP WLAN Tests
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re
import pytest
from typing import Tuple
from os import getenv
from time import sleep
from microesp.esp8266 import ESP8266
from microesp.esp8266.wlan import WLAN, IfType, IfStatus, IfConfigParam

_IP_ADDR_RE = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')


@pytest.fixture
def dev():
    return ESP8266()


@pytest.fixture()
def interfaces(dev: ESP8266) -> Tuple[WLAN, WLAN]:
    return WLAN(dev.open(), IfType.AP), WLAN(dev.open(), IfType.STA)


class TestWLAN:
    def test_init(self, dev: ESP8266):
        with dev:
            assert WLAN(dev, IfType.AP).if_type == IfType.AP
            assert WLAN(dev, IfType.STA).if_type == IfType.STA

    def test_activation(self, interfaces: Tuple[WLAN, WLAN]):
        for i in interfaces:
            i.deactivate()
            assert i.is_active == False

            i.activate()
            assert i.is_active == True

    def test_ifconfig(self, interfaces: Tuple[WLAN, WLAN]):
        for i in interfaces:
            ifcfg = i.ifconfig()
            assert len(ifcfg) == 4
            for n in ifcfg:
                _IP_ADDR_RE.match(n)

    def test_get_config(self, interfaces: Tuple[WLAN, WLAN]):
        for i in interfaces:
            for param in IfConfigParam:
                if param in (IfConfigParam.PASSWORD,):
                    with pytest.raises(TypeError):
                        i.get_config(param)
                elif i.if_type == IfType.AP:
                    if param in (IfConfigParam.DHCP_HOSTNAME,):
                        with pytest.raises(TypeError):
                            i.get_config(param)
                    else:
                        assert i.get_config(param) is not None
                elif i.if_type == IfType.STA:
                    if param in (IfConfigParam.CHANNEL, IfConfigParam.HIDDEN, IfConfigParam.AUTHMODE):
                        with pytest.raises(TypeError):
                            i.get_config(param)
                    else:
                        assert i.get_config(param) is not None

    def test_set_config(self, interfaces: Tuple[WLAN, WLAN]):
        for i in interfaces:
            for param in IfConfigParam:
                if i.if_type == IfType.STA:
                    with pytest.raises(TypeError):
                        i.set_config(param, 'value')


    def test_ap(self, interfaces: Tuple[WLAN, WLAN]):
        i = interfaces[0]

        assert i.status == IfStatus.STAT_UNKNOWN

        with pytest.raises(TypeError):
            i.connect('a', 'b')

        with pytest.raises(TypeError):
            i.disconnect()

        with pytest.raises(TypeError):
            i.scan()

    def test_sta(self, interfaces: Tuple[WLAN, WLAN]):
        i = interfaces[1]
        i.disconnect()
        assert i.is_connected() == False

        i.connect(getenv('MICROESP_STA_AP'), getenv('MICROESP_STA_PASSWD'))
        for n in range(10):
            if i.status == IfStatus.STAT_GOT_IP:
                break
            sleep(1)

        if i.status != IfStatus.STAT_GOT_IP:
            raise RuntimeError('Error while connecting to network. Check MICROESP_STA_* environment variables.')

        assert i.is_connected() == True

        scan = i.scan()
        assert isinstance(scan, list)
        for s in scan:
            assert len(s) == 6
            assert isinstance(s, tuple)
            assert isinstance(s[0], str)
            assert isinstance(s[1], str)
            assert isinstance(s[2], int)
            assert isinstance(s[3], int)
            assert isinstance(s[4], int)
            assert isinstance(s[5], bool)
