#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
sensorflux.database_connector
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains the class that communicates data to influxdb
"""

from copy import deepcopy
from datetime import datetime

from influxdb import InfluxDBClient


class DatabaseConnector:
    """
    A class to represent a client connection to the influxdb instance

    :param str measurement: measurement name
    :param str device: name for the device tag
    :param tuple fields: name for the device tag
    """
    def __init__(self, measurement, device, fields):
        self.client = InfluxDBClient(
            host='localhost',
            port=8086,
            username='admin',
            password='admin',
            database='sensorflux')
        self.measurement = measurement
        self.device = device
        self.fields = fields
        self._create_database('sensorflux')

    def _create_database(self, db_name):
        db_list = (el['name'] for el in self.client.get_list_database())
        if db_name not in db_list:
            self.client.create_database(db_name)

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

    def delete_data(self):
        self.client.delete_series(tags={'device': self.device})
