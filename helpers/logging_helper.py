# -*- coding: utf8 -*-
import logging
from datetime import datetime
from config_helper import Config

ENDING = ".."
OK = "..OK!"

# separadores para leer mejor el log con distintos niveles de indentación
SEP_2_INIT = "\t-> "
SEP_2_END = "\t== "
SEP_3 = "\t" * 2
SEP_4 = "\t" * 3


def init_logger(module, test):
	"""
	Inicializa el logger para escribir en un archivo el historial completo
	de ejecución del script
	"""
	d = datetime.now()

	filename = Config().get_dir_run_history()
	if test:
		filename += "test."
	filename += module + "-" + d.strftime('%Y%m%d_%H%M') + ".log"

	logging.basicConfig(
		filename=filename,
		format='%(asctime)s - %(message)s',
		# http://docs.python.org/2/howto/logging.html#displaying-the-date-time-in-messages
		datefmt='%H:%M:%S',
		level=logging.INFO,
		filemode='w'
	)


# mensajes de iniciación de algún procedimiento. Distintos niveles de indentación
def log_msg(msg):
	logging.info(msg + ENDING)


def log_msg2(msg):
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
	logging.error(error_msg)
