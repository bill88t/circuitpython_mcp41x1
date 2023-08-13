from time import sleep
import digitalio
from adafruit_bus_device.spi_device import SPIDevice
from busio import SPI


class mcp41x1:
    def __init__(self, clk, miso, mosi, cs, wiper: int = 0) -> None:
        # half_duplex=True not implemented
        self._spi = SPI(clk, miso, mosi)
        del clk, miso, mosi
        chip_sel = digitalio.DigitalInOut(cs)
        del cs
        self._device = SPIDevice(self._spi, chip_sel, baudrate=1000000)
        del chip_sel

        # Bootup delay
        sleep(0.03)

        # Set initial wiper value
        self._wiper = wiper
        self._set()
        del wiper
        self._deinited = False

    @property
    def wiper(self) -> int:
        self._deinit_ch()
        return self._wiper

    @wiper.setter
    def wiper(self, value: int) -> None:
        self._deinit_ch()
        if value < 0 or value > 128:  # Yes. Not 127.
            raise ValueError("Wiper value must be from 0 to 128")
        self._wiper = value
        self._set()

    def deinit(self) -> None:
        self._deinit_ch()
        del self._device
        del self._spi
        self._deinited = True

    # Internal functions

    def _set(self) -> None:
        with self._device as spi:
            spi.write(bytes([0, self._wiper]))

    def _deinit_ch(self) -> None:
        if self._deinited:
            raise AttributeError(
                "This object has been deinitialized. Please create a new one."
            )
