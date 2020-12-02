#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from sensorflux.polling_interface import PollingInterface


@pytest.fixture()
def poller():
    return PollingInterface('fake_arduino', 'fake_db', 0)


def test_int(poller):
    poller.period = 123
    assert poller.period == 123


def test_float(poller):
    with pytest.raises(ValueError):
        poller.period = 12.3


def test_negative(poller):
    with pytest.raises(ValueError):
        poller.period = -321


def test_string(poller):
    with pytest.raises(ValueError):
        poller.period = '123'


def test_bool(poller):
    with pytest.raises(ValueError):
        poller.period = True
