#!/usr/bin/python
# -*- coding: utf8 -*-

# prueba para popular la BD squidlogs a partir de logs de 10 días 
# anteriores a la fecha actual 

import test_helper

from run_wikisquilter import run

from datetime import date, timedelta

date = date.today()
date -= timedelta(10)

for i in range(0, 10):
	run(date, test=True)
	date += timedelta(1)
