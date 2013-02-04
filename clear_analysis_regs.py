#!/usr/bin/python
# -*- coding: utf8 -*-

# borra registros en analysis

from argparse import ArgumentParser
from datetime import timedelta
import sys

from helpers.mysql_helper import mysql_query
from helpers.config_helper import Config
from helpers.date_helper import str_to_date


def del_query(table_name):
	"""
	Ejecuta la query sobre una BD para eliminar los registros
	de una tabla y fecha dada
	"""
	global i_date
	where_clause = " WHERE day = '" + str(i_date) + "'"
	# http://dev.mysql.com/doc/refman/5.0/en/delete.html
	query = "DELETE FROM " + table_name + i_date.strftime('%Y') + where_clause

	global database
	mysql_query(database, query, "delete_rows")


def delete_day():
	"""
	Mira en la lista de días procesados. Si existe el día elimina los registros
	y borra el día en dicha lista de procesados.
	"""
	global i_date
	global test_mode
	if Config().is_processed_date(i_date, test_mode):
		del_query("actions")
		del_query("saved")
		del_query("visited")
		Config().remove_from_processed_list(i_date, test_mode)
		print "Deleted rows for " + str(i_date)
	else:
		print str(i_date) + " not in processed list"


###############
#
#  MAIN
#
###############

parser = ArgumentParser()
parser.add_argument('-t', '--test',
	action="store_true",
	dest="test",
	default=False,
	help='Clear test_analysis database regs')
parser.add_argument(
	nargs="+",
	metavar=('INITIAL_DATE', 'FINAL_DATE'),
	dest="date",
	default=False,
	help='Delete regs from database between 2 dates')
args = parser.parse_args()

print args

test_mode = True if args.test else False
# date_mode = True if args.date else False

if not test_mode:
	ans = raw_input("WARNING: Not in test mode. Type 'analysis' to continue..\n")
	if ans != 'analysis':
		print "Exiting without changes.."
		sys.exit(0)


database = "test_analysis" if test_mode else "analysis"

i_date = str_to_date(args.date[0])

if len(args.date) == 1:
	delete_day()
else:
	f_date = str_to_date(args.date[1])
	while i_date <= f_date:
		delete_day()
		i_date += timedelta(1)
