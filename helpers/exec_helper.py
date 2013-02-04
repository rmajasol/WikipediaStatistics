#!/usr/bin/python
# -*- coding: utf8 -*-

import subprocess
import sys
from logging_helper import log_error_msg


# import datetime


# ejecuta un comando via shell y deja el script esperando a su finalización
# para poder continuar
# http://stackoverflow.com/questions/1996518/retrieving-the-output-of-subprocess-call
# http://docs.python.org/2/library/subprocess.html#popen-objects
def exec_proc(cmd):

	# start = datetime.datetime.now()

	output, error = subprocess.Popen(cmd, shell=True,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE).communicate()

	# si hay error mostramos su mensaje y salimos del script
	if error:
		log_error_msg(error)
		# http://stackoverflow.com/questions/1187970/how-to-exit-from-python-without-traceback
		# http://docs.python.org/2/library/exceptions.html#exceptions.SystemExit
		sys.exit(0)

	# return datetime.datetime.now() - start
