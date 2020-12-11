#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
sensorflux.database_connector
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains the class that communicates data to influxdb.
"""

from datetime import datetime

from influxdb import InfluxDBClient


class DatabaseConnector:
    """
    A class to represent a client connection to the influxdb instance.

    :param str measurement: measurement name.
    :param str device: name for the device tag.
    :param tuple fields: names of the fields containing the data to be sent.
    """
    host = 'localhost'
    port = 8086
    username = 'admin'
    password = 'admin'
    database_name = 'sensorflux'

    def __init__(self, measurement, device, fields):
        self._client = InfluxDBClient(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            database=self.database_name)
        self._measurement = measurement
        self._device = device
        self._fields = fields

    @property
    def client(self):
        return self._client

    @property
    def measurement(self):
        return self._measurement

    @property
    def device(self):
        return self._device

    @property
    def fields(self):
        return self._fields

    def check_data(self, data):
        """
        Checks that the data is in a valid format. Returns true if yes.

        :param dict data: measurement data.
        :rtype: bool
        """
        right_type = isinstance(data, dict)
        has_data = any(key in data for key in self.fields)
        return right_type and has_data

    def data_to_point(self, data):
        """
        Formats the data in the right format for influxdb.

        :param dict data: measurement data.
        :rtype: dict
        """
        time = data['time'] if 'time' in data \
            else datetime.utcnow().isoformat()
        fields = {key: value for key, value in data.items() if key != 'time'}
        return {
            'measurement': self.measurement,
            'tags': {
                'device': self.device
            },
            'time': time,
            'fields': fields
        }

    def write(self, data):
        r"""
        Sends data to influxdb. Returns true if successful.

        :param dict data: measurement data as a dict optionally
            containing a timestamp in ISO 8601 format, and containing
            any of 'temp', 'atmo' or 'humi' values.
        :rtype: bool
        """
        if not self.check_data(data):
            return False
        point = self.data_to_point(data)
        successful = self.client.write_points([point])
        return successful
