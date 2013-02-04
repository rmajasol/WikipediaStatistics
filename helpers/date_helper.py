#!/usr/bin/python
# -*- coding: utf8 -*-

# para manejarnos con las fechas

from datetime import datetime


def get_now_to_zero():
	"""
	Devuelve la fecha actual con los demás valores seteados a 0
	http://stackoverflow.com/questions/5476065/truncate-python-datetime
	"""
	now = datetime.now()
	now = now.replace(hour=0, minute=0, second=0, microsecond=0)
	return now.date()


def str_to_date(str):
	"""
	Obtenemos un objeto de tipo 'date' a partir de un string YYYYMMDD
	"""
	date = get_now_to_zero()

	year = int(str[:4])
	month = int(str[4:6])
	day = int(str[6:])

	return date.replace(year=year, month=month, day=day)
