import ConfigParser


# creamos esta clase como helper para interactuar con el fichero de configuracion
class Config(object):

	CONFIG_FILE = "../config.cfg"
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
