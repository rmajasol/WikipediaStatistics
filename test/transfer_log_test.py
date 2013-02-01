#!/usr/bin/python
# -*- coding: utf8 -*-

# prueba para la transferencia de logs desde equipo remoto a local

from datetime import date

from test_helper import *
from helpers.logging_helper import init_logger
from transfer_log import run


init_logger("transfer_log", test=True)

day = date.today().replace(year=2013, month=01, day=10)

run(day, test=True)
