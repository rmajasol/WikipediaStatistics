import ConfigParser


# creamos esta clase como helper para interactuar con el fichero de configuracion
class Config(object):

	CONFIG_FILE = "config.cfg"

	SECTION__DB_CONNECTION = "db_connection"

	cfg = ConfigParser.ConfigParser()

	def __init__(self):
		# leemos del archivo de configuracion 'config.cfg'
		self.cfg.read([self.CONFIG_FILE])

	# lee el nombre de un parametro dentro de una seccion en el archivo de configuracion
	def read(self, section, name):
		return self.cfg.get(section, name)

	# modifica un parametro dentro de una seccion en el archivo de configuracion
	def write(self, section, name, value):
		self.cfg.set(section, name, value)
		f = open(self.CONFIG_FILE, "w")
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

	def get_logs_dir(self):
		return self.cfg.get("other", "logs_dir")
