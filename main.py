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


from datetime import date, timedelta
import logging

import transfer_log
import run_wikisquilter
import populate_analysis
import clear_squidlogs


# ejecuta toda la tarea para el dia dado
def run(date):
	logging.info("Procesando día: " + date.strftime('%Y%m%d'))
	# transferimos
	#transfer_log.run(date)

	# ejecutamos wsq
	run_wikisquilter.run(date)

	# populamos analysis con resultados
	populate_analysis.run()

	# vaciamos BD squidlogs
	clear_squidlogs.run()

date = date.today()

# configuramos un logger para informarnos de la ejecucion en el archivo run[fecha].log
logging.basicConfig(filename="run_logs/run-" + date.strftime('%Y%m%d') + ".log",
	format='%(asctime)s - %(message)s',
	level=logging.INFO)

logging.info("********* COMENZANDO EJECUCIÓN ********* ")

today = date.day

# si hoy es el día 1 procesaremos los logs entre los días 20 y último día del mes anterior
if today == 1:
	date -= timedelta(1)
	top_day = date.day
	for i in range(20, top_day + 1):
		date = date.replace(day=i)  # http://docs.python.org/2/library/datetime.html
		run(date)

# si hoy es 10 entonces se procesarán los logs entre el 1 y 9
elif today == 19:
	date -= timedelta(9)
	for i in range(0, 9):
		run(date)
		date += timedelta(1)

# si hoy es 20 se procesarán entre el 10 y el 19
elif today == 20:
	date -= timedelta(10)
	for i in range(0, 10):
		run(date)
		date += timedelta(1)
