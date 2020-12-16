#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from datetime import datetime

from requests import RequestException


class PollingError(Exception):
    pass


class PollingInterface:
    def __init__(self, arduino_client, influxdb_client, period):
        self._arduino_client = arduino_client
        self._influxdb_client = influxdb_client
        self._period = period
        self._running = False
        self._polling_errors = 0
        self._error_threshold = 5

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
            try:
                await self.poll()
            except PollingError as e:
                print(e)
                self._running = False
                return 1
            except ValueError as e:
                error_message, time = e.args
                print(error_message)
                self._polling_errors += 1
                await asyncio.sleep(max(
                    0, self.period - (datetime.now() - time).total_seconds()))

    def stop(self):
        self._running = False

    async def poll(self):
        if self._polling_errors >= self._error_threshold:
            raise PollingError(f'got {self._polling_errors} '
                               f'successive errors while polling')
        start_time = datetime.now()
        print(f'polling now at: {start_time.isoformat()}')
        try:
            data = await self._arduino_client.poll()
            if data is None:
                raise ValueError('no data returned from the arduino client',
                                 start_time)
            self._influxdb_client.write(data)
        except AssertionError:
            print('starting the arduino client')
            await self._arduino_client.start()
            self._polling_errors += 1
            return
        except RequestException as e:
            print(e)
            self._polling_errors += 1
        else:
            self._polling_errors = 0
        await asyncio.sleep(max(
            0,
            self.period - (datetime.now() - start_time).total_seconds()))
