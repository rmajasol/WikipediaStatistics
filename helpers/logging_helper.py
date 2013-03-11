# -*- coding: utf8 -*-
import logging
from datetime import datetime

# importamos el método 'getConfig' para poder obtener el obtejo 'config' compartido
# entre los módulos, definido previamente en el módulo principal con 'setConfig()..
from helpers.config_helper import getConfig

# Hacer esto no funciona:
# 		from config_helper import config
#		print config
#
# Esto tampoco funciona (config = None):
# 		config = config_helper.config

# Lo que funciona es esto (obtiene el valor actual de config dentro de config_helper)
# 		print config_helper.config
# Pero se considera más legible la solución anterior


ENDING = ".."
OK = "..OK!"

# separadores para leer mejor el log con distintos niveles de indentación
SEP_2_INIT = "\t\t-> "
SEP_2_END = "\t\t== "
SEP_2_PROCESSED = "\t\t#### "
SEP_3 = "\t" * 4
SEP_4 = "\t" * 5


def init_logger(module):
	"""
	Inicializa el logger para escribir en un archivo el historial completo
	de ejecución del script
	"""
	d = datetime.now()

	filename = getConfig().get_dir_run_history()
	if getConfig().test_mode:
		filename += "test."
	filename += module + "-" + d.strftime('%Y%m%d_%H%M') + ".log"

	logging.basicConfig(
		filename=filename,
		format='%(asctime)s - %(message)s',
		# http://docs.python.org/2/howto/logging.html#displaying-the-date-time-in-messages
		# http://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
		datefmt='%b,%d %H:%M',
		level=logging.INFO,
		filemode='w'
	)

	print "Creado historial de ejecución en " + filename


# mensajes de iniciación de algún procedimiento. Distintos niveles de indentación
def log_msg(msg):
	logging.info(msg)


def log_msg2(msg, state='not_processed'):
	"""
	Para indicar el comienzo de una tarea para un día dado:
		* Transferencia del log
		* Squidlogs
		* Analysis
	"""
	if state == 'processed':
		logging.info(SEP_2_PROCESSED + msg)
	else:
		logging.info(SEP_2_INIT + msg + ENDING)


def log_msg3(msg):
	logging.info(SEP_3 + msg + ENDING)


def log_msg4(msg):
	logging.info(SEP_4 + msg + ENDING)


# Mensajes de confirmación para cada nivel
def log_msg_ok():
	logging.info(OK)


def log_msg_ok2():
	logging.info(SEP_2_END + OK)


def log_msg_ok3():
	logging.info(SEP_3 + OK)


def log_msg_ok4():
	logging.info(SEP_4 + OK)


# mensaje de error
def log_error_msg(error_msg):
	logging.error("ERROR: " + str(error_msg))
