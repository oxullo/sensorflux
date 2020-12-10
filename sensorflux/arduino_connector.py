#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
arduino.connector
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module contains the class that receives sensor values from Arduino.
"""

import re
import random
from datetime import datetime

import serial_asyncio


class ArduinoConnector:
    DEFAULT_BAUDRATE = 9600

    def __init__(self, serial_port, baudrate=None):
        self.serial_port = serial_port
        self.baudrate = self.DEFAULT_BAUDRATE if baudrate is None else baudrate
        self.arduino_connection = True
        self.reader = None

    async def start(self):
        self.reader, _ = await serial_asyncio.open_serial_connection(
            url=self.serial_port,
            baudrate=self.baudrate)

    async def read(self):
        assert self.reader, "Arduino connector must be started first"
        arduino_data = str(await self.reader.readline())
        print(f'Arduino data {arduino_data}')
        arduino_data = re.findall(r'\d+', arduino_data)
        print(f'Arduino data findall {arduino_data}')
        sensor_values = {'time': 0, 'temp': 0, 'atmo': 0, 'humi': 0}
        if len(arduino_data) == 3:
            sensor_values['time'] = datetime.utcnow().isoformat()
            sensor_values['temp'] = arduino_data[0]
            sensor_values['atmo'] = arduino_data[1]
            sensor_values['humi'] = arduino_data[2]
        return sensor_values


class ArduinoMockConnector:
    def __init__(self):
        pass

    async def poll(self):
        return {'time': datetime.utcnow().isoformat(),
                'temp': float(random.randrange(-20, 40)),
                'atmo': float(random.randrange(930, 1300)),
                'humi': float(random.randrange(0, 100))}


if __name__ == '__main__':

    import asyncio

    async def main():
        mock = ArduinoMockConnector()
        while True:
            print(await mock.poll())
            await asyncio.sleep(1)

    asyncio.run(main())
