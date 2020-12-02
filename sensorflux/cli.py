#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import random
import sys

from sensorflux.database_connector import DatabaseConnector
from sensorflux.polling_interface import PollingInterface


class FakeData:
    def __init__(self, fields):
        self._fields = fields

    def read(self):
        return {field: random() * 100 for field in self._fields}


def run():
    fields = ('temp', 'atmo', 'humi')
    fake_client = FakeData(fields)
    db_client = DatabaseConnector('test_measurement', 'test_device', fields)
    poller = PollingInterface(fake_client, db_client, 5)
    try:
        poller.run()
    except KeyboardInterrupt:
        print('shutting down')
        return 0
    except AttributeError as e:
        print(e)
    return 1


if __name__ == '__main__':
    sys.exit(run())
