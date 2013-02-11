#!/usr/bin/python
# -*- coding: utf8 -*-

# borra registros en analysis

import sys

import add_to_pythonpath
from helpers.mysql_helper import exec_mysql_query
from helpers.config_helper import Config
from helpers.date_helper import *
from helpers.parser_helper import init_argparser


def del_row_query(table_name, date):
	"""
	Ejecuta la query sobre una BD para eliminar los registros
	de una tabla y fecha dada
	"""
	# http://dev.mysql.com/doc/refman/5.0/en/delete.html
	query = "DELETE FROM " + table_name + date.strftime('%Y') + \
			" WHERE day = '" + str(date) + "'"

	exec_mysql_query(database, query)


def del_table_query(table_name, year):
	"""
	Ejecuta la query sobre una BD para eliminar las tablas para
	el año dado
	"""
	# http://dev.mysql.com/doc/refman/5.0/en/delete.html
	query = "DROP TABLE IF EXISTS " + table_name + year

	exec_mysql_query(database, query)


def delete_date(date):
	"""
	Mira en la lista de días procesados. Si existe el día elimina los registros
	y borra el día en dicha lista de procesados.
	"""
	if Config().is_processed_date(date, test_mode):
		del_row_query("actions", date)
		del_row_query("saved", date)
		del_row_query("visited", date)
		Config().remove_from_processed_list(date, test_mode)
		print "Deleted rows for " + str(date)

		# elimina las tablas si no existe ningún registro para el año
		year = date.strftime('%Y')
		if Config().year_not_exists(year, test_mode):
			del_table_query("actions", year)
			del_table_query("saved", year)
			del_table_query("visited", year)
			print "Deleted tables for " + year

	else:
		print str(date) + " not in processed list"


###############
#
#  MAIN
#
###############

args = init_argparser(
	test="Clear test_analysis database regs",
	date='Delete regs from database between 2 dates or just one')


test_mode = True if args.test else False

# crea diálogo de confirmación en caso de no ejecutar en modo test
if not test_mode:
	ans = raw_input("WARNING: Not in test mode. Type 'analysis' to continue..\n")
	if ans != 'analysis':
		print "Exiting without changes.."
		sys.exit(0)


database = "test_analysis" if test_mode else "analysis"

do_for_dates(delete_date, args)
