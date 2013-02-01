#!/usr/bin/python
# -*- coding: utf8 -*-

# prueba para limpiar por completo la DB squidlogs

from test_helper import *
from helpers.logging_helper import init_logger
from clear_squidlogs import run


init_logger("clear_squidlogs", test=True)

run()
