#!/usr/bin/python
# -*- coding: utf8 -*-

# prueba para limpiar por completo la DB squidlogs

import test_helper
from helpers.logging_helper import init_logger
import clear_squidlogs

init_logger('clear_squidlogs')

clear_squidlogs.run()
