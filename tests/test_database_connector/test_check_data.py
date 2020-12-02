#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

import pytest

from sensorflux.database_connector import DatabaseConnector


@pytest.fixture()
def connector():
    connector_instance = DatabaseConnector(
        measurement='measurement',
        device='device',
        fields=('temp', 'atmo', 'humi'))
    return connector_instance


def test_check_data(connector):
    """
    GIVEN data to be sent to influxdb
    WHEN the method is called with data as an argument
    THEN it should only return True if the data is valid
    """
    assert connector.check_data({
        'time': datetime.utcnow().isoformat(),
        'temp': 123,
        'atmo': 456,
        'humi': 789})
    assert connector.check_data({
        'time': datetime.utcnow().isoformat(),
        'humi': 789})
    assert connector.check_data({'temp': 123, 'atmo': 789})
    assert not connector.check_data({})
    assert not connector.check_data(
        (datetime.utcnow().isoformat(), 123, 456))
    assert not connector.check_data(
        [datetime.utcnow().isoformat(), 987, 654])
