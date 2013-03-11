#!/usr/bin/python

from helpers.logging_helper import *
from helpers.mysql_helper import exec_mysql_query
from helpers.config_helper import getConfig


def run():
	DB_USER = getConfig().get_db_user()
	DB_NAME = getConfig().get_db_name('squidlogs')
	DB_HOST = getConfig().get_db_host()

	query = "DROP DATABASE IF EXISTS " + DB_NAME + ";" + \
			"CREATE DATABASE " + DB_NAME + " DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;" + \
			"GRANT ALL PRIVILEGES ON `" + DB_NAME + "` . * " + \
				"TO '" + DB_USER + "'@'" + DB_HOST + "' WITH GRANT OPTION ;" + \
			"GRANT ALL PRIVILEGES ON `" + DB_NAME + "` . * " + \
				"TO '" + DB_USER + "'@'%' WITH GRANT OPTION ;"

	log_msg2("Limpiando B.D. squidlogs")

	log_msg3("Creando BD..")
	exec_mysql_query(DB_NAME, query=query)
	log_msg_ok3()

	log_msg3("Creando tablas..")
	exec_mysql_query(DB_NAME, sql_file='squidlogs_tables.sql')
	log_msg_ok3()

	log_msg_ok2()
