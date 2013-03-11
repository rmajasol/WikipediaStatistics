#!/usr/bin/python
# -*- coding: utf8 -*-

# prueba para la transferencia de logs desde equipo remoto a local

from datetime import date

import test_helper
from helpers.logging_helper import init_logger
import transfer_log

init_logger("transfer_log")

# vamos a descargar logs para 3 fechas..

day = date.today().replace(year=2013, month=01, day=01)
transfer_log.run(day)

day = date.today().replace(year=2013, month=01, day=02)
transfer_log.run(day)

day = date.today().replace(year=2013, month=01, day=05)
transfer_log.run(day)
