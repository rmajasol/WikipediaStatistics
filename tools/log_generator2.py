#!/usr/bin/python
# -*- coding: utf8 -*-

import os
import gzip
from datetime import date, timedelta
import add_to_pythonpath
from helpers.config_helper import Config


LINES_TO_WRITE = 100000

# numero de bloque de 100000 líneas del log descomprimido en texto plano
block_number = 0


# se crea archivo ~/test_logs/log-[año][mes][dia].gz con bloque de 100000 líneas
# escogidas a partir de ~/test_logs/log_lines con la fecha modificada a la indicada
def crear_log(date):
	"""
	Crea un log de prueba -> test_logs/log-[año][mes][dia].gz a partir de un bloque
	de 100000 líneas de un log real -> test_logs/log_lines, modificando cada línea
	a la fecha dada
	"""
	global block_number
	print "bloque " + str(block_number)
	test_logs_dir = Config().get_dir_test_logs()

	# leemos el archivo con todas las líneas en texto plano
	src_file = test_logs_dir + "log_lines"
	lines = open(src_file, 'r')

	# saltamos de línea en el archivo hasta llegar al siguiente bloque
	for i in range(0, LINES_TO_WRITE * block_number):
		lines.readline()

	# abrimos el archivo destino donde escribiremos el bloque de líneas escogido
	dest_file = test_logs_dir + "log-" + date.strftime('%Y%m%d')
	dest = open(dest_file, 'w')

	# escribimos cada línea en el archivo destino con la fecha cambiada
	for i in range(0, LINES_TO_WRITE):
		line = lines.readline()

		# cambiamos la fecha de cada linea leída en log_lines por la actual
		line = line.replace("Jun 14 ", date.strftime('%b %d '))
		line = line.replace(" 2012-06-14", date.strftime(' %Y-%m-%d'))

		# escribimos la linea cambiada en el archivo destino
		dest.write(line)

	dest.close()

	# comprimimos el fichero destino (dest_file) donde se escribieron todas las líneas anteriores
	# http://stackoverflow.com/questions/8156707/gzip-a-file-in-python
	f_in = open(dest_file, 'rb')
	f_out = gzip.open(dest_file + ".gz", 'wb')
	f_out.writelines(f_in)
	f_out.close()
	f_in.close()

	# borramos el archivo dest de texto plano, quedándonos sólo con el .gz
	os.system("rm " + dest_file)

	# incrementamos el número de bloque para saber la siguiente línea a obtener
	# la próxima vez que volvamos a leer el archivo log_lines
	block_number += 1


if __name__ == "__main__":

	d = date.today()
	d = d.replace(year=2012, month=4, day=1)
	d2 = d.replace(year=2012, month=8, day=1)

	# mientras que la fecha d sea menor a la final (d2)..
	while d < d2:
		crear_log(d)
		d += timedelta(1)
