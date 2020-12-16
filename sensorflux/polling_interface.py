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
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError('Period should be an integer.')
        if value < 0:
            raise ValueError('Period should be positive.')
        self._period = value

    @property
    def running(self):
        return self._running

    async def run(self):
        self._running = True
        while self.running is True:
            await self.poll()

    def stop(self):
        self._running = False

    async def poll(self):
        start_time = datetime.now()
        print(f'polling now at: {start_time.isoformat()}')
        data = await self._arduino_client.poll()
        self._influxdb_client.write(data)
        await asyncio.sleep(max(
            0,
            self.period - (datetime.now() - start_time).total_seconds()))
