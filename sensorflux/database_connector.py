#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import deepcopy
from datetime import datetime
from random import random

from influxdb import InfluxDBClient


class DatabaseConnector:
    def __init__(self, measurement='test_measurement', device='test_device'):
        self.client = InfluxDBClient(
            host='localhost',
            port=8086,
            username='admin',
            password='admin',
            database='sensorflux')
        self.measurement = measurement
        self.device = device

    @staticmethod
    def check_data(data):
        right_type = isinstance(data, dict)
        has_data = any(key in data for key in ('temp', 'atmo', 'humi'))
        return right_type and has_data

    def clean_point(self, data):
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
