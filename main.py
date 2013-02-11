#!/usr/bin/python
# -*- coding: utf8 -*-


# Script principal que realiza todo el proceso de popular la BD
# analysis a partir de los logs
#
#
# Tenemos dos modos de ejecución:
#
# -> Automático:
# 		Creamos cron:
#			0 12 1,10,20 * * python /ruta/absoluta/hacia/main.py
#
# 		Así, a las 12:00 horas de cada día 1, 10 y 20 de cada mes
#		se realizará la siguiente serie de tareas para procesar
#		cada log:
# 			1. Tansferir log: transfer_log.py
# 			2. Ejecutar wikisquilter sobre él: run_wikisquilter.py
# 			3. Popular BD analysis: populate_analysis.py
# 			4. Vaciar BD squidlogs: clear_squidlogs.py
#
#		Según el día de ejecución se procesarán logs correspondientes
#		a los días:
#			Día 1: en mes anterior entre 20 - último día de mes
#			Día 10: 1 - 9
#			Día 20: 10 - 19
#
# -> Manual:
# 		Ejecutamos "python main.py -m FECHA_INICIO FECHA_FIN"
# 		para procesar logs entre dos fechas dadas.
# 		Por ejemplo entre los días 1 y 20 de febrero de 2013:
# 			python main.py -m 20130101 20130220
#
# Además, incluyendo la opción -t podemos indicar que se ejecute sólo
# sobre logs de prueba, es decir, los generados usando el script
# log_generator3.py
# Por ejemplo, para procesar logs de prueba entre dos fechas:
#		python main.py -t -m 20130101 20130220


from datetime import timedelta
from argparse import ArgumentParser

from helpers.config_helper import *
from helpers.logging_helper import *
from helpers.date_helper import *

import transfer_log
import run_wikisquilter
import populate_analysis
import clear_squidlogs


def run_for_day(date):
	"""
	Ejecuta todas la tareas para procesar el día dado
	"""
	processed = Config().is_processed_date(date, test_mode)
	day = Config().get_log_date(date)

	if not processed:
		log_msg("---- Procesando día " + day + " ----")

		# transferimos
		# transfer_log.run(date, test_mode)

		# ejecutamos wsq
		run_wikisquilter.run(date, test_mode)

		# populamos analysis con resultados
		populate_analysis.run(date, test_mode)

		# vaciamos BD squidlogs
		clear_squidlogs.run()
	else:
		log_msg("#### No es necesario procesar el día " + day + " ####")


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


def run_manual():
	"""
	Si recibe 2 argumentos: Procesa días entre la fecha inicial y final
	Si recibe un argumento: Procesa sólo ese día
	"""
	d = str_to_date(args.manual[0])

	if len(args.manual) == 1:
		run_for_day(d)
	else:
		d2 = str_to_date(args.manual[1])
		# mientras que la fecha d sea menor a la final (d2)..
		while d <= d2:
			run_for_day(d)
			d += timedelta(1)


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
	nargs='+',
	# http://argparse.googlecode.com/svn/trunk/doc/add_argument.html#metavar
	metavar=('INITIAL_DATE', 'FINAL_DATE'),
	dest="manual",
	default=False,
	help='Manually process a certain volume of logs between 2 dates.\n' + \
		'e.g. main.py -m 20130101 20130327 -> ' + \
		'This will process all logfiles between 1st Jan 2013 and 27th Mar 2013')
args = parser.parse_args()


test_mode = True if args.test else False
manual_mode = True if args.manual else False

# configuramos un logger para informarnos de la ejecucion en el archivo main-[fecha].log
init_logger("main", test=test_mode)

# guardamos la fecha actual en 'date' con los demás valores (hora, minuto..) seteados a 0
date = get_now_to_zero()

# según estemos ejecutando en modo manual o no..
if manual_mode:
	run_manual()
else:
	run_auto()
