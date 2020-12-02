#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from datetime import datetime


class PollingInterface:
    def __init__(self, arduino_client, influxdb_client, period):
        self._arduino_client = arduino_client
        self._influxdb_client = influxdb_client
        self._period = period
        self._running = False

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value):
        if isinstance(value, int) and value >= 0:
            self._period = value
        else:
            raise ValueError('Value should be a positive integer.')

    @property
    def running(self):
        return self._running

    def run(self):
        self._running = True
        while self.running is True:
            asyncio.run(self.poll())

    def stop(self):
        self._running = False

    async def poll(self):
        start_time = datetime.now()
        print(f'polling now at: {start_time.isoformat()}')
        data = self._arduino_client.read()
        self._influxdb_client.write(data)
        await asyncio.sleep(max(
            0,
            self.period - (datetime.now() - start_time).total_seconds()))
