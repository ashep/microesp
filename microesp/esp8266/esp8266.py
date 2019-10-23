"""MicroPython REPL Client for ESP8266
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from ampy.pyboard import Pyboard, PyboardError
from ampy.files import Files
from .wlan import WLAN, WLAN_AP, WLAN_STA


class ESP8266:

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

    def open(self):
        """Initialize the board
        """
        self._dev = Pyboard(self._port, self._baud)
        self._dev.enter_raw_repl()

        self._files = Files(self._dev)
        self._wlan_ap = WLAN(self, WLAN_AP)
        self._wlan_sta = WLAN(self, WLAN_STA)

    def close(self):
        """Close connection to the board
        """
        self._dev.exit_raw_repl()
        self._dev.close()

    def exec(self, code: str, eval_response: bool = False):
        """Execute Python code on the board
        """
        if not self._dev:
            raise RuntimeError('Device is not connected')

        data, data_err = self._dev.exec_raw(code)

        if data_err:
            raise RuntimeError(data_err.decode('utf-8'))

        if eval_response:
            data = eval(data)

        return data

    def exec_file(self, f_path: str):
        """Execute Python code from a file on the board
        """

        try:
            return self._dev.execfile(f_path).decode('utf-8')
        except PyboardError as e:
            print(e)

    def reset(self):
        """Reset the board
        """
        self.exec('import machine;machine.reset()')

    def freq(self):
        """Get current board's frequency
        """
        return self.exec('import machine;print(machine.freq())', True)
