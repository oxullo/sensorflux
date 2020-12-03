#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
sensorflux.database_connector
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains the class that communicates data to influxdb.
"""

from datetime import datetime
import logging

from influxdb import InfluxDBClient

logger = logging.getLogger(__name__)


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
        self._ensure_database()
        logger.info(f'Instance of DatabaseConnector created for device: '
                    f'{self.device} at: {self.host}:{self.port}')

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

    def _ensure_database(self):
        db_list = (el['name'] for el in self.client.get_list_database())
        if self.database_name not in db_list:
            logger.info(f'Creating new database named: {self.database_name}')
            self.client.create_database(self.database_name)

    def check_data(self, data):
        """
        Checks that the data is in a valid format. Returns true if yes.

        :param dict data: measurement data.
        :rtype: bool
        """
        right_type = isinstance(data, dict)
        has_data = any(key in data for key in self.fields)
        is_valid = right_type and has_data
        if not is_valid:
            logger.warning(f'The data is not in a valid format: {data}')
        return is_valid

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
        if successful:
            logger.debug('Successfully sent data')
        else:
            logger.warning('Data could not be sent')
        return successful

    def delete_data(self):
        self.client.delete_series(tags={'device': self.device})
        logger.info(f'Deleted data for device: {self.device}')
