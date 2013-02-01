#!/usr/bin/python
# -*- coding: utf8 -*-

# prueba para ejecutar wikisquilter sobre un log

from datetime import date

from test_helper import *
from helpers.logging_helper import init_logger
from run_wikisquilter import run


init_logger("run_wsq", test=True)

day = date.today().replace(year=2013, month=01, day=10)

run(day, test=True)
