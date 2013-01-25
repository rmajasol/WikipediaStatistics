#!/usr/bin/python
# -*- coding: utf8 -*-

import os
from shutil import copy
import subprocess
# import shlex
# import time
# import signal
import logging
from config_helper import Config


# ejecutamos wikisquilter sobre el log de la fecha dada
def run(date, test=False):

	DB_USER = Config().get_db_user()
	DB_PASS = Config().get_db_password()
	DB_NAME = Config().get_db_name()
	DB_HOST = Config().get_db_host()
	DB_PORT = Config().get_db_port()

	if test:
		LOGS_DIR = Config().get_test_logs_dir()
	else:
		LOGS_DIR = Config().get_logs_dir()

	LOG_FILENAME = "log-" + date.strftime('%Y%m%d') + ".gz"
	LOG_MONTH = LOG_FILENAME[8:10]

	# cambiamos al directorio /wikisquilter desde donde ejecutamos este script
	os.chdir("wikisquilter")

	# copiamos el log a procesar a la carpeta wikisquilter/squidlogfiles
	SQUIDLOGFILES_DIR = Config().get_squidlogsfiles_dir()
	copy(LOGS_DIR + LOG_FILENAME, SQUIDLOGFILES_DIR)

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

	logging.info("Ejecutando wikisquilter sobre: " + LOG_FILENAME)

	# http://stackoverflow.com/questions/1996518/retrieving-the-output-of-subprocess-call
	# Así hacemos para que este script espere a la finalización de wikisquilter
	output, error = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

	logging.info(LOG_FILENAME + " procesado OK")

	# eliminamos el log procesado de la carpeta wikisquilter/squidlogfiles
	os.remove(SQUIDLOGFILES_DIR + "/" + LOG_FILENAME)

	# vuelvo al directorio padre para que no haya problema a la hora de
	# ejecutar el siguiente módulo, ya que para ejecutar wikisquilter estábamos en /wikisquilter
	os.chdir("..")
