#!/usr/bin/python
# -*- coding: utf8 -*-

# Nos ayudará para crear un parseador de argumentos

from argparse import ArgumentParser


def init_argparser(**kwargs):
	"""
	Nos devuelve el objeto 'parser' con todos los argumentos parseados

	**kwargs contiene hashes:
		* clave = tipo de argumento, que puede ser 'test' o 'date'
		* valor = descripción de lo que hace el argumento

	Por ejemplo:
		init_argparser(
			test="Sube sólo logs de prueba",
			date="Sube logs para la/s fecha/s dada/s " + \
				"en el equipo remoto"
		)
	"""
	test = None
	date = None
	manual = None
	database = None

	for key in kwargs:
		if key == 'test':
			test = kwargs[key]
		elif key == 'date':
			date = kwargs[key]
		elif key == 'manual':
			manual = kwargs[key]
		elif key == 'database':
			database = kwargs[key]

	parser = ArgumentParser()

	if test:
		parser.add_argument('-t', '--test',
			action="store_true",
			dest="test",
			default=False,
			help=test)

	if date:
		parser.add_argument(
			nargs="+",
			metavar=('INITIAL_DATE', 'FINAL_DATE'),
			dest="date",
			default=False,
			help=date)

	if manual:
		parser.add_argument('-m', '--manual',
			nargs='+',
			# http://argparse.googlecode.com/svn/trunk/doc/add_argument.html#metavar
			metavar=('INITIAL_DATE', 'FINAL_DATE'),
			dest="manual",
			default=False,
			help=manual)

	if database:
		parser.add_argument('-d', '--database',
			required=True,
			nargs=1,
			# http://argparse.googlecode.com/svn/trunk/doc/add_argument.html#metavar
			metavar=('DATABASE_NAME'),
			dest="database",
			default=False,
			help=database)

	return parser.parse_args()
