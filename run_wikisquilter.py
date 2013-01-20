#!/usr/bin/python
# -*- coding: utf8 -*-

import os
import subprocess
import shlex
import time
import signal
import logging
from config_helper import Config


# ejecutamos wikisquilter sobre el log de la fecha dada
def run(date):
	#
	# probamos a procesar el log-20120615.gz
	# date = date.replace(year=2012, month=06, day=15)

	DB_USER = Config().get_db_user()
	DB_PASS = Config().get_db_password()
	DB_NAME = Config().get_db_name()
	DB_HOST = Config().get_db_host()
	DB_PORT = Config().get_db_port()

	# LOGS_DIR = Config().get_logs_dir()
	LOGS_DIR = Config().get_test_logs_dir()
	LOGS_DIR = LOGS_DIR[0:len(LOGS_DIR) - 1]

	LOG_FILENAME = "log-" + date.strftime('%Y%m%d') + ".gz"
	LOG_MONTH = LOG_FILENAME[8:10]

	# cambiamos al directorio /wikisquilter desde donde ejecutamos este script
	os.chdir("wikisquilter")

	logging.info("Ejecutando wikisquilter sobre: " + LOG_FILENAME)

	cmd = "java -cp " + \
		"./build/classes:./dist/lib/mysql-connector-java-5.1.5-bin.jar " + \
		"wikisquilter.Main " + \
		"'jdbc:mysql://" + DB_HOST + ":" + DB_PORT + "/" + \
			DB_NAME + "' " + DB_USER + " " + DB_PASS + \
		" AllRequests Filtered Searches " + \
		"cfgWPFilter.xml " + \
		LOGS_DIR + " -f " + LOG_FILENAME + " " + LOG_MONTH + " " + \
		'sal33.txt err33.txt -d -f -i -r &'

	# http://stackoverflow.com/questions/1996518/retrieving-the-output-of-subprocess-call
	#
	# Así hacemos para que este script espere a la finalización de wikisquilter
	args = shlex.split(cmd)
	output, error = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

	# pondremos este script 10 segundos en espera y luego mataremos el wikisquilter
	# time.sleep(10)
	# os.killpg(pro.pid, signal.SIGTERM)  # Send the signal to all the process groups

	# vuelvo al directorio padre para que no haya problema a la hora de
	# ejecutar el siguiente módulo, ya que para ejecutar wikisquilter estábamos en /wikisquilter
	os.chdir("..")
