#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from errors import *


class Sensor:
    # sensor object factory
    def __init__(self, binding: str, name: str):
        # sensor object model
        # param binding: string containing the key name which the sensor will right to
        # param name: string containing the name of the sensor
        self.binding = binding
        self.name = name
        self.response = {}

    