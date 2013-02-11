#!/usr/bin/python
# -*- coding: utf8 -*-

# prueba para popular la DB test_analysis

from datetime import date

from test_helper import *
from helpers.logging_helper import init_logger, log_msg
from helpers.config_helper import Config
from populate_analysis import run


init_logger("pop_analysis", test=True)

day = date.today().replace(year=2012, month=02, day=20)


processed = Config().is_processed_date(day, test=True)

if not processed:
	run(day, test=True)
else:
	print "#### No es necesario procesar el día " + str(day) + " ####"
