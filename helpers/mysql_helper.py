#!/usr/bin/python
# -*- coding: utf8 -*-

# Nos ayudará para interactuar con la BD

from exec_helper import exec_proc
from helpers.config_helper import getConfig


DB_USER = getConfig().get_db_user()
DB_PASS = getConfig().get_db_password()


def create_sql_file(query):
	"""
	Crea un archivo [carpeta_archivos_temporales]/query.sql con una query dada.
	Finalmente se devuelve nombre del archivo .sql junto a su ruta absoluta
	"""
	sql_file = getConfig().get_dir_tmp() + "query.sql"

	# escribimos la query en un .sql temporal
	f = open(sql_file, "w")
	f.write(query)
	f.close()

	return sql_file


def exec_mysql(database, **kwargs):
	"""
	Ejecuta la query, ya sea especificada en un String o se cargue desde un archivo .sql

	http://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/
	**kwargs puede estar vacío o contener un hash con las
	siguientes claves:
		* query: indica la query a ejecutar
		* dumped: si tiene valor 'True' volcará el resultado
			de la query sobre un fichero dumped.txt
		* options: esta clave tiene como valor un array de
			Strings, de modo que en el comando mysql 'cmd' se
			inyectarán tantas opciones de ejecución como
			elementos posea dicho array
		* sql_file: indica el archivo .sql a ejecutar (en lugar de una query)

	Por ejemplo si kwargs['options'] = ['local-infile'], entonces
	se ejecutaría así:
		mysql --local-infile -D..[resto de argumentos]

	Si hay error de 'acceso denegado' hay que dar este permiso:
	http://dev.mysql.com/doc/refman/5.0/es/access-denied.html
	GRANT FILE ON *.* TO 'ajreinoso'@'localhost';
	"""
	# Dejamos estos 2 valores por defecto
	options = []
	dumped = False
	query = None
	sql_file = None

	# seteamos cada variable según el contenido de kwargs
	for key in kwargs:
		if key == 'dumped':
			dumped = kwargs[key]
		elif key == 'options':
			options = kwargs[key]
		elif key == 'query':
			query = kwargs[key]
		elif key == 'sql_file':
			sql_file = kwargs[key]

	# creamos el archivo query.sql si no recibimos la opción sql_file='archivo.sql'
	sql_file = create_sql_file(query) if not sql_file else sql_file

	# construimos el comando 'cmd'
	cmd = "mysql "

	for option in options:
		cmd += "--" + option + " "

	cmd += 	"-D " + database + " -u " + DB_USER + " -p" + DB_PASS + \
			" < " + sql_file

	if dumped:
		cmd += 	" > " + getConfig().get_dumped_txt_filename()

	# ejecutamos el comando
	exec_proc(cmd)
