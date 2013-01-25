#!/usr/bin/python

import subprocess
from config_helper import Config


def run():
	DB_USER = Config().get_db_user()
	DB_PASS = Config().get_db_password()
	DB_NAME = Config().get_db_name()
	DB_HOST = Config().get_db_host()
	TMP_DIR = Config().get_tmp_dir()
	SQL_FILE = TMP_DIR + "clear_squidlogs.sql"

	query = "DROP DATABASE IF EXISTS " + DB_NAME + ";" + \
			"CREATE DATABASE " + DB_NAME + " DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;" + \
			"GRANT ALL PRIVILEGES ON `" + DB_NAME + "` . * " + \
				"TO '" + DB_USER + "'@'" + DB_HOST + "' WITH GRANT OPTION ;" + \
			"GRANT ALL PRIVILEGES ON `" + DB_NAME + "` . * " + \
				"TO '" + DB_USER + "'@'%' WITH GRANT OPTION ;"

	# escribimos la query en un .sql temporal
	f = open(SQL_FILE, "w")
	f.write(query)
	f.close()

	cmd = "mysql -u " + DB_USER + " -p" + DB_PASS + \
		" < " + SQL_FILE

	output, error = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
