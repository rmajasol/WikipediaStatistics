#!/usr/bin/python
# -*- coding: utf8 -*-

import os
import random
import gzip
from datetime import date, timedelta
from config_helper import Config

# numero de linea del log descomprimido en texto plano
current_line = 0


# se crea archivo ~/test_logs/log-[año][mes][dia].gz con 100000 líneas 
# escogidas a partir de ~/test_logs/log_lines con la fecha modificada a la indicada
def crear_log(date):
	global current_line
	print "linea actual: " + str(current_line)
	test_logs_dir = Config().get_test_logs_dir()

	# leemos el archivo con todas las líneas en texto plano
	src_file = test_logs_dir + "log_lines"
	lines = open(src_file, 'r')

	# Get the total file size
	# file_size = os.stat(src_file)[6]

	# http://www.regexprn.com/2008/11/read-random-line-in-large-file-in.html
	#
	# Seek to a place in the file which is a random distance away
	# Mod by file size so that it wraps around to the beginning
	# Para que el último bloque posible a escoger no tenga pocas líneas
	# acotamos el límite a la longitud total - (200Bytes/linea * 100000 lineas)
	# lines.seek(
	# 	(lines.tell() + random.randint(0, file_size - 1))
	# 	%
	# 	(file_size - (200 * 100000))
	# )

	lines_to_write = 100000
	for i in range(current_line, lines_to_write):
		lines.readline()

	dest_file = test_logs_dir + "log-" + date.strftime('%Y%m%d')
	dest = open(dest_file, 'w')

	for i in range(0, lines_to_write):
		#dont use the first readline since it may fall in the middle of a line
		lines.readline()
		#this will return the next (complete) line from the file
		line = lines.readline()

		#cambiamos la fecha en cada linea por la actual
		line = line.replace("Jun 14 ", date.strftime('%b %d '))
		line = line.replace(" 2012-06-14", date.strftime(' %Y-%m-%d'))

		# escribimos la linea en el destino
		dest.write(line)

	dest.close()

	# comprimimos el fichero dest_file, donde se escribieron todas las líneas anteriores
	# http://stackoverflow.com/questions/8156707/gzip-a-file-in-python
	f_in = open(dest_file, 'rb')
	f_out = gzip.open(dest_file + ".gz", 'wb')
	f_out.writelines(f_in)
	f_out.close()
	f_in.close()

	# borramos el archivo dest de texto plano, quedándonos sólo con el .gz
	os.system("rm " + dest_file)

	# incrementamos para así indicar la próxima línea a leer dentro de log_lines
	current_line += 100000


d = date.today()
d = d.replace(year=2013, month=1, day=1)
d2 = d.replace(year=2013, month=2, day=1)
d2 -= timedelta(1)

# mientras que la fecha d sea menor a la final (d2)..
while d < d2:
	crear_log(d)
	d += timedelta(1)
