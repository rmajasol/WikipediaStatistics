#!/usr/bin/python
# -*- coding: utf8 -*-

# nos ayudará para realizar querys en el script

from config_helper import Config
from exec_helper import exec_proc


DB_USER = Config().get_db_user()
DB_PASS = Config().get_db_password()
TMP_DIR = Config().get_dir_tmp()


def mysql_query(database, query, sql_file):
	"""
	Crea una query a escribir en un archivo [sql_file].sql
	y luego la ejecuta
	"""
	# definimos ruta + archivo .sql
	sql_file = TMP_DIR + sql_file + ".sql"

	# escribimos la query en un .sql temporal
	f = open(sql_file, "w")
	f.write(query)
	f.close()

	cmd = "mysql -D " + database + " -u " + DB_USER + " -p" + DB_PASS + \
		" < " + sql_file

	exec_proc(cmd)
