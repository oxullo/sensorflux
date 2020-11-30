#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from sensorflux.database_connector import DatabaseConnector


def test_check_data():
    """
    GIVEN data to be sent to influxdb
    WHEN the method is called with data as an argument
    THEN it should only return True if the data is valid
    """
    connector = DatabaseConnector(
        measurement='measurement',
        device='device',
        fields=('temp', 'atmo', 'humi'))

    assert connector.check_data({
        'time': datetime.utcnow().isoformat(),
        'temp': 123,
        'atmo': 456,
        'humi': 789}) is True
    assert connector.check_data({
        'time': datetime.utcnow().isoformat(),
        'humi': 789}) is True
    assert connector.check_data({'temp': 123, 'atmo': 789}) is True
    assert connector.check_data({}) is False
    assert connector.check_data(
        (datetime.utcnow().isoformat(), 123, 456)) is False
    assert connector.check_data(
        [datetime.utcnow().isoformat(), 987, 654]) is False
