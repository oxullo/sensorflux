#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
sensorflux.database_connector
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains the class that communicates data to influxdb
"""

from copy import deepcopy
from datetime import datetime
from random import random

from influxdb import InfluxDBClient


class DatabaseConnector:
    """
    A class to represent a client connection to the influxdb instance

    :param str measurement: measurement name
    :param str device: name for the device tag
    :param tuple fields: name for the device tag
    """
    def __init__(
            self,
            measurement='test_measurement',
            device='test_device',
            fields=('temp', 'atmo', 'humi')):
        self.client = InfluxDBClient(
            host='localhost',
            port=8086,
            username='admin',
            password='admin',
            database='sensorflux')
        self.measurement = measurement
        self.device = device
        self.fields = fields

    def check_data(self, data):
        """
        Checks that the data is in a valid format. Returns true if yes

        :param dict data: measurement data
        :rtype: bool
        """
        right_type = isinstance(data, dict)
        has_data = any(key in data for key in self.fields)
        return right_type and has_data

    def clean_point(self, data):
        """
        Formats the data in the right format for influxdb

        :param dict data: measurement data
        :rtype: dict
        """
        data_copy = deepcopy(data)
        time = data_copy.pop('time') if 'time' in data_copy \
            else datetime.utcnow().isoformat()
        return {
            'measurement': self.measurement,
            'tags': {
                'device': self.device
            },
            'time': time,
            'fields': data_copy
        }

    def write(self, data):
        r"""
        Sends data to influxdb. Returns true if successful

        :param dict data: measurement data as a dict optionally
            containing a timestamp in ISO 8601 format, and containing
            any of 'temp', 'atmo' or 'humi' values
        :rtype: bool
        """
        assert self.check_data(data), 'wrong data format'
        point = self.clean_point(data)
        successful = self.client.write_points([point])
        return successful


if __name__ == '__main__':
    connector = DatabaseConnector(measurement='testing_database')

    fake_data = {
        # 'time': datetime.utcnow().isoformat(),
        'temp': random() * 100,
        'atmo': random() * 100,
        'humi': random() * 100,
    }

    print(connector.write(fake_data))
