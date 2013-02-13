#!/usr/bin/python
# -*- coding: utf8 -*-

from shutil import copy
from helpers.config_helper import *
from helpers.logging_helper import *
from helpers.exec_helper import exec_proc, halt


# ejecutamos wikisquilter sobre el log de la fecha dada
def run(date, test):

	DB_USER = Config().get_db_user()
	DB_PASS = Config().get_db_password()
	DB_NAME = "squidlogs"
	DB_HOST = Config().get_db_host()
	DB_PORT = Config().get_db_port()

	if test:
		LOGS_DIR = Config().get_dir_test_logs()
	else:
		LOGS_DIR = Config().get_dir_logs()

	LOG_FILENAME = Config().get_log_filename(date)
	LOG_MONTH = Config().get_log_month(LOG_FILENAME)

	# cambiamos al directorio /wikisquilter desde donde ejecutamos este script
	os.chdir(Config().get_dir_wikisquilter())

	log_msg2("Ejecutando wikisquilter sobre " + LOG_FILENAME)

	# copiamos el log a procesar a la carpeta wikisquilter/squidlogfiles
	log_msg3("Copiando " + LOG_FILENAME + " a /squidlogfiles")

	SQUIDLOGFILES_DIR = Config().get_dir_squidlogfiles()
	try:
		copy(LOGS_DIR + LOG_FILENAME, SQUIDLOGFILES_DIR)
	except IOError as err:
		halt(err)

	log_msg_ok3()

	# ejecutamos wikisquilter
	cmd = "java -cp " + \
		"./build/classes:./dist/lib/mysql-connector-java-5.1.5-bin.jar " + \
		"wikisquilter.Main " + \
		"'jdbc:mysql://" + DB_HOST + ":" + DB_PORT + "/" + \
			DB_NAME + "' " + DB_USER + " " + DB_PASS + \
		" AllRequests Filtered Searches " + \
		"cfgWPFilter.xml " + \
		"./squidlogfiles -f " + LOG_FILENAME + " " + LOG_MONTH + " " + \
		'sal33.txt err33.txt -d -f -i -r &'

	log_msg3("Ejecutando")
	exec_proc(cmd)
	log_msg_ok3()

	# eliminamos el log procesado de la carpeta wikisquilter/squidlogfiles
	log_msg3("Eliminando " + LOG_FILENAME + " de /squidlogfiles")
	try:
		os.remove(SQUIDLOGFILES_DIR + LOG_FILENAME)
	except OSError as err:
		halt(err)
	log_msg_ok3()

	# vuelvo al directorio padre para que no haya problema a la hora de
	# ejecutar el siguiente módulo, ya que para ejecutar wikisquilter estábamos en /wikisquilter
	# os.chdir("..")

	log_msg_ok2()
