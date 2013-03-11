#!/usr/bin/python
# -*- coding: utf8 -*-

# borra registros en analysis

from datetime import timedelta
import sys

from helpers.config_helper import setConfig, getConfig
from helpers.parser_helper import init_argparser
from helpers.date_helper import str_to_date


deleted_year = None


def del_row_query_for_analysis(table_name, date):
	"""
	Ejecuta la query sobre analysis para eliminar los registros
	de una tabla y fecha dada
	"""
	# http://dev.mysql.com/doc/refman/5.0/en/delete.html
	query = "DELETE FROM " + table_name + date.strftime('%Y') + \
			" WHERE day = '" + str(date) + "'"

	exec_mysql(getConfig().db_name_analysis, query=query)


def del_row_query_for_squidlogs(date):
	"""
	Ejecuta la query sobre squidlogs para eliminar los registros para la fecha dada
	"""
	query = "DELETE FROM Filtered " + \
			"WHERE date(f_date_time) = '" + date.strftime('%Y-%m-%d') + "'"

	exec_mysql(getConfig().db_name_squidlogs, query=query)


def del_table_query_for_analysis(table_name, year):
	"""
	Ejecuta la query sobre analysis para eliminar las tablas para
	el año dado
	"""
	# http://dev.mysql.com/doc/refman/5.0/en/delete.html
	query = "DROP TABLE IF EXISTS " + table_name + year

	exec_mysql(getConfig().db_name_analysis, query=query)


def delete_date(date):
	"""
	Mira en la lista de días procesados. Si existe el día elimina los registros
	y borra el día en dicha lista de procesados.
	"""
	year = date.strftime('%Y')

	if db_name == 'analysis' or db_name == 'test_analysis':
		if getConfig().is_processed_for(date, 'analysis'):
			del_row_query_for_analysis("actions", date)
			del_row_query_for_analysis("saved", date)
			del_row_query_for_analysis("visited", date)
			getConfig().remove_from_processed_list(date, 'analysis')
			print "\tDeleted rows for " + str(date)

			# elimina las tablas si no existe ningún registro para el año
			if getConfig().year_not_exists_in_list(year, 'analysis'):
				del_table_query_for_analysis("actions", year)
				del_table_query_for_analysis("saved", year)
				del_table_query_for_analysis("visited", year)

				print "Deleted tables for " + year

		# si la fecha dada no está procesada pero su año aparece en la lista
		# de fechas procesadas (log.analysis.processed)..
		elif not getConfig().year_not_exists_in_list(year, 'analysis'):
			print "\t\t" + str(date) + " not in processed list for " + db_name
	else:
		if getConfig().is_processed_for(date, 'squidlogs'):
			del_row_query_for_squidlogs(date)
			getConfig().remove_from_processed_list(date, 'squidlogs')
			print "Deleted rows for " + str(date)
		elif not getConfig().year_not_exists_in_list(year, 'squidlogs'):
			print "\t" + str(date) + " not in processed list for " + db_name


###############
#
#  MAIN
#
###############

args = init_argparser(
	test='Removes only test regs in chosen database',
	database='Especify database name',
	date='Delete regs from database between 2 dates or just one')

test_mode = True if args.test else False
setConfig(test_mode=test_mode)

# nombre de la base de datos en la cual eliminar los registros
db_name = getConfig().db_name_squidlogs if args.database[0] == 'squidlogs' \
			else getConfig().db_name_analysis


from helpers.mysql_helper import exec_mysql

# crea diálogo de confirmación en caso de no ejecutar en modo test
if not test_mode:
	ans = raw_input("WARNING: Not in test mode. Type " + db_name + " to continue..\n")
	if ans != db_name:
		print "Exiting without changes.."
		sys.exit(0)

print "Deleting data in " + db_name + ".."

if len(args.date) == 1:
	delete_date(args.date[0])
else:
	i_date = str_to_date(args.date[0])
	f_date = str_to_date(args.date[1])
	while i_date <= f_date:
		delete_date(i_date)
		i_date += timedelta(1)
