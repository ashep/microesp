"""MicroPython REPL Client for ESP8266
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import binascii
from ampy.pyboard import Pyboard, PyboardError
from ampy.files import Files
from .error import DeviceNotConnectedError, DeviceCodeExecutionError
from .wlan import WLAN, IfType


class ESP8266:

    def __init__(self, port: str = '/dev/ttyUSB0', baud: int = 115200, timeout: int = 0):
        """Init
        """
        self._port = port
        self._baud = baud
        self._timeout = timeout
        self._dev = None  # type: Pyboard
        self._files = None  # type: Files
        self._wlan_ap = None  # type: WLAN
        self._wlan_sta = None  # type: WLAN

    def __enter__(self):
        """___enter___()
        """
        self.open()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """___exit___()
        """
        self.close()

    @property
    def unique_id(self) -> str:
        """Get unique device ID
        """
        uid = self.exec('import machine;print(machine.unique_id());', decode_output=False)

        return binascii.hexlify(uid).decode('utf-8')

    @property
    def wlan_ap(self) -> WLAN:
        """Get the WLAN access point interface
        """
        return self._wlan_ap

    @property
    def wlan_sta(self) -> WLAN:
        """Get the WLAN station interface
        """
        return self._wlan_sta

    @property
    def files(self) -> Files:
        """Files API
        """
        return self._files

    def open(self):
        """Initialize the board
        """
        self._dev = Pyboard(self._port, self._baud)
        self._dev.enter_raw_repl()

        self._files = Files(self._dev)
        self._wlan_ap = WLAN(self, IfType.AP)
        self._wlan_sta = WLAN(self, IfType.STA)

        return self

    def close(self):
        """Close connection to the board
        """
        self._dev.exit_raw_repl()
        self._dev.close()

        return self

    def exec(self, code: str, eval_response: bool = False, decode_output: bool = True):
        """Execute Python code on the board
        """
        if not self._dev:
            raise DeviceNotConnectedError('Device is not connected')

        data, data_err = self._dev.exec_raw(code)

        if data_err:
            raise DeviceCodeExecutionError(data_err.decode('utf-8'))

        if eval_response:
            return eval(data)
        else:
            return data.decode('utf-8') if decode_output else data

    def exec_file(self, f_path: str, decode_output: bool = True):
        """Execute Python code from a file on the board
        """
        if not self._dev:
            raise DeviceNotConnectedError('Device is not connected')

        try:
            r = self._dev.execfile(f_path)
            return r.decode('utf-8') if decode_output else r
        except PyboardError as e:
            raise DeviceCodeExecutionError(e.args[2].decode('utf-8') if decode_output else e.args[2])

    def reset(self):
        """Reset the board
        """
        self.exec('import machine;machine.reset()')

    def freq(self, f: int = None) -> int:
        """Get/set board's clock frequency
        """
        if not f:
            return self.exec('import machine;print(machine.freq())', True)
        else:
            self.exec('import machine;machine.freq({})'.format(f))
            return self.freq()
