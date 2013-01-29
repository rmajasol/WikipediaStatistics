import ConfigParser
# -*- coding: utf8 -*-


# creamos esta clase como helper para interactuar con el fichero de configuracion
class Config(object):

	config_file = "config.cfg"

	SECTION__DB_CONNECTION = "db_connection"
	SECTION__DIRS = "dirs"
	SECTION__FILES = "files"
	SECTION__HOSTS = "hosts"

	cfg = ConfigParser.ConfigParser()

	def __init__(self):
		# if config_file:
		# 	self.config_file = config_file[0]
		# leemos del archivo de configuracion 'config.cfg'
		self.cfg.read([self.config_file])

	# lee el nombre de un parametro dentro de una seccion en el archivo de configuracion
	def read(self, section, name):
		return self.cfg.get(section, name)

	# modifica un parametro dentro de una seccion en el archivo de configuracion
	def write(self, section, name, value):
		self.cfg.set(section, name, value)
		f = open(self.config_file, "w")
		self.cfg.write(f)
		f.close()

	# SECTION__DB_CONNECTION
	# obtiene el nombre de usuario para conectar a la BD
	def get_db_user(self):
		return self.cfg.get(self.SECTION__DB_CONNECTION, "db_user")

	def get_db_password(self):
		return self.cfg.get(self.SECTION__DB_CONNECTION, "db_pass")

	def get_db_name(self):
		return self.cfg.get(self.SECTION__DB_CONNECTION, "db_name")

	def get_db_host(self):
		return self.cfg.get(self.SECTION__DB_CONNECTION, "db_host")

	def get_db_port(self):
		return self.cfg.get(self.SECTION__DB_CONNECTION, "db_port")

	# SECTION__DIRS
	# ruta hacia cada directorio
	def get_dir_logs(self):
		return self.cfg.get(self.SECTION__DIRS, "logs")

	def get_dir_logs_remote(self):
		return self.cfg.get(self.SECTION__DIRS, "logs_remote")

	def get_dir_test_logs(self):
		return self.cfg.get(self.SECTION__DIRS, "test_logs")

	def get_dir_test_logs_remote(self):
		return self.cfg.get(self.SECTION__DIRS, "test_logs_remote")

	def get_dir_tmp(self):
		return self.cfg.get(self.SECTION__DIRS, "tmp")

	def get_dir_squidlogfiles(self):
		return self.cfg.get(self.SECTION__DIRS, "squidlogfiles")

	def get_dir_run_history(self):
		return self.cfg.get(self.SECTION__DIRS, "run_history")

	# SECTION__FILES
	# nombres de archivo
	def get_filename_processed_list(self):
		return self.cfg.get(self.SECTION__FILES, "processed_list")

	# SECTION__HOSTS
	# direcciones IP / nombres de dominio
	def get_host_remote(self):
		return self.cfg.get(self.SECTION__HOSTS, "remote")


# devuelve el nombre del log a partir de una fecha dada
def get_log_filename(date):
	return "log-" + date.strftime('%Y%m%d') + ".gz"


# devuelve el mes dado el nombre de archivo del log
def get_log_month(log_file):
	return log_file[8:10]


# devuelve sólo la fecha del log
def get_log_date(date):
	return date.strftime('%Y%m%d')
