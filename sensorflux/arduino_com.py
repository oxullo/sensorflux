#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arduino_value_collect


class ArduinoCom:


    def get_last_value(self):
        value_collection = arduino_value_collect.input_collection
        latest_values = []
        for i in value_collection:
            latest_values.append(i[-1])

        print(f' This are the latest Values {latest_values}')
        return latest_values

    def get_latest_values(self, num_samples):
        value_collection = arduino_value_collect.input_collection
        latest_values_average = []
        it = iter(value_collection)
        next(it, None)
        for i in it:
            average = sum(i[-num_samples:]) / num_samples
            latest_values_average.append(average)

        latest_values = []
        for i in value_collection:
            for j in i[-num_samples:]:
                latest_values.append(j)

        print(f' Values average is {latest_values_average}')
        print(f'Latest values List{latest_values}')
        return latest_values_average , latest_values

    def get_values_day(self):
        return

    def get_values_between(self):
        return