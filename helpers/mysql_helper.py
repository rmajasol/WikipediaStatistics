#!/usr/bin/python
# -*- coding: utf8 -*-

# Nos ayudará para interactuar con la BD

from config_helper import Config
from exec_helper import exec_proc


DB_USER = Config().get_db_user()
DB_PASS = Config().get_db_password()


def create_sql_file(query):
	"""
	Crea un archivo [carpeta_archivos_temporales]/query.sql con una query dada.
	Finalmente se devuelve nombre del archivo .sql junto a su ruta absoluta
	"""
	sql_file = Config().get_dir_tmp() + "query.sql"

	# escribimos la query en un .sql temporal
	f = open(sql_file, "w")
	f.write(query)
	f.close()

	return sql_file


def exec_mysql_query(database, query, **kwargs):
	"""
	Ejecuta la query escrita en el archivo query.sql

	http://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/
	**kwargs puede estar vacío o contener un hash con las
	siguientes claves:
		* dumped: si tiene valor 'True' volcará el resultado
			de la query sobre un fichero dumped.txt
		* options: esta clave tiene como valor un array de
			Strings, de modo que en el comando mysql 'cmd' se
			inyectarán tantas opciones de ejecución como
			elementos posea dicho array

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

	# seteamos cada variable según el contenido de kwargs
	for key in kwargs:
		if key == 'dumped':
			dumped = kwargs[key]
		elif key == 'options':
			options = kwargs[key]

	# creamos el archivo query.sql
	sql_file = create_sql_file(query)

	# construimos el comando 'cmd'
	cmd = "mysql "

	for option in options:
		cmd += "--" + option + " "

	cmd += 	"-D " + database + " -u " + DB_USER + " -p" + DB_PASS + \
			" < " + sql_file

	if dumped:
		cmd += 	" > " + Config().get_dir_tmp() + "dumped.txt"

	# ejecutamos el comando
	exec_proc(cmd)
