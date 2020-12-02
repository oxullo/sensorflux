#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
arduino.connector
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module contains the class that receives sensor values from Arduino.
"""

import serial
import asyncio
import re
from datetime import datetime
import random


class ArduinoConnector:
    def __init__(self, serial_port, baudrate, sample_rate):
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.sample_rate = sample_rate
        self.arduino_connection = True

    def start_ardunio_connect(self):
        try:
            self.ser = serial.Serial(self.serial_port, self.baudrate)
        except serial.SerialException:
            self.arduino_connection = False

    async def arduino_read(self):
        arduino_data = str(self.ser.readline())
        print(f'Arduino data {arduino_data}')
        arduino_data = re.findall(r'\d+', arduino_data)
        print(f'Arduino data findall {arduino_data}')
        sensor_values = {'time': 0, 'temp': 0, 'atmo': 0, 'humi': 0}
        if len(arduino_data) == 3:
            sensor_values['time'], sensor_values['temp'],
            sensor_values['atmo'],
            sensor_values['humi'] = datetime.utcnow().isoformat(),
            arduino_data[0], arduino_data[1], arduino_data[2]
        await asyncio.sleep(self.sample_rate)
#        print(f'are we getting here? {sensor_values}')
        return sensor_values

    async def backup_vaule_gen(self):
        temp = random.randint(1, 255)
        atmo = random.randint(1, 255)
        humi = random.randint(1, 255)
        time = datetime.utcnow().isoformat()
        await asyncio.sleep(self.sample_rate)
        return [time, temp, atmo, humi]

    async def task1(self, value_send_out):
        while True:
            if self.arduino_connection:
                sensor_values = await self.arduino_read()
#               print(f'Task1 sensor {sensor_values}')
                value_send_out(sensor_values)
            else:
                sensor_values = await self.backup_vaule_gen()
                value_send_out(sensor_values)

    # async def main(self):
    #     test = asyncio.create_task(self.task1())
    #     await asyncio.sleep(1)
