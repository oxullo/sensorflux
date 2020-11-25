#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from _datetime import datetime
import threading

input_collection = [[], [], [], []]


# Read Arduino Data Dummy data
def input_genertator():
    temp = random.randint(1, 255)
    atmo = random.randint(1, 255)
    humi = random.randint(1, 255)
    time = datetime.now()
    date_time_cleaned = [time.year, time.month, time.day]
    return [date_time_cleaned, temp, atmo, humi]


def call_generator():
    threading.Timer(5.0, call_generator).start()
    global input_collection
    values = input_genertator()
    count = 0
    for i in input_collection:
        i.append(values[count])
        count = count + 1
    return


call_generator()
