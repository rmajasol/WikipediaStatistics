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
	test = ""
	date = ""

	for key in kwargs:
		if key == 'test':
			test = kwargs[key]
			print test
		elif key == 'date':
			date = kwargs[key]

	parser = ArgumentParser()

	if test:
		# print test + "aaaaaa"
		parser.add_argument('-t', '--test',
			action="store_true",
			dest="test",
			default=False,
			help=test)

	if date:
		# print date
		parser.add_argument(
			nargs="+",
			metavar=('INITIAL_DATE', 'FINAL_DATE'),
			dest="date",
			default=False,
			help=date)

	return parser.parse_args()
