#!/usr/bin/python
# -*- coding: utf8 -*-

# para manejarnos con las fechas

from datetime import datetime, timedelta


def get_now_to_zero():
	"""
	Devuelve la fecha actual seteando a 0 los argumentos de la
	función 'replace'
	http://stackoverflow.com/questions/5476065/truncate-python-datetime
	"""
	now = datetime.now()
	now = now.replace(hour=0, minute=0, second=0, microsecond=0)
	return now.date()


def str_to_date(str):
	"""
	Obtenemos un objeto de tipo 'date' a partir de un string
	con el formato de fecha YYYYMMDD
	"""
	date = get_now_to_zero()

	year = int(str[:4])
	month = int(str[4:6])
	day = int(str[6:])

	return date.replace(year=year, month=month, day=day)


# http://stackoverflow.com/questions/6289646/python-function-as-a-function-argument
def do_for_dates(function, args):
	"""
	Ejecuta una función dada 'function' sobre una fecha concreta si sólo se pasa una
	como argumento en 'args' y sobre un intervalo de fechas si se pasa como argumento
	una fecha inicial y otra final
	"""
	d = str_to_date(args.date[0])
	if len(args.date) == 1:
		function(d)
	else:
		d2 = str_to_date(args.date[1])
		while d <= d2:
			function(d)
			d += timedelta(1)
