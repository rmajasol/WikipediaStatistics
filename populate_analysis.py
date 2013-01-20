#!/usr/bin/python
# -*- coding: utf8 -*-

import os
import shlex
import subprocess
from config_helper import Config
import re
import logging

DB_USER = Config().get_db_user()
DB_PASS = Config().get_db_password()
TMP_DIR = Config().get_tmp_dir()

# indica el año del txt donde se vuelca el resultado de la query
txt_year = ""


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

	print "Creando txt a partir de la consulta " + table_name
	args = shlex.split(cmd)
	output, error = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()


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


# crea la tabla y actualiza el config.cfg con el nuevo anio para el que ha sido creada
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

	cmd = "mysql -D analysis -u " + DB_USER + " -p" + DB_PASS + \
		" < " + sql_file

	print "Creando tabla " + table_name + txt_year
	args = shlex.split(cmd)
	output, error = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

	# actualizo el fichero de configuracion avisando que se creo la tabla para ese anio
	Config().write("latest_tables", table_name, txt_year)


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

	cmd = "mysql --local-infile -D analysis -u " + DB_USER + " -p" + DB_PASS + \
		" < " + sql_file

	print "Volcando txt sobre tabla " + table_name + txt_year
	args = shlex.split(cmd)
	output, error = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

	# si dice acceso denegado hay que dar permiso: http://dev.mysql.com/doc/refman/5.0/es/access-denied.html
	# GRANT FILE ON *.* TO 'ajreinoso'@'localhost';


# hace todo el proceso para popular cada tabla
def populate(table_name):
	logging.info("Populando tabla: " + table_name + txt_year)
	print "Populando tabla: " + table_name + txt_year

	wsq_to_txt(table_name)

	# si es un nuevo anio creo la nueva tabla visitedxxxx para el anio
	if(not_created_table(table_name)):
		logging.info("Tabla %s no creada. Creando...' % (table_name + txt_year)")
		create_table(table_name)

	txt_to_table(table_name, txt_year)


#
#	POPULA VISITEDXXXX, SAVEDXXXX y ACTIONSXXXX
#
def run():
	populate('visited')
	populate('saved')
	populate('actions')
