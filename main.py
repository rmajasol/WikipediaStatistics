#!/usr/bin/python
# -*- coding: utf8 -*-


# script principal que realiza todo el proceso de popular la BD
# analysis a partir de los logs
#
#
# Cada día 1, 10 y 20 de cada mes se realizan las siguiente serie de tareas:
#
# 1. Tansferir logs de días anteriores -> transfer_log.py
# 2. Ejecutar wikisquilter sobre ellos -> run_wikisquilter.py
# 3. Popular BD de analysis -> populate_analysis.py
# 4. Vaciar la BD squidlogs -> clear_squidlogs.py

# añadimos la carpeta raíz del proyecto al PYTHONPATH
# import os
# import sys
# sys.path.append(os.getcwd())

from datetime import datetime, timedelta
from argparse import ArgumentParser

from helpers.config_helper import *
from helpers.logging_helper import *

import transfer_log
import run_wikisquilter
import populate_analysis
import clear_squidlogs


def run_for_day(date):
	"""
	Ejecuta todas la tareas para procesar el día dado
	"""
	global test_mode
	processed = Config().is_processed_date(date, test_mode)
	day = Config().get_log_date(date)

	if not processed:
		log_msg("---- Procesando día: " + day + " ----")

		# transferimos
		transfer_log.run(date, test_mode)

		# ejecutamos wsq
		run_wikisquilter.run(date, test_mode)

		# populamos analysis con resultados
		populate_analysis.run(date, test_mode)

		# vaciamos BD squidlogs
		clear_squidlogs.run()
	else:
		log_msg("#### El día " + day + " ya fue procesado ####")


def run_auto():
	"""
	Ejecución automática según el día en que haya sido invocado el script
	"""
	global date
	today = date.day

	# si hoy es el día 1 procesaremos los logs entre los días 20 y último día del mes anterior
	if today == 1:
		date -= timedelta(1)
		top_day = date.day
		for i in range(20, top_day + 1):
			date = date.replace(day=i)  # http://docs.python.org/2/library/datetime.html
			run_for_day(date)

	# si hoy es 10 entonces se procesarán los logs entre los días 1 y 9
	elif today == 10:
		date -= timedelta(9)
		for i in range(0, 9):
			run_for_day(date)
			date += timedelta(1)

	# si hoy es 20 se procesarán entre el 10 y el 19
	elif today == 20:
		date -= timedelta(10)
		for i in range(0, 10):
			run_for_day(date)
			date += timedelta(1)


def run_manual(initial_date, final_date):
	"""
	Procesa días entre la fecha inicial y final
	"""
	i_year = int(initial_date[:4])
	i_month = int(initial_date[4:6])
	i_day = int(initial_date[6:])

	f_year = int(final_date[:4])
	f_month = int(final_date[4:6])
	f_day = int(final_date[6:])

	global date
	i_date = date.replace(year=i_year, month=i_month, day=i_day)
	f_date = date.replace(year=f_year, month=f_month, day=f_day)

	# mientras que la fecha d sea menor a la final (d2)..
	while i_date <= f_date:
		run_for_day(i_date)
		i_date += timedelta(1)


###########################
#
# EJECUCIÓN PRINCIPAL
#
###########################

# obtenemos los argumentos con el uso del parseador..
parser = ArgumentParser()
parser.add_argument('-t', '--test',
	action="store_true",
	dest="test",
	default=False,
	help='Runs in test mode')
parser.add_argument('-m', '--manual',
	nargs=2,
	# http://argparse.googlecode.com/svn/trunk/doc/add_argument.html#metavar
	metavar=('INITIAL_DATE', 'FINAL_DATE'),
	dest="manual",
	default=False,
	help='Manually process a certain volume of logs between 2 dates.\n' + \
		'e.g. option_parser.py -m 20130101 20130327 -> ' + \
		'This will process all logfiles between 1st Jan 2013 and 27th Mar 2013')
args = parser.parse_args()


test_mode = True if args.test else False
manual_mode = True if args.manual else False


# guardamos la fecha actual en 'date' con los demás valores seteados a 0
# http://stackoverflow.com/questions/5476065/truncate-python-datetime
now = datetime.now()
now = now.replace(hour=0, minute=0, second=0, microsecond=0)
date = now.date()


# configuramos un logger para informarnos de la ejecucion en el archivo run[fecha].log
init_logger("main", test=test_mode)


# según estemos ejecutando en modo manual o no..
if manual_mode:
	run_manual(args.manual[0], args.manual[1])
else:
	run_auto()
