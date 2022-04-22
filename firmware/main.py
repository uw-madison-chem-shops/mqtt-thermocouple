import settings

import sys
import machine
from machine import Pin, I2C, SPI
import network
import time
import struct

import mqtt_as
mqtt_as.MQTT_base.DEBUG = True



from homie.constants import FALSE, TRUE, BOOLEAN, FLOAT, STRING
from homie.device import HomieDevice
from homie.node import HomieNode
from homie.property import HomieNodeProperty

from uasyncio import get_event_loop, sleep_ms


from max9651 import MAX9651



def temp_c(byteData):
    # Taken from MCP9600 Datasheet:
    # Temperature >= 0°C
    # TΔ = (UpperByte x 16 + LowerByte / 16)
    # Temperature < 0°C
    # TΔ = (UpperByte x 16 + LowerByte / 16) - 4096

    temp = (byteData[0] * 16 + byteData[1] / 16)
    value = byteData[0] << 8 | byteData[1]

    if value & 0x1000:
        temp -= 4096.0
    return temp



class TemperatureSensor(HomieNode):

    def __init__(self, name="thermocouple", device=None):
        super().__init__(id="thermocouple", name=name, type="sensor")
        self.device = device
        self.i2c = I2C(scl=Pin(5), sda=Pin(4))
        self.display = MAX9651()
        self.temperature = HomieNodeProperty(
            id="temperature",
            name="temperature",
            unit="°C",
            settable=False,
            datatype=FLOAT,
            default=0,
        )
        self.add_property(self.temperature)
        self.uptime = HomieNodeProperty(
            id="uptime",
            name="uptime",
            settable=False,
            datatype=STRING,
            default="PT0S"
        )
        self.add_property(self.uptime)
        self.ip = HomieNodeProperty(
            id="ip",
            name="ip",
            settable=False,
            datatype=STRING,
            default="",
        )
        self.add_property(self.ip)
        self.led = Pin(0, Pin.OUT)
        self.online_led = Pin(15, Pin.OUT)
        self.online_led.off()
        self.last_online = time.time()
        self.start = time.time()
        print("start time", self.start)
        self.measured_temps = []
        loop = get_event_loop()
        loop.create_task(self.measure_temp())
        loop.create_task(self.update_data())

    async def update_data(self):
        # wait until connected
        for _ in range(60):
            print("wait until connected")
            await sleep_ms(1_000)
            if self.device.mqtt.isconnected():
                break
        # loop forever
        while True:
            while self.device.mqtt.isconnected():
                print("update data")
                print(network.WLAN().status())
                self.last_online = time.time()
                print(1)
                self.online_led.on()
                print(2)
                self.led.value(0)  # illuminate onboard LED
                self.temperature.data = str(sum(self.measured_temps) / len(self.measured_temps))
                self.measured_temps = []
                self.uptime.data = self.get_uptime()
                self.ip.data = network.WLAN().ifconfig()[0]
                self.led.value(1)  # onboard LED off
                print("final")
                await sleep_ms(15_000)
            while not self.device.mqtt.isconnected():
                print("wait for reconnect")
                if time.time() - self.last_online > 300:   # 5 minutes
                    machine.reset()
                self.online_led.off()
                self.led.value(0)  # illuminate onboard LED
                await sleep_ms(100)
                self.led.value(1)  # onboard LED off
                await sleep_ms(1000)
            machine.reset()  # if lost connection, restart

    async def measure_temp(self):
        while True:
            temp = temp_c(self.i2c.readfrom_mem(0b0110_0000, 0b0000_0000, 2))
            print(temp)
            self.display.show(temp)
            self.measured_temps.append(temp)
            await sleep_ms(500)


    def get_uptime(self):
        diff = int(time.time() - self.start)
        out = "PT"
        # hours
        if diff // 3600:
            out += str(diff // 3600) + "H"
            diff %= 3600
        # minutes
        if diff // 60:
            out += str(diff // 60) + "M"
            diff %= 60
        # seconds
        out += str(diff) + "S"
        return out

def main():
    print("homie main")
    homie = HomieDevice(settings)
    homie.add_node(TemperatureSensor(device=homie))
    homie.run_forever()


if __name__ == "__main__":
    main()
