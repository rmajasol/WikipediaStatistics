#!/usr/bin/python
# -*- coding: utf8 -*-

import re
from helpers.utils import is_empty
from helpers.config_helper import getConfig
from helpers.logging_helper import log_msg2, log_msg3, log_msg4, log_msg_ok2, log_msg_ok3, log_msg_ok4
from helpers.mysql_helper import exec_mysql

DB_NAME = getConfig().db_name_analysis
TEST_MODE = getConfig().test_mode
TXT_FILE = getConfig().get_dumped_txt_filename()

# indica el año del txt donde se vuelca el resultado de la query a squidlogs
txt_year = ""

# indica si se crearon ya las tablas nuevas
new_tables_created = False


def get_table_name_year(table_name):
	"""
	Devuelve el nombre de la tabla junto con el año obtenido del .txt
	generado por la query a squidlogs
	"""
	return table_name + txt_year


def wsq_to_txt(table_name, date):
	"""
	Vuelca en tmp/dumped.txt el resultado de la query a la BD squidlogs
	"""
	if(table_name == 'visited'):
		query = "select date(f_date_time), substr(dayname(f_date_time),1,2), " + \
			"f_lang_id, f_ns_id, count(*) " + \
			"from Filtered where f_action_id is null " + \
			"and date(f_date_time) = '" + date.strftime('%Y-%m-%d') + "' " + \
			"group by date(f_date_time), f_lang_id, f_ns_id;"
	elif(table_name == 'saved'):
		query = "select date(f_date_time), substr(dayname(f_date_time),1,2), " + \
			"f_lang_id, f_ns_id, count(*) " + \
			"from Filtered where f_action_id = 2 " + \
			"and date(f_date_time) = '" + date.strftime('%Y-%m-%d') + "' " + \
			"group by date(f_date_time), f_lang_id, f_ns_id;"
	elif(table_name == 'actions'):
		query = "select date(f_date_time), substr(dayname(f_date_time),1,2), " + \
			"f_action_id, f_lang_id, f_ns_id, count(*) " + \
			"from Filtered where f_action_id in (0, 1, 3, 4) " + \
			"and date(f_date_time) = '" + date.strftime('%Y-%m-%d') + "' " + \
			"group by date(f_date_time), f_action_id, f_lang_id, f_ns_id;"

	log_msg4("Creando dump para " + table_name)

	exec_mysql(getConfig().db_name_squidlogs, query=query, dumped=True)

	log_msg_ok4()


def is_new_year(table_name):
	"""
	Mira en el txt el año y si no hay fecha alguna procesada para ese año
	entonces devolverá True
	"""
	# si el fichero no tiene nada devolvemos False para no crear luego una tabla vacia
	if is_empty(TXT_FILE):
		log_msg4("WARNING: No se puede obtener el año del dump.txt vacío!!")
		return False
	else:
		# si el fichero no está vacío lo leemos para comprobar el año
		f = open(TXT_FILE)
		f.readline()
		# la primera linea no interesa. Leemos la segunda y sacamos el
		# año eligiendo el primer grupo (\d{4}) de la expresión regular
		# que coincide con dicha línea
		l = f.readline()
		m = re.match(".*(\d{4})\-\d{2}.*", l)
		# seteamos txt_year con el año del dumped.txt
		global txt_year
		txt_year = m.group(1)

		# miramos si en la lista de procesados (logs.processed)
		# aparece alguno ya procesado para el año del txt,
		# lo cual quiere decir que ya existe la tabla
		return getConfig().year_not_exists_in_list(txt_year, 'analysis')


def create_table(table_name):
	"""
	Crea nueva tabla
	"""
	table_name_year = get_table_name_year(table_name)
	query = "DROP TABLE IF EXISTS " + table_name_year + ";" + \
			"CREATE TABLE " + table_name_year + " (" + \
				"day DATE," + \
				"dayWeek VARCHAR(2),"

	# si la tabla es actions hay que añadir este campo
	if(table_name == 'actions'):
		query += "action TINYINT,"

	query += "lang VARCHAR(2)," + \
				"ns TINYINT," + \
				"count int" + \
			");" + \
			"alter table " + table_name_year + " add index (day, dayWeek, lang, ns);"

	exec_mysql(DB_NAME, query=query)


def create_tables():
	"""
	Crea nuevas tablas VISITEDYYYY, SAVEDYYYY, ACTIONSYYYY
	"""
	log_msg4("No hay tablas para el año " + txt_year + ". Creando")

	create_table('visited')
	create_table('saved')
	create_table('actions')

	global new_tables_created
	new_tables_created = True

	log_msg_ok4()


def txt_to_table(table_name):
	"""
	Populo la tabla con los datos del _result.txt
	"""
	table_name_year = get_table_name_year(table_name)

	# si el fichero no tiene nada no hay nada que pasar a la BD
	if is_empty(TXT_FILE):
		log_msg4("WARNING: No se populó la tabla. dump.txt vacío!!")
		return

	# http://stackoverflow.com/questions/3971541/what-file-and-directory-permissions-are-required-for-mysql-load-data-infile
	# http://www.markhneedham.com/blog/2011/01/18/mysql-the-used-command-is-not-allowed-with-this-mysql-version/
	query = "LOAD DATA LOCAL INFILE '" + TXT_FILE + "' INTO TABLE " + \
		table_name_year + " IGNORE 1 LINES;"

	log_msg4("Volcando sobre " + table_name_year)

	exec_mysql(DB_NAME, query=query, options=['local-infile'])

	log_msg_ok4()


def populate(table_name, date):
	"""
	Realiza todo el proceso para popular cada tabla
	"""
	log_msg3("Populando " + table_name)

	wsq_to_txt(table_name, date)

	# si es un nuevo año se crea una nueva tabla
	if(is_new_year(table_name) and not new_tables_created):
		create_tables()

	txt_to_table(table_name)

	log_msg_ok3()


#
# RUN
#
def run(date):
	"""
	POPULA VISITEDYYYY, SAVEDYYYY y ACTIONSYYYY
	(YYYY corresponde al año, por ejemplo 'SAVED2013')
	"""
	global new_tables_created
	new_tables_created = False

	analysis_processed = getConfig().is_processed_for(date, 'analysis')

	if not analysis_processed:
		log_msg2('Populando analysis')
		populate('visited', date)
		populate('saved', date)
		populate('actions', date)
		getConfig().add_to_processed_list(date, 'analysis')
		log_msg_ok2()
	else:
		log_msg2(
			'La fecha ' + date.strftime('%Y-%m-%d') + ' ya fue anteriormente '
			'procesada para analysis.',
			state='processed')
