#!/usr/bin/python

import os
import ConfigParser
import re

# Leemos del archivo de configuracion 'config.cfg'
cfg = ConfigParser.ConfigParser()
cfg.read(["config.cfg"])
USER = cfg.get("bd_connection", "user")
PASS = cfg.get("bd_connection", "pass")
# indica el anio del txt donde se vuelca la query
txt_year = ""
query = ""
path = "tmp/"


# mira si un fichero esta vacio
def is_empty(filename):
	f = open(filename)
	if f.readline() == "":
		return True
	else:
		return False


# escribe la query en [table]tmp.sql, un archivo que usamos como temporal
def write_query(table_name):
	global path
	f = open(path + "tmp_" + table_name + ".sql", "w")
	f.write(query)
	f.close()


# vuelca en tmp.txt el resultado de la query a la BD squidlogs
def dump_query(table_name):
	global query
	global path
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
	write_query(table_name + "_query")
	os.system("mysql -D squidlogs -u " + USER + " -p" + PASS + \
		" < " + path + "tmp_" + table_name + "_query.sql" + \
		" > " + path + "tmp_" + table_name + "_result.txt" + \
		" 2>" + path + "tmp_" + table_name + "_result.err")


# mira en el txt el anio y si no hay creada una tabla para ese anio devolvera True
def not_created_table(table_name):
	global path
	filename = path + "tmp_" + table_name + "_result.txt"
	# si el fichero no tiene nada devolvemos False para no crear luego una tabla vacia
	if is_empty(filename):
		return False
	else:
		f = open(filename)
		f.readline()
		# la primera linea no interesa, asi que volvemos a leer
		l = f.readline()
		m = re.match(".*(\d{4})\-\d{2}.*", l)
		global txt_year
		txt_year = m.group(1)
		# indica el ultimo anio que hay creado para la tabla
		last_year_table = cfg.get("year_for_the_last_table_created", table_name)
		if (txt_year != last_year_table):
			return True
		else:
			return False


# crea la tabla y actualiza el config.cfg con el nuevo anio para el que ha sido creada
def create_table(table_name):
	global query
	global path
	query = "DROP TABLE IF EXISTS " + table_name + txt_year + ";" + \
			"CREATE TABLE " + table_name + txt_year + " (" + \
				"day DATE," + \
				"dayWeek VARCHAR(2),"

	if(table_name == 'actions'):
		query += "action TINYINT,"

	query += "lang VARCHAR(2)," + \
				"ns TINYINT," + \
				"count int" + \
			");" + \
			"alter table " + table_name + txt_year + " add index (day, dayWeek, lang, ns);"
	write_query(table_name + "_createTable")
	sql_file = path + "tmp_" + table_name + "_createTable.sql"
	os.system("mysql -D analysis -u " + USER + " -p" + PASS + \
		" < " + sql_file)

	# actualizo el fichero de configuracion avisando que se creo la tabla para ese anio
	cfg.set("year_for_the_last_table_created", table_name, txt_year)
	f = open("config.cfg", "w")
	cfg.write(f)
	f.close()


# populo la tabla con los datos del _result.txt
def txt_to_table(table_name):
	global path
	txt_filename = path + "tmp_" + table_name + "_result.txt"
	# si el fichero no tiene nada no hay nada que pasar a la BD
	if is_empty(txt_filename):
		return
	# http://stackoverflow.com/questions/3971541/what-file-and-directory-permissions-are-required-for-mysql-load-data-infile
	# http://www.markhneedham.com/blog/2011/01/18/mysql-the-used-command-is-not-allowed-with-this-mysql-version/
	global query
	query = "LOAD DATA LOCAL INFILE '" + txt_filename + "' INTO TABLE " + \
		table_name + txt_year + " IGNORE 1 LINES;"
	write_query(table_name + "_load")
	sql_file = path + "tmp_" + table_name + "_load.sql"
	os.system("mysql --local-infile -D analysis -u " + USER + " -p" + PASS + \
		" < " + sql_file)
	# si dice acceso denegado hay que dar permiso: http://dev.mysql.com/doc/refman/5.0/es/access-denied.html
	# GRANT FILE ON *.* TO 'ajreinoso'@'localhost';


# hace todo el proceso para popular la tabla
def populate(table_name):
	dump_query(table_name)

	# si es un nuevo anio creo la nueva tabla visitedxxxx para el anio
	if(not_created_table(table_name)):
		print 'Tabla %s no creada. Creando...' % (table_name + txt_year)
		create_table(table_name)

	txt_to_table(table_name)


#
#	POPULAR VISITEDXXXX
#
populate('visited')


#
#	POPULAR SAVEDXXXX
#
populate('saved')


#
#	POPULAR ACTIONSXXXX
#
populate('actions')
