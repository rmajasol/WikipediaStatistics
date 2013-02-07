#!/usr/bin/python
# -*- coding: utf8 -*-

# borra registros en analysis

from argparse import ArgumentParser
from datetime import timedelta
import sys

from helpers.mysql_helper import exec_mysql_query
from helpers.config_helper import Config
from helpers.date_helper import str_to_date


def del_query(table_name):
	"""
	Ejecuta la query sobre una BD para eliminar los registros
	de una tabla y fecha dada
	"""
	# http://dev.mysql.com/doc/refman/5.0/en/delete.html
	query = "DELETE FROM " + table_name + i_date.strftime('%Y') + \
			" WHERE day = '" + str(i_date) + "'"

	exec_mysql_query(database, query)


def delete_date():
	"""
	Mira en la lista de días procesados. Si existe el día elimina los registros
	y borra el día en dicha lista de procesados.
	"""
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
	help='Delete regs from database between 2 dates or just one')
args = parser.parse_args()


test_mode = True if args.test else False

# crea diálogo de confirmación en caso de no ejecutar en modo test
if not test_mode:
	ans = raw_input("WARNING: Not in test mode. Type 'analysis' to continue..\n")
	if ans != 'analysis':
		print "Exiting without changes.."
		sys.exit(0)


database = "test_analysis" if test_mode else "analysis"

if len(args.date) == 1:
	delete_date()
else:
	i_date = str_to_date(args.date[0])
	f_date = str_to_date(args.date[1])
	while i_date <= f_date:
		delete_date()
		i_date += timedelta(1)
