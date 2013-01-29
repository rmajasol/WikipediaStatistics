#!/usr/bin/python
# -*- coding: utf8 -*-

import re
from helpers.config_helper import Config
from helpers.logging_helper import *
from helpers.exec_helper import exec_proc

DB_USER = Config().get_db_user()
DB_PASS = Config().get_db_password()
TMP_DIR = Config().get_dir_tmp()
PROCESSED_LIST = Config().get_filename_processed_list()

# indica el año del txt donde se vuelca el resultado de la query
txt_year = ""

# indica si este módulo se ejecuta en modo test o no
test_mode = False
# si estamos ejecutando en modo test se populará la B.D. test_analysis
DB_NAME = "test_analysis" if test_mode else "analysis"


# mira si un fichero esta vacio
def is_empty(filename):
	f = open(filename)
	if f.readline() == "":
		return True
	else:
		return False


# crea un archivo .sql temporal con una query dada.
# El archivo tendrá un nombre u otro dependiendo del tipo de query que hagamos (query_type):
# 	* wsq_query: querys a wikisquilter
#   * create_table: para crear la tabla
#	* txt_to_analysis: para popular BD analysis a partir del txt
#
# finalmente se devuelve la ruta del archivo tmp/[tabla]_[query_type].sql
def create_sql_file(query, table_name, query_type):
	sql_file = TMP_DIR + table_name + "_" + query_type + ".sql"
	f = open(sql_file, "w")
	f.write(query)
	f.close()
	return sql_file


# devuelve el nombre del archivo .txt
def txt_file(table_name):
	return TMP_DIR + table_name + "_wsq_result.txt"


# devuelve el nombre del archivo .err
def err_file(table_name):
	return TMP_DIR + table_name + "_wsq_result.err"


# vuelca en [table_name]_wsq_result.txt el resultado de la query a la BD squidlogs
def wsq_to_txt(table_name):
	global query
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

	# escribe la query en el archivo tmp/[table_name]_wsq_query.sql
	sql_file = create_sql_file(query, table_name, "wsq_query")

	cmd = "mysql -D squidlogs -u " + DB_USER + " -p" + DB_PASS + \
		" < " + sql_file + \
		" > " + txt_file(table_name) + \
		" 2>" + err_file(table_name)

	log_msg4("Creando .txt a partir de la consulta a " + table_name)
	exec_proc(cmd)
	log_msg_ok4()


# mira en el txt el año y si no hay creada una tabla para ese año devolverá True
def not_created_table(table_name):
	txt = txt_file(table_name)
	# si el fichero no tiene nada devolvemos False para no crear luego una tabla vacia
	if is_empty(txt):
		return False
	else:
		f = open(txt)
		f.readline()
		# la primera linea no interesa, asi que volvemos a leer
		l = f.readline()
		m = re.match(".*(\d{4})\-\d{2}.*", l)
		global txt_year
		txt_year = m.group(1)
		# indica el año de la tabla más reciente
		latest_table_year = Config().read("latest_tables", table_name)
		if (txt_year != latest_table_year):
			return True
		else:
			return False


# crea la tabla y actualiza el config.cfg con el nuevo año para el que ha sido creada
def create_table(table_name):
	query = "DROP TABLE IF EXISTS " + table_name + txt_year + ";" + \
			"CREATE TABLE " + table_name + txt_year + " (" + \
				"day DATE," + \
				"dayWeek VARCHAR(2),"

	# si la tabla es actions hay que añadir este campo
	if(table_name == 'actions'):
		query += "action TINYINT,"

	query += "lang VARCHAR(2)," + \
				"ns TINYINT," + \
				"count int" + \
			");" + \
			"alter table " + table_name + txt_year + " add index (day, dayWeek, lang, ns);"

	# escribe la query en el archivo tmp/[table_name]_create.sql
	sql_file = create_sql_file(query, table_name, "create")

	cmd = "mysql -D " + DB_NAME + " -u " + DB_USER + " -p" + DB_PASS + \
		" < " + sql_file

	# ejecuto la query para crear la tabla
	log_msg4("Tabla %s no creada. Creando" % (table_name + txt_year))
	exec_proc(cmd)
	log_msg_ok4()

	# actualizo el fichero de configuracion avisando que se creo la tabla para ese anio
	log_msg4("Cambiando año a %s para %s en config.cfg" % (txt_year, table_name))
	Config().write("latest_tables", table_name, txt_year)
	log_msg_ok4()


# populo la tabla con los datos del _result.txt
def txt_to_table(table_name, txt_year):
	txt = txt_file(table_name)
	# si el fichero no tiene nada no hay nada que pasar a la BD
	if is_empty(txt):
		return
	# http://stackoverflow.com/questions/3971541/what-file-and-directory-permissions-are-required-for-mysql-load-data-infile
	# http://www.markhneedham.com/blog/2011/01/18/mysql-the-used-command-is-not-allowed-with-this-mysql-version/
	query = "LOAD DATA LOCAL INFILE '" + txt + "' INTO TABLE " + \
		table_name + txt_year + " IGNORE 1 LINES;"

	# tmp/[table]_txt_to_analysis.sql
	sql_file = create_sql_file(query, table_name, "txt-to-analysis")

	cmd = "mysql --local-infile -D " + DB_NAME + " -u " + DB_USER + " -p" + DB_PASS + \
		" < " + sql_file

	log_msg4("Volcando txt sobre tabla " + table_name + txt_year)
	exec_proc(cmd)
	log_msg_ok4()

	# si dice acceso denegado hay que dar permiso: http://dev.mysql.com/doc/refman/5.0/es/access-denied.html
	# GRANT FILE ON *.* TO 'ajreinoso'@'localhost';


# hace todo el proceso para popular cada tabla
def populate(table_name):
	log_msg3("Populando la tabla " + table_name + txt_year + "..")

	wsq_to_txt(table_name)

	# si es un nuevo anio creo la nueva tabla visitedxxxx para el anio
	if(not_created_table(table_name)):
		create_table(table_name)

	txt_to_table(table_name, txt_year)

	log_msg_ok3()


# añade el log ya procesado a la lista del archivo logs.processed
def add_to_processed_list(date):
	log_date = Config().get_log_date(date)
	f = open(PROCESSED_LIST, "a")
	f.write(log_date + "\n")
	f.close()


#
#	POPULA VISITEDXXXX, SAVEDXXXX y ACTIONSXXXX
#
def run(date, test):
	global test_mode
	test_mode = test

	log_msg2("POPULANDO ANALYSIS")

	populate('visited')
	populate('saved')
	populate('actions')

	add_to_processed_list(date)

	log_msg_ok2()
