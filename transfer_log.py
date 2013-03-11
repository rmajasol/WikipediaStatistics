#!/usr/bin/python
# -*- coding: utf8 -*-

from helpers.exec_helper import *
from helpers.config_helper import getConfig
from helpers.logging_helper import *
from helpers.utils import file_exists


def run(date):
	"""
	Transfiere de remoto a local un log para una fecha dada.
	"""
	log_name = getConfig().get_log_filename(date)
	dir_local = getConfig().get_dir_local_logs()
	dir_remote = getConfig().get_dir_remote_logs()

	#
	# Si no aparece como descargado o aparece como descargado pero no existe..
	downloaded = getConfig().is_processed_for(date, 'transfer')
	if not downloaded or (downloaded and not file_exists(dir_local + log_name)):
		log_msg2("Descargando " + log_name + " desde equipo remoto..")

		# si aparece como descargado lo quitamos primero de la lista..
		if downloaded:
			getConfig().remove_from_processed_list(date, 'transfer')

		#
		# Transferimos..
		cmd = "scp " + dir_remote + log_name + " " + dir_local
		exec_proc(cmd)

		# De esta forma nos aseguramos que el log fue descargado por completo:
		getConfig().add_to_processed_list(date, 'transfer')

		log_msg_ok2()
	else:
		log_msg2(log_name + " no es necesario descargar de nuevo.", state='processed')
