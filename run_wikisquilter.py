#!/usr/bin/python
# -*- coding: utf8 -*-

import os
from shutil import copy
from helpers.config_helper import getConfig
from helpers.logging_helper import *
from helpers.exec_helper import exec_proc, halt


log_filename = None


def run_wsq(date):
	"""
	Ejecutamos wikisquilter sobre el log de la fecha dada
	"""

	DB_USER = getConfig().get_db_user()
	DB_PASS = getConfig().get_db_password()
	DB_NAME = getConfig().db_name_squidlogs
	DB_HOST = getConfig().get_db_host()
	DB_PORT = getConfig().get_db_port()

	LOGS_DIR = getConfig().get_dir_local_logs()
	LOG_MONTH = getConfig().get_log_month(log_filename)
	SQUIDLOGFILES_DIR = getConfig().get_dir_squidlogfiles()

	# copiamos el log a procesar a la carpeta wikisquilter/squidlogfiles
	log_msg3("Copiando " + log_filename + " a la carpeta 'squidlogfiles'")
	# cambiamos al directorio /wikisquilter desde donde ejecutamos este script
	os.chdir(getConfig().get_dir_wikisquilter())
	try:
		copy(LOGS_DIR + log_filename, SQUIDLOGFILES_DIR)
	except IOError as err:
		halt(err)
	log_msg_ok3()

	#
	# Según la lista de logs procesados 'logs.processed' esté vacía o no
	# se escogerá una opción u otra.
	#
	# 		-d  Elimina todas las tablas existentes en squidlogs y crea nuevas vacías
	#			para insertar en ellas únicamente los datos de la fecha a procesar.
	#		-a 	Añade a las tablas existentes los datos procesados, sin eliminar
	#		   	por tanto las anteriores fechas procesadas de squidlogs
	#			(las tablas deben existir).
	#
	# Si se escoge -a entonces
	#
	OPTION = '-d' if getConfig().is_processed_list_empty('squidlogs') else '-a'
	# ejecutamos wikisquilter
	cmd = "java -cp " + \
		"./build/classes:./dist/lib/mysql-connector-java-5.1.5-bin.jar " + \
		"wikisquilter.Main " + \
		"'jdbc:mysql://" + DB_HOST + ":" + DB_PORT + "/" + \
			DB_NAME + "' " + DB_USER + " " + DB_PASS + \
		" AllRequests Filtered Searches " + \
		"cfgWPFilter.xml " + \
		"./squidlogfiles -f " + log_filename + " " + LOG_MONTH + " " + \
		"sal33.txt err33.txt " + OPTION + " -f -i -r &"
	log_msg3("Ejecutando")
	exec_proc(cmd)
	log_msg_ok3()

	# eliminamos el log procesado de la carpeta wikisquilter/squidlogfiles
	log_msg3("Eliminando " + log_filename + " de la carpeta 'squidlogfiles'")
	try:
		os.remove(SQUIDLOGFILES_DIR + log_filename)
	except OSError as err:
		halt(err)
	log_msg_ok3()

	# vuelvo al directorio padre para que no haya problema a la hora de
	# ejecutar el siguiente módulo, ya que para ejecutar wikisquilter estábamos en /wikisquilter
	# os.chdir("..")

	getConfig().add_to_processed_list(date, 'squidlogs')


def run(date):

	global log_filename
	log_filename = getConfig().get_log_filename(date)

	squidlogs_processed = getConfig().is_processed_for(date, 'squidlogs')

	if not squidlogs_processed:
		log_msg2("Ejecutando wikisquilter sobre " + log_filename)
		run_wsq(date)
		log_msg_ok2()
	else:
		log_msg2(log_filename + " ya fue anteriormente procesado por WikiSquilter.", state='processed')
