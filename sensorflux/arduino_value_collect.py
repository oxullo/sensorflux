#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import asyncio
import random
from _datetime import datetime
import threading

input_collection = [[], [], [], []]


# Read Arduino Data Dummy data
def input_genertator():
    temp = random.randint(1, 255)
    atmo = random.randint(1, 255)
    humi = random.randint(1, 255)
    dateTime = datetime.now()
    date_time_cleaned = [dateTime.year, dateTime.month, dateTime.day, dateTime.hour, dateTime.minute, dateTime.second]
    return [date_time_cleaned, temp, atmo, humi]


def call_generator():
    threading.Timer(5.0, call_generator).start()
    global input_collection
    input = input_genertator()
    count = 0
    for i in input_collection:
        i.append(input[count])
        count = count + 1


#    print(input_collection)

call_generator()
# TIME_PAUSE_VALUES = 5
#
# ticker = threading.Event()
# while not ticker.wait(TIME_PAUSE_VALUES):
#     call_generator()

# async def call_generator():
#     global input_collection
#     while True:
#         input = input_genertator()
#        # print(input)
#         #input_collection[0].append(input[0])
#         #print(input_collection)
#         count=0
#         for i in input_collection:
#             i.append(input[count])
#             count=count+1
#         print(f'This is input_collection{input_collection}')
#
#         await asyncio.sleep(10)
#
#
# input_loop = asyncio.get_event_loop()
# input_tasks = input_loop.create_task(call_generator())
# input_loop.run_forever()
# input_loop.close()
