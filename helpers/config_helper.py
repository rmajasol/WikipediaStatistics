# -*- coding: utf8 -*-

import ConfigParser
import os
import sys
import re


from utils import *


class Config(object):
	"""
	Creamos esta clase como helper para interactuar con el fichero
	de configuracion y realizar otras funciones de utilidad
	"""

	# secciones en el archivo de configuración 'config.cfg'
	SECTION__HOSTS = 'hosts'
	SECTION__DB_CONNECTION = 'db_connection'
	SECTION__DB_NAMES = 'db_names'
	SECTION__LOCAL_DIRS = 'local_dirs'
	SECTION__REMOTE_DIRS = 'remote_dirs'

	cfg = ConfigParser.ConfigParser()

	def __init__(self, test_mode):
		"""
		Carga la ruta base donde se aloja este código y el fichero de
		configuración 'config.cfg'
		"""
		self.base_path = self.get_base_path()
		self.config_file = self.base_path + "config.cfg"
		self.cfg.read([self.config_file])
		self.test_mode = test_mode

		# El nombre de la carpeta que aloja logs de prueba se llama 'test_logs'.
		# Para logs reales símplemente 'logs'.
		self.logs_dirname = 'test_logs' if self.test_mode else 'logs'

		# Definimos cómo se llamarán las BDs squidlogs y analysis
		self.db_name_squidlogs = self.get_db_name('squidlogs')
		self.db_name_analysis = self.get_db_name('analysis')

	#
	#
	# Métodos de ayuda para la lectura/escritura en 'config.cfg'
	#
	def read(self, section, name):
		"""
		Lee el nombre de un parámetro dentro de una sección en
		el archivo de configuracion
		"""

		# cadena leída del fichero de configuración dada una sección y su nombre
		# e.g.: section = [dirs], name = local_test
		value = self.cfg.get(section, name)

		if section == self.SECTION__LOCAL_DIRS or section == self.SECTION__REMOTE_DIRS:
			# si es esta sección entonces añadimos al final de 'cad' el caracter
			# '/' si no lo tiene
			path = value + '/' if value[:-1] != '/' else value
			return path
		else:
			return value

	def write(self, section, name, value):
		"""
		Modifica un parámetro dentro de una sección en el archivo
		de configuración
		"""
		self.cfg.set(section, name, value)
		f = open(self.config_file, "w")
		self.cfg.write(f)
		f.close()

	#
	#
	# SECTION__DB_
	#
	def get_db_user(self):
		"""
		Lee el fichero de configuración 'config.cfg' para obtener
		el nombre de usuario con el que conectar a la BD
		"""
		return self.read(self.SECTION__DB_CONNECTION, "db_user")

	def get_db_password(self):
		return self.read(self.SECTION__DB_CONNECTION, "db_pass")

	def get_db_host(self):
		return self.read(self.SECTION__DB_CONNECTION, "db_host")

	def get_db_port(self):
		return self.read(self.SECTION__DB_CONNECTION, "db_port")

	def get_db_name(self, name):
		"""
		Posibles nombres:
			* squidlogs
			* analysis

			Si es en modo test:
				* test_squidlogs
				* test_analysis
		"""
		return 'test_' + name if self.test_mode else name

	#
	#
	# SECTION__HOSTS
	#
	def get_host_remote(self):
		return self.read(self.SECTION__HOSTS, "remote")

	#
	#
	# Directorios para los logs
	#
	def get_dir_local_logs(self):
		"""
		Devuelve ruta hacia los logs en equipo local
		"""
		path = self.read(self.SECTION__LOCAL_DIRS, self.logs_dirname)

		# si es un directorio local y la ruta es absoluta, devolvemos la ruta
		# tal cual, pero si es relativa a la del proyecto entonces devolvemos
		# la ruta del proyecto + ruta relativa
		return path if is_absolute(path) else self.base_path + path

	def get_dir_remote_logs(self):
		"""
		Devuelve dirección de equipo remoto + ruta hacia 'logs' o 'test_logs' allí
		"""
		path = self.read(self.SECTION__REMOTE_DIRS, self.logs_dirname)
		return self.get_host_remote() + ':' + path

	#
	#
	# RUTAS ABSOLUTAS
	#
	def get_dir_tmp(self):
		"""
		Carpeta que contiene archivos temporales
		"""
		return self.base_path + "tmp/"

	def get_dir_wikisquilter(self):
		"""
		Carpeta desde donde se ejecuta wikisquilter
		"""
		return self.base_path + "wikisquilter/"

	def get_dir_squidlogfiles(self):
		"""
		Carpeta que aloja cada log a procesarse por wikisquilter
		"""
		return self.get_dir_wikisquilter() + "squidlogfiles/"

	def get_dir_run_history(self):
		"""
		Carpeta donde van todos los historiales de ejecución
		"""
		return self.base_path + "run_history/"

	#
	#
	# PROCESSED LIST (lista de fechas ya procesadas)
	#
	def get_processed_list(self, list_name):
		"""
		Devuelve ruta + nombre de archivo para la lista de logs ya procesados
		según name sea:
			* squidlogs: procesados en la BD squidlogs -> [ test_ ]logs.squidlogs.processed
			* analysis: procesados en BD analysis -> [ test_ ]logs.analysis.processed
		"""
		if self.test_mode:
			return self.base_path + "test/test_logs." + list_name + ".processed"
		else:
			return self.base_path + "logs." + list_name + ".processed"

	def is_processed_for(self, date, list_name):
		"""
		Devuelve si la fecha dada ya está procesada en la lista dada
		"""
		# http://maengora.blogspot.com.es/2010/10/receta-python-buscar-una-cadena-de-un.html
		filename = self.get_processed_list(list_name)
		f = open(filename)
		lines = f.readlines()
		for l in lines:
			if l == self.get_log_date(date) + "\n":
				return True
		return False

	def is_full_processed(self, date):
		"""
		Devuelve si la fecha está completamente procesada (aparece en todas las listas)
		"""
		return self.is_processed_for(date, 'squidlogs') \
				and \
				self.is_processed_for(date, 'analysis')

	def year_not_exists_in_list(self, year, list_name):
		"""
		Comprueba en 'logs.processed' si no hay ningún log ya procesado para el año dado
		http://maengora.blogspot.com.es/2010/10/receta-python-buscar-una-cadena-de-un.html
		"""
		filename = self.get_processed_list(list_name)
		f = open(filename)
		lines = f.readlines()
		for l in lines:
			if l[:4] == year:
				return False
		return True

	def add_to_processed_list(self, date, list_name):
		"""
		Añade el log ya procesado a la lista del archivo logs.processed
		http://chuwiki.chuidiang.org/index.php?title=Leer_y_escribir_ficheros_en_python
		"""
		log_date = self.get_log_date(date)
		filename = self.get_processed_list(list_name)
		f = open(filename, "a")
		f.write(log_date + "\n")
		f.close()

	def remove_from_processed_list(self, date, list_name):
		"""
		Quita una fecha de la lista de procesadas
		http://stackoverflow.com/questions/5947833/deleting-a-line-from-a-file-in-python
		"""
		filename = self.get_processed_list(list_name)
		f = open(filename)
		output = []
		for line in f:
			d = self.get_log_date(date) + "\n"
			if line != d:
				output.append(line)
		f.close()
		f = open(filename, 'w')
		f.writelines(output)
		f.close()

	def is_processed_list_empty(self, filename):
		"""
		Indica si en logs.processed aún no hay ningún log procesado
		"""
		filename = self.get_processed_list(filename)
		f = open(filename)
		lines = f.readlines()
		for l in lines:
			regexp = re.compile('.*\d{8}.*')
			if regexp.search(l) is not None:
				return False
		return True

	def get_dumped_txt_filename(self):
		return self.get_dir_tmp() + "dumped.txt"

	# def is_processed_date_on_squidlogs(self, date):
	# 	query = "select date(f_date_time) " + \
	# 		"from Filtered where " + \
	# 		"date(f_date_time) = '" + date.strftime('%Y-%m-%d') + "' " + \
	# 		"limit 1;"

	# 	from helpers.mysql_helper import exec_mysql
	# 	exec_mysql(self.db_name_squidlogs, query=query, dumped=True)

	# 	# si el fichero dumped.txt no está vacío es que la fecha está procesada
	# 	if not is_empty(self.get_dumped_txt_filename()):
	# 		return True

	# 	return False
	# 	log_msg4("WARNING: No se populó la tabla. dump.txt vacío!!")
	# 	return

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

	#
	# OTRAS
	#
	def get_base_path(self):
		"""
		Devuelve la ruta absoluta hacia la carpeta raíz del proyecto
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


#
# Instanciamos un objeto vacío para luego asignarle una instancia de esta clase 'Config'
# al importarlo a otro módulo y así poder usarlo como objeto compartido entre los demás
# módulos
# http://docs.python.org/2/faq/programming.html#how-do-i-share-global-variables-across-modules
#
config = None


#
# Creamos el getter y setter para usar la misma variable 'config' en otros módulos
# http://www.daniweb.com/software-development/python/threads/73673/trouble-with-module-scope-variables#post335939
def getConfig():
	return config


def setConfig(test_mode):
	global config
	config = Config(test_mode)
