#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio

from arduino_connector import ArduinoConnector


class DatabaseConnectorFake:

    def write(self, data):
        print(f'This is Values in write function {data}')


if __name__ == '__main__':
    newArduinoConnector = ArduinoConnector('/dev/cu.usbmodem145101', 9600, 2)
    newArduinoConnector.start_ardunio_connect()
    newDatabaseConnection = DatabaseConnectorFake()
    asyncio.run(newArduinoConnector.task1(newDatabaseConnection.write))
    asyncio.sleep(4)
