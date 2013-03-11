#!/usr/bin/python
# -*- coding: utf8 -*-

# prueba para popular la DB test_analysis

from datetime import date

import test_helper
from helpers.logging_helper import init_logger
import populate_analysis

init_logger("pop_analysis")

from helpers.config_helper import getConfig

# vamos a popular analysis con 3 fechas

day = date.today().replace(year=2013, month=01, day=01)
populate_analysis.run(day)

day = date.today().replace(year=2013, month=01, day=02)
populate_analysis.run(day)

day = date.today().replace(year=2013, month=01, day=05)
populate_analysis.run(day)
