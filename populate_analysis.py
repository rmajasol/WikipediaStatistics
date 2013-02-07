#!/usr/bin/python
# -*- coding: utf8 -*-

import re
from helpers.config_helper import Config
from helpers.logging_helper import *
from helpers.mysql_helper import *

db_name = ""
DB_USER = Config().get_db_user()
DB_PASS = Config().get_db_password()
TMP_DIR = Config().get_dir_tmp()
TXT_FILE = TMP_DIR + "dumped.txt"

# indica el año del txt donde se vuelca el resultado de la query a squidlogs
txt_year = ""

# indica si este módulo se ejecuta en modo test o no
test_mode = False


def is_empty(filename):
	"""
	mira si un fichero esta vacío
	"""
	f = open(filename)
	return f.readline() == ""


def get_table_name_year(table_name):
	"""
	Devuelve el nombre de la tabla junto con el año obtenido del .txt
	que contiene los resultados de la query a squidlogs
	"""
	return table_name + txt_year


def wsq_to_txt(table_name):
	"""
	Vuelca en tmp/[table_name]_wsq_result.txt el resultado
	de la query a la BD squidlogs
	"""
	if(table_name == 'visited'):
		query = "select date(f_date_time), substr(dayname(f_date_time),1,2), " + \
			"f_lang_id, f_ns_id, count(*) " + \
			"from Filtered where f_action_id is null " + \
			"group by date(f_date_time), f_lang_id, f_ns_id;"
	elif(table_name == 'saved'):
		query = "select date(f_date_time), substr(dayname(f_date_time),1,2), " + \
			"f_lang_id, f_ns_id, count(*) " + \
			"from Filtered where f_action_id = 2 " + \
			"group by date(f_date_time), f_lang_id, f_ns_id;"
	elif(table_name == 'actions'):
		query = "select date(f_date_time), substr(dayname(f_date_time),1,2), " + \
			"f_action_id, f_lang_id, f_ns_id, count(*) " + \
			"from Filtered where f_action_id in (0, 1, 3, 4) " + \
			"group by date(f_date_time), f_action_id, f_lang_id, f_ns_id;"

	log_msg4("Creando dump para " + table_name)

	exec_mysql_query('squidlogs', query, dumped=True)

	log_msg_ok4()


def not_created_table(table_name):
	"""
	Mira en el txt el año y si no hay creada una tabla para ese
	año devolverá True
	"""
	# si el fichero no tiene nada devolvemos False para no crear luego una tabla vacia
	if is_empty(TXT_FILE):
		log_msg4("result.txt vacío!!")
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
		# seteamos txt_year con el año del result.txt
		global txt_year
		txt_year = m.group(1)

		# indica el año de la tabla más reciente
		latest_table_year = Config().get_latest_table_year(table_name, test_mode)

		return txt_year != latest_table_year


def create_table(table_name):
	"""
	Crea la tabla y actualiza el config.cfg con el nuevo año para
	el que ha sido creada
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

	log_msg4("Tabla " + table_name_year + " no creada. Creando")

	exec_mysql_query(db_name, query)

	log_msg_ok4()

	# actualizo el fichero de configuracion avisando que se creo la tabla para ese anio
	log_msg4("Cambiando año a %s para %s en config.cfg" % (txt_year, table_name))
	Config().set_latest_table_year(table_name, txt_year, test_mode)
	log_msg_ok4()


def txt_to_table(table_name):
	"""
	Populo la tabla con los datos del _result.txt
	"""
	# si el fichero no tiene nada no hay nada que pasar a la BD
	if is_empty(TXT_FILE):
		return

	table_name_year = get_table_name_year(table_name)

	# http://stackoverflow.com/questions/3971541/what-file-and-directory-permissions-are-required-for-mysql-load-data-infile
	# http://www.markhneedham.com/blog/2011/01/18/mysql-the-used-command-is-not-allowed-with-this-mysql-version/
	query = "LOAD DATA LOCAL INFILE '" + TXT_FILE + "' INTO TABLE " + \
		table_name_year + " IGNORE 1 LINES;"

	log_msg4("Volcando sobre " + table_name_year)

	exec_mysql_query(db_name, query, options=['local-infile'])

	log_msg_ok4()


def populate(table_name):
	"""
	Realiza todo el proceso para popular cada tabla
	"""
	log_msg3("Populando " + table_name)

	wsq_to_txt(table_name)

	# si es un nuevo anio creo la nueva tabla visitedxxxx para el anio
	if(not_created_table(table_name)):
		create_table(table_name)

	txt_to_table(table_name)

	log_msg_ok3()


#
#
#
def run(date, test):
	"""
	POPULA VISITEDYYYY, SAVEDYYYY y ACTIONSYYYY
	(YYYY corresponde al año, por ejemplo 'SAVED2013')
	"""
	global test_mode
	test_mode = test

	# si estamos ejecutando en modo test se populará la B.D. test_analysis
	global db_name
	db_name = "test_analysis" if test_mode else "analysis"

	log_msg2("Populando " + db_name)

	populate('visited')
	populate('saved')
	populate('actions')
	Config().add_to_processed_list(date, test_mode)

	log_msg_ok2()
