#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from sensorflux.database_connector import DatabaseConnector


def test_check_data():
    """
    GIVEN data as a parameter to be sent to influxdb
    WHEN the data is not valid
    THEN it should return false
    """
    connector = DatabaseConnector()

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
