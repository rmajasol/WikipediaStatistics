#!/usr/bin/python
# -*- coding: utf8 -*-

# Nos ayudará para interactuar con la BD

from config_helper import Config
from exec_helper import exec_proc


DB_USER = Config().get_db_user()
DB_PASS = Config().get_db_password()


def create_sql_file(query):
	"""
	crea un archivo [carpeta_archivos_temporales]/query.sql con una query dada.
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
	Ejecuta la query escrita en el archivo query.sql, indicándole tantas
	opciones de ejecución como elementos contenga el parámetro 'options'.
	Por ejemplo si options contiene sólo la opción 'local-infile'
	entonces se ejecutaría así:
		mysql --local-infile -D..

	Si hay error de 'acceso denegado' hay que dar permiso:
	http://dev.mysql.com/doc/refman/5.0/es/access-denied.html
	GRANT FILE ON *.* TO 'ajreinoso'@'localhost';

	Si el parámetro 'output' está a True entonces se vuelca el
	resultado en un archivo result.txt, indicándose en el
	archivo result.err si hubo error


	http://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/
	"""
	options = []
	dumped = False

	for key in kwargs:
		if key == 'dumped':
			dumped = kwargs[key]
		elif key == 'options':
			options = kwargs[key]

	sql_file = create_sql_file(query)

	# construimos el comando 'cmd'
	cmd = "mysql "

	for option in options:
		cmd += "--" + option + " "

	cmd += 	"-D " + database + " -u " + DB_USER + " -p" + DB_PASS + \
			" < " + sql_file

	if dumped:
		cmd += 	" > " + Config().get_dir_tmp() + "dumped.txt"

	exec_proc(cmd)
