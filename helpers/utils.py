# -*- coding: utf8 -*-

#
# funciones de utilidad
#
import os


def is_absolute(path):
	"""
	Indica si la ruta que introducimos es relativa o no
	"""
	return True if path[0] == '/' else False


def is_empty(filename):
	"""
	Mira si un fichero esta vacío
	"""
	f = open(filename)
	return f.readline() == ""


def file_exists(file):
	"""
	Indica si existe el archivo indicado con ruta absoluta
	"""
	return os.path.isfile(file)


def dir_exists(dir):
	"""
	Indica si existe el directorio indicado con ruta absoluta
	"""
	return os.path.exists(dir)
