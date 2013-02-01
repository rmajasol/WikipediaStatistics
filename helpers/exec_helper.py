#!/usr/bin/python
# -*- coding: utf8 -*-

import subprocess
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

	# return datetime.datetime.now() - start
