#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arduino_com
import threading


if __name__ == '__main__':

    WAIT_TIME_SECONDS = 2

    ticker = threading.Event()
    while not ticker.wait(WAIT_TIME_SECONDS):
        arduino_com.get_last_value()
        arduino_com.get_average(2)
        arduino_com.get_latest_values(2)
        arduino_com.get_values_day([2020, 11, 25])
