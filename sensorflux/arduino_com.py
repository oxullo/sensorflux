#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arduino_value_collect


def get_values_day(date):
    value_collection = arduino_value_collect.input_collection
    values_of_day = []
    print(f'This is value collection {value_collection}')
#    values_of_day = [i for i in value_collection if i[0] == date]
    for i in value_collection:
        print(f'This is i {i}')
        if i[0] == date:
            values_of_day.append(i)

    print(f'Values of the Day {values_of_day}')
    return


def get_values_between():
    return


def get_highest_value():
    return


def get_last_value():
    value_collection = arduino_value_collect.input_collection
    last_value = []
    for i in value_collection:
        last_value.append(i[-1])
#    print(f' This are the latest Values {last_value}')
    return last_value


def get_average(num_samples):
    value_collection = arduino_value_collect.input_collection
    latest_values_average = []
    it = iter(value_collection)
    next(it, None)
    for i in it:
        average = sum(i[-num_samples:]) / num_samples
        latest_values_average.append(average)
#    print(f' Values average is {latest_values_average}')
    return latest_values_average


def get_latest_values(num_sampless):
    value_collection = arduino_value_collect.input_collection
    latest_values = []
    for i in value_collection:
        latest_values.append(i[-num_sampless:])
#    print(f'Latest values List{latest_values}')
    return latest_values
