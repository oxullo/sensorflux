#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from random import random
import sys

from sensorflux.database_connector import DatabaseConnector
from sensorflux.polling_interface import PollingInterface


class FakeData:
    def __init__(self, fields):
        self._fields = fields

    def read(self):
        return {field: random() * 100 for field in self._fields}

    async def async_read(self):
        await asyncio.sleep(random() * 3)
        return self.read()


async def poller_manager(*instances):
    pollers = [PollingInterface(*instance) for instance in instances]
    tasks = [poller.run() for poller in pollers]
    await asyncio.gather(*tasks)


def run():
    fields = ('temp', 'atmo', 'humi')
    fake_client = FakeData(fields)
    db_client = DatabaseConnector(
        'test_measurement', 'test_device', fields)
    db_client_2 = DatabaseConnector(
        'test_measurement_2', 'test_device_2', fields)
    pollers_config = (
        (fake_client, db_client, 5),
        (fake_client, db_client_2, 3))

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
