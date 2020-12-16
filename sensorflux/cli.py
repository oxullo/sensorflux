#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import sys

from sensorflux.arduino_connector import ArduinoConnector, ArduinoMockConnector
from sensorflux.database_connector import DatabaseConnector
from sensorflux.polling_interface import PollingInterface


async def poller_manager(*instances):
    pollers = [PollingInterface(*instance) for instance in instances]
    tasks = [poller.run() for poller in pollers]
    start_arduinos = [instance[0].start() for instance in instances]
    await asyncio.gather(*start_arduinos, *tasks)


def run():
    fields = ('temp', 'atmo', 'humi')
    arduino_client = ArduinoConnector('/dev/cu.usbmodem146101')
    arduino_mock = ArduinoMockConnector()
    db_client = DatabaseConnector(
        'test_measurement', 'test_device', fields)
    db_client_2 = DatabaseConnector(
        'test_measurement_2', 'test_device_2', fields)
    pollers_config = (
        (arduino_client, db_client, 5),
        (arduino_mock, db_client_2, 3))

    try:
        asyncio.run(poller_manager(*pollers_config))
    except KeyboardInterrupt:
        print('shutting down')
        return 0
    except AttributeError as e:
        print(e)
    return 1


if __name__ == '__main__':
    sys.exit(run())
