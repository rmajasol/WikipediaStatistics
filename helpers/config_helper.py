# -*- coding: utf8 -*-

import ConfigParser
import os
import sys


# creamos esta clase como helper para interactuar con el fichero de configuracion
class Config(object):

	SECTION__HOSTS = "hosts"
	SECTION__DB = "db"
	SECTION__LATEST_TABLES = "latest_tables"

	cfg = ConfigParser.ConfigParser()

	def __init__(self):
		self.base_path = self.get_base_path()
		self.config_file = self.base_path + "config.cfg"
		self.cfg.read([self.config_file])

	def read(self, section, name):
		"""
		Lee el nombre de un párametro dentro de una sección en
		el archivo de configuracion
		"""
		return self.cfg.get(section, name)

	def write(self, section, name, value):
		"""
		Modifica un parámetro dentro de una sección en el archivo de configuración
		"""
		self.cfg.set(section, name, value)
		f = open(self.config_file, "w")
		self.cfg.write(f)
		f.close()

	#
	# SECTION__DB
	#
	def get_db_user(self):
		"""
		Lee el fichero de configuración 'config.cfg' para obtener
		el nombre de usuario con el que conectar a la BD
		"""
		return self.read(self.SECTION__DB, "db_user")

	def get_db_password(self):
		return self.read(self.SECTION__DB, "db_pass")

	def get_db_name(self):
		return self.read(self.SECTION__DB, "db_name")

	def get_db_host(self):
		return self.read(self.SECTION__DB, "db_host")

	def get_db_port(self):
		return self.read(self.SECTION__DB, "db_port")

	#
	# SECTION__HOSTS
	#
	def get_host_remote(self):
		return self.read(self.SECTION__HOSTS, "remote")

	#
	# SECTION__LATEST_TABLES
	#
	def get_latest_table_year(self, table_name):
		"""
		Lee en el archivo de configuración el último año para el que
		ya está creada la tabla
		"""
		return self.read(self.SECTION__LATEST_TABLES, table_name)

	def set_latest_table_year(self, table_name, year):
		"""
		Escribe en el archivo de configuración el último año existente
		para la tabla
		"""
		self.write(self.SECTION__LATEST_TABLES, table_name, year)

	#
	# Directorios
	#
	def get_dir_logs(self):
		return self.base_path + "../../../logs/"

	def get_dir_logs_remote(self):
		return self.get_host_remote() + ":~/logs/"

	def get_dir_test_logs(self):
		return self.base_path + "../../../test_logs/"

	def get_dir_test_logs_remote(self):
		return self.get_host_remote() + ":~/test_logs/"

	def get_dir_tmp(self):
		return self.base_path + "tmp/"

	def get_dir_wikisquilter(self):
		return self.base_path + "wikisquilter/"

	def get_dir_squidlogfiles(self):
		return self.get_dir_wikisquilter() + "squidlogfiles/"

	def get_dir_run_history(self):
		return self.base_path + "run_history/"

	#
	# PROCESSED LIST (lista de fechas ya procesadas)
	#
	def get_processed_list_filename(self, test):
		"""
		Devuelve si la fecha dada ya está procesada
		"""
		if test:
			return self.base_path + "test/test_logs.processed"
		else:
			return self.base_path + "logs.processed"

	def is_processed_date(self, date, test):
		# http://maengora.blogspot.com.es/2010/10/receta-python-buscar-una-cadena-de-un.html
		filename = self.get_processed_list_filename(test)
		f = open(filename)
		lines = f.readlines()
		for l in lines:
			if l == self.get_log_date(date) + "\n":
				return True
		return False

	def add_to_processed_list(self, date, test):
		"""
		Añade el log ya procesado a la lista del archivo logs.processed
		http://chuwiki.chuidiang.org/index.php?title=Leer_y_escribir_ficheros_en_python
		"""
		log_date = self.get_log_date(date)
		filename = self.get_processed_list_filename(test)
		f = open(filename, "a")
		f.write(log_date + "\n")
		f.close()

	#
	# LOG FILENAME FORMAT
	#
	def get_log_filename(self, date):
		"""
		Devuelve el nombre de archivo para el log a partir de una fecha dada
		"""
		return "log-" + date.strftime('%Y%m%d') + ".gz"

	def get_log_month(self, log_file):
		"""
		Devuelve el mes dado el nombre de archivo del log,
		útil para pasarlo como argumento en la ejecución de wikisquilter
		"""
		return log_file[8:10]

	def get_log_date(self, date):
		"""
		Devuelve una cadena con la fecha en formato YYYYMMDD
		"""
		return date.strftime('%Y%m%d')

	def get_base_path(self):
		"""
		Devuelve la ruta absoluta de la raíz del proyecto
		http://stackoverflow.com/a/1296522/1260374
		"""
		dirname, filename = os.path.split(os.path.abspath(__file__))
		# puesto que estamos en /helpers subimos un directorio:
		# http://docs.python.org/2/library/os.path.html
		return os.path.join(dirname, '../')

	def set_pythonpath(self):
		"""
		Añade a la variable de entorno PYTHONPATH la ruta
		hacia la carpeta raíz del proyecto
		"""
		dirname, filename = os.path.split(os.path.abspath(__file__))
		sys.path.append(os.path.join(dirname, '../'))
