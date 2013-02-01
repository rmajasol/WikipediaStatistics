#!/usr/bin/python
# -*- coding: utf8 -*-
import logging
from datetime import date
from config_helper import Config

ENDING = ".."
OK = "..OK!"

# separadores para leer mejor el log con indentación
SEP_2_INIT = "\t-> "
SEP_2_END = "\t== "
SEP_3 = "\t" * 2
SEP_4 = "\t" * 3


def init_logger(module, test):
	"""
	Inicializa el archivo donde escribiremos el historial de ejecución
	"""
	d = date.today()
	filename = Config().get_dir_run_history() + module + "-" + \
		d.strftime('%Y%m%d') + \
		".test.log" if test else ".log"

	logging.basicConfig(filename=filename,
		format='%(asctime)s - %(message)s',
		# http://docs.python.org/2/howto/logging.html#displaying-the-date-time-in-messages
		datefmt='%H:%M:%S',
		level=logging.INFO)


# mensajes de iniciación de algún procedimiento..
def log_msg(msg):
	logging.info(msg + ENDING)


def log_msg2(msg):
	logging.info(SEP_2_INIT + msg + ENDING)


def log_msg3(msg):
	logging.info(SEP_3 + msg + ENDING)


def log_msg4(msg):
	logging.info(SEP_4 + msg + ENDING)


# ..mensajes de confirmación
def log_msg_ok():
	logging.info(OK)


def log_msg_ok2():
	logging.info(SEP_2_END + OK)


def log_msg_ok3():
	logging.info(SEP_3 + OK)


def log_msg_ok4():
	logging.info(SEP_4 + OK)
