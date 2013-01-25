#!/usr/bin/python
# -*- coding: utf8 -*-

# prueba para mover un archivo de un directorio a otro

from shutil import copy
import os

copy("/home/ramon/test_logs/log-20130101.gz",
	"/home/ramon/Dropbox/tfg/proyecto/wikisquilter/squidlogfiles")

while True:
	n = int(input("Pulsa 1 para eliminar el archivo"))
	if n == 1:
		os.remove("/home/ramon/Dropbox/tfg/proyecto/wikisquilter/squidlogfiles/log-20130101.gz")
		break
