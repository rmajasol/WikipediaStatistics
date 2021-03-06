#!/usr/bin/python
# -*- coding: utf8 -*-

import subprocess
import sys
from logging_helper import log_error_msg


def halt(error_msg):
	"""
	Detenemos la ejecución del script por completo, mostrando un
	mensaje de error tanto en consola como en el historial de ejecución
	"""
	print "ERROR: " + str(error_msg)
	log_error_msg(error_msg)
	# http://stackoverflow.com/questions/1187970/how-to-exit-from-python-without-traceback
	# http://docs.python.org/2/library/exceptions.html#exceptions.SystemExit
	sys.exit(0)


def exec_proc(cmd):
	"""
	Ejecuta un proceso invocado por el comando 'cmd' del mismo modo
	que si se hiciese vía shell y deja el script python esperando
	a su finalización para poder continuar.

	Si hubiera error escribimos el mensaje en el historial de ejecución
	y detenemos por completo el script
	http://stackoverflow.com/questions/1996518/retrieving-the-output-of-subprocess-call
	http://docs.python.org/2/library/subprocess.html#popen-objects
	"""

	# start = datetime.datetime.now()

	output, error = subprocess.Popen(cmd, shell=True,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE).communicate()

	# si hay error mostramos su mensaje y salimos del script
	if error:
		halt(error)

	# return datetime.datetime.now() - start
