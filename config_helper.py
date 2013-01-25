import ConfigParser


# creamos esta clase como helper para interactuar con el fichero de configuracion
class Config(object):

	config_file = "config.cfg"

	SECTION__DB_CONNECTION = "db_connection"

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

	# nos devuelve la ruta relativa hacia los archivos temporales
	def get_tmp_dir(self):
		return self.cfg.get("other", "tmp_dir")

	def get_test_logs_dir(self):
		return self.cfg.get("other", "test_logs_dir")

	def get_squidlogsfiles_dir(self):
		return self.cfg.get("other", "squidlogfiles_dir")

	def get_logs_dir(self):
		return self.cfg.get("other", "logs_dir")

	def get_run_logs_dir(self):
		return self.cfg.get("other", "run_logs_dir")
