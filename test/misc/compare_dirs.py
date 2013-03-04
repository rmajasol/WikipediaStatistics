# -*- coding: utf8 -*-

import os
from argparse import ArgumentParser


def is_absolute(path):
	"""
	Indica si la ruta que introducimos es relativa o no
	"""
	return True if path[0] == '/' else False


def get_file_list(dir):
	"""
	Devuelve recursivamente la lista de archivos en 'dir',
	expresados con su ruta relativa desde la raíz de 'dir'
	"""
	os.chdir(dir)
	dir = '.'

	filelist = []

	for dirpath, dnames, fnames in os.walk(dir):
		# recorre archivos de forma recursiva dentro del directorio
		for f in fnames:
			# f_rel es archivo de 'folder' expresado en ruta relativa, e.g.:
			#
			# ./wait_process.py
			# ./test99/dos.txt
			# ./test99/uno.txt
			# ./test99/carpuno/cuno.txt

			f_rel = dirpath + '/' + f
			filelist.append(f_rel)

	os.chdir(CURRENT_DIR)

	return filelist


def rm_file_if_exists(file):
	"""
	Se elimina un archivo si existe
	"""
	try:
		with open(file):
			os.remove(file)
	except IOError:
		pass


def write_filelist_to_file(filelist, filename):
	"""
	Escribimos en el archivo 'filename' la lista de archivos 'filelist' dada
	"""
	filename = DIR1_ABS + '/' + filename
	f = open(filename, "a")
	for file in filelist:
		f.write(file[2:] + '\n')
	f.close()


def init_argparse():
	parser = ArgumentParser(
		description='Get filelist from two directories recursively and ' + \
			'checks if each file from DIR1 exists in DIR2. ' + \
			'If there puts its relative path in DIR1/Existe.txt, ' + \
			'and if not then puts its path in DIR1/NoExiste.txt')

	parser.add_argument('DIR1', help='Absolute or relative path to DIR1')
	parser.add_argument('DIR2', help='Absolute or relative path to DIR2')

	return parser.parse_args()


##########
#
# MAIN
#
##########

if __name__ == "__main__":

	args = init_argparse()

	# DIRECTORIOS DIR1 Y DIR2 A COMPARAR
	#
	# Cada directorio podemos expresarlo usando ruta absoluta o relativa.
	# Por ejemplo, si el directorio DIR1 es el mismo
	# desde donde ejecutamos el script, entonces es suficiente con indicar la ruta relativa '.'
	DIR1 = args.DIR1
	DIR2 = args.DIR2

	# Directorio desde el que ejecutamos el script
	CURRENT_DIR = os.path.abspath('.')

	# si los archivos 'Existe.txt' y 'NoExiste.txt' existen los eliminamos
	DIR1_ABS = DIR1 if is_absolute(DIR1) else os.path.abspath('./' + DIR1)
	DIR2_ABS = DIR2 if is_absolute(DIR2) else os.path.abspath('./' + DIR2)
	rm_file_if_exists(DIR1_ABS + '/Existe.txt')
	rm_file_if_exists(DIR1_ABS + '/NoExiste.txt')

	# Creamos las listas de archivos para cada carpeta
	dir1_rel_filelist = get_file_list(DIR1)
	dir2_rel_filelist = get_file_list(DIR2)

	# lista ordenada de archivos comunes entre DIR1 y DIR2
	files_that_exist = sorted(list(set(dir1_rel_filelist).intersection(dir2_rel_filelist)))
	# lista ordenada de archivos que están en DIR1 y no en DIR2
	files_that_not_exist = sorted(list(set(dir1_rel_filelist) - set(dir2_rel_filelist)))

	# escribimos los archivos que existen y no existen en sus respectivos .txt
	write_filelist_to_file(files_that_exist, 'Existe.txt')
	write_filelist_to_file(files_that_not_exist, 'NoExiste.txt')
