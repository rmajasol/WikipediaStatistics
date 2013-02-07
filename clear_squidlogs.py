#!/usr/bin/python

from helpers.config_helper import *
from helpers.logging_helper import *
from helpers.mysql_helper import exec_mysql_query


def run():
	DB_USER = Config().get_db_user()
	DB_NAME = "squidlogs"
	DB_HOST = Config().get_db_host()

	query = "DROP DATABASE IF EXISTS " + DB_NAME + ";" + \
			"CREATE DATABASE " + DB_NAME + " DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;" + \
			"GRANT ALL PRIVILEGES ON `" + DB_NAME + "` . * " + \
				"TO '" + DB_USER + "'@'" + DB_HOST + "' WITH GRANT OPTION ;" + \
			"GRANT ALL PRIVILEGES ON `" + DB_NAME + "` . * " + \
				"TO '" + DB_USER + "'@'%' WITH GRANT OPTION ;"

	log_msg2("Limpiando B.D. squidlogs")

	exec_mysql_query(DB_NAME, query)

	log_msg_ok2()
