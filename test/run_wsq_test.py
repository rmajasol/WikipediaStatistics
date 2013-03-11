#!/usr/bin/python
# -*- coding: utf8 -*-

# prueba para ejecutar wikisquilter sobre un log

from datetime import date

import test_helper
from helpers.logging_helper import init_logger
import run_wikisquilter

init_logger('run_wsq')

# vamos a procesar WikiSquilter sobre 3 logs..

day = date.today().replace(year=2013, month=01, day=01)
run_wikisquilter.run(day)

day = date.today().replace(year=2013, month=01, day=02)
run_wikisquilter.run(day)

day = date.today().replace(year=2013, month=01, day=05)
run_wikisquilter.run(day)
