#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
arduino.connector
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module contains the class that receives sensor values from Arduino.
"""

import random
from datetime import datetime
import logging

import serial_asyncio

logger = logging.getLogger(__name__)


class ArduinoConnectorBase:
    async def start(self):
        pass

    async def poll(self):
        pass


class ArduinoConnector(ArduinoConnectorBase):
    DEFAULT_BAUDRATE = 9600

    def __init__(self, serial_port, baudrate=None):
        self.serial_port = serial_port
        self.baudrate = self.DEFAULT_BAUDRATE if baudrate is None else baudrate
        self.arduino_connection = True
        self.reader = None
        self.writer = None

    async def start(self):
        self.reader, self.writer = await serial_asyncio.open_serial_connection(
            url=self.serial_port,
            baudrate=self.baudrate)

    async def poll(self):

        assert self.reader and self.writer, 'Arduino connector must be ' \
                                            'started first'

        self.writer.write(b'A')
        await self.writer.drain()
        try:
            incoming_bytes = (await asyncio.wait_for(self.reader.readline(),
                                                     timeout=2.0))
        except asyncio.TimeoutError:
            logger.warning('Arduino didn\'t reply')
            return None

        logger.debug(f'Arduino data {incoming_bytes}')
        list_of_strings = incoming_bytes.decode().split('\t')
        try:
            list_of_floats = [float(i) for i in list_of_strings]
        except ValueError:
            logger.warning('Converting strings into floats failed')
            return None

        sensor_values = {'time': 0, 'temp': 0, 'atmo': 0, 'height': 0}
        if len(list_of_floats) == 3:
            sensor_values['time'] = datetime.utcnow().isoformat()
            sensor_values['temp'] = list_of_floats[0]
            sensor_values['atmo'] = list_of_floats[1]
            sensor_values['height'] = list_of_floats[2]
            logger.debug(f'Here are your sensor values {sensor_values}')
            return sensor_values
        else:
            logger.warning('Wrong amount of values')
            return None


class ArduinoMockConnector(ArduinoConnectorBase):

    async def poll(self):
        return {'time': datetime.utcnow().isoformat(),
                'temp': float(random.randrange(-20, 40)),
                'atmo': float(random.randrange(930, 1300)),
                'humi': float(random.randrange(0, 100))}


if __name__ == '__main__':

    import asyncio

    async def main():
        mock = ArduinoConnector('/dev/cu.usbmodem146101')
        await mock.start()
        while True:
            print(await mock.poll())
            await asyncio.sleep(1)

    asyncio.run(main())
