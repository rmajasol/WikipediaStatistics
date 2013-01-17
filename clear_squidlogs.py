#!/usr/bin/python

import os
from config_helper import Config

DB_USER = Config().get_db_user()
DB_PASS = Config().get_db_password()
DB_NAME = Config().get_db_name()
DB_HOST = Config().get_db_host()
TMP_DIR = Config().get_tmp_dir()
TMP_SQL = "tmp_clear_squidlogs.sql"

query = "DROP DATABASE IF EXISTS " + DB_NAME + ";" + \
		"CREATE DATABASE " + DB_NAME + " DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;" + \
		"GRANT ALL PRIVILEGES ON `" + DB_NAME + "` . * " + \
			"TO '" + DB_USER + "'@'" + DB_HOST + "' WITH GRANT OPTION ;" + \
		"GRANT ALL PRIVILEGES ON `" + DB_NAME + "` . * " + \
			"TO '" + DB_USER + "'@'%' WITH GRANT OPTION ;"

# escribimos la query en un .sql temporal
f = open(TMP_DIR + "tmp_clear_squidlogs.sql", "w")
f.write(query)
f.close()

os.system("mysql -u " + DB_USER + " -p" + DB_PASS + \
	" < " + TMP_DIR + TMP_SQL)
