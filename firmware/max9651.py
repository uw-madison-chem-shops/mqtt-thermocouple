from machine import Pin, I2C, SPI
import time



class MAX9651(object):

    def __init__(self):
        self.spi = SPI(sck=Pin(14), mosi=Pin(13), miso=Pin(15), baudrate=50_000, polarity=0)
        self.cs = Pin(12, mode=Pin.OUT, value=1)
        self._write_bytes(b"\x01\xFF")  # enable decode mode
        self._write_bytes(b"\x02\x7F")  # intensity
        self._write_bytes(b"\x03\x03")  # display four digits
        self._write_bytes(b"\x04\x21")  # clear

    def show(self, num: float):
        string = "{:.1f}".format(num)
        string = ("0" * (5 - len(string))) + string
        self._write_bytes(b"\x60" + int(string[0]).to_bytes(1, "big"))
        self._write_bytes(b"\x61" + int(string[1]).to_bytes(1, "big"))
        self._write_bytes(b"\x62" + (int(string[2]) | 128).to_bytes(1, "big"))
        self._write_bytes(b"\x63" + int(string[4]).to_bytes(1, "big"))

    def _write_bytes(self, data: bytes):
        time.sleep(0.01)
        self.cs(0)
        time.sleep(0.01)
        self.spi.write(data)
        time.sleep(0.01)
        self.cs(1)
        time.sleep(0.01)
