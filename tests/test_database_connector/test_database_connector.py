#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import random

from influxdb import client

from sensorflux.database_connector import DatabaseConnector


def client_params():
    measurement = f'measurement_{str(random())[2:]}'
    device = f'device_{str(random())[2:]}'
    connector_instance = DatabaseConnector(
        measurement=measurement,
        device=device,
        fields=(666, 777, 888))
    yield connector_instance
    yield connector_instance.client.drop_measurement(measurement)


def test_database_connector():
    """
    GIVEN the DatabaseConnector class
    WHEN you instantiate it
    THEN it should return a valid InfluxDBClient object
    """
    params_gen = client_params()
    connector = next(params_gen)
    assert isinstance(connector.client, client.InfluxDBClient)
    next(params_gen)


def test_write_to_database():
    """
    GIVEN an instance of the DatabaseConnector
    WHEN you try to send data to influxdb through it
    THEN it should return True
    """
    params_gen = client_params()
    connector = next(params_gen)
    data = {field: random() * 100 for field in connector.fields}
    assert connector.write(data)
    next(params_gen)
