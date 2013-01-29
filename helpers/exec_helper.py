#!/usr/bin/python
# -*- coding: utf8 -*-

import subprocess


# ejecuta un comando via shell y deja el script esperando a su finalización
# para poder continuar
# http://stackoverflow.com/questions/1996518/retrieving-the-output-of-subprocess-call
def exec_proc(cmd):
	output, error = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
