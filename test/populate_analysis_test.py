#!/usr/bin/python
# -*- coding: utf8 -*-

# prueba para popular la DB test_analysis

from datetime import date

from test_helper import *
from helpers.logging_helper import init_logger
from populate_analysis import run


init_logger("pop_analysis", test=True)

day = date.today().replace(year=2013, month=01, day=11)

run(day, test=True)
