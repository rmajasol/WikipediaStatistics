#!/usr/bin/python
# -*- coding: utf8 -*-
import logging

ENDING = ".."
OK = "..OK!"

# separadores para leer mejor el log con indentación
SEP_2 = "\t-> "
SEP_3 = "\t" * 2
SEP_4 = "\t" * 4


# mensajes de iniciación de algún procedimiento..
def log_msg(msg):
	logging.info(msg + ENDING)


def log_msg2(msg):
	logging.info(SEP_2 + msg + ENDING)


def log_msg3(msg):
	logging.info(SEP_3 + msg + ENDING)


def log_msg4(msg):
	logging.info(SEP_4 + msg + ENDING)


# ..mensajes de confirmación
def log_msg_ok():
	logging.info(OK)


def log_msg_ok2():
	logging.info(SEP_2 + OK)


def log_msg_ok3():
	logging.info(SEP_3 + OK)


def log_msg_ok4():
	logging.info(SEP_4 + OK)
