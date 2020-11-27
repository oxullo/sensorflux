#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import random

from influxdb import client

from sensorflux.database_connector import DatabaseConnector


def client_params():
    measurement = f'measurement_{str(random())[2:]}'
    device = f'device_{str(random())[2:]}'
    client_connection = (yield measurement, device)
    yield client_connection.client.drop_measurement(measurement)


def test_database_connector():
    """
    GIVEN the DatabaseConnector class
    WHEN you instantiate it
    THEN it returns a valid InfluxDBClient object
    """
    params_gen = client_params()
    measurement, device = next(params_gen)
    connector = DatabaseConnector(
        measurement=measurement,
        device=device,
        fields=(666, 777, 888))
    assert isinstance(connector.client, client.InfluxDBClient)
    params_gen.send(connector)


def test_write_to_database():
    """
    GIVEN an instance of the DatabaseConnector
    WHEN you try to send data to influxdb through it
    THEN it should return True
    """
    params_gen = client_params()
    measurement, device = next(params_gen)
    fields = (666, 777, 888)
    connector = DatabaseConnector(
        measurement=measurement,
        device=device,
        fields=fields)
    data = {field: random() * 100 for field in fields}
    assert connector.write(data) is True
    params_gen.send(connector)
