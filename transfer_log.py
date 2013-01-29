#!/usr/bin/python
# -*- coding: utf8 -*-

from helpers.exec_helper import *
from helpers.config_helper import *
from helpers.logging_helper import *


# transfiere desde una maquina a otra un log de una fecha dada
def run(date, test):
	origin = ""
	remote = Config().get_host_remote()
	if test:
		origin += Config().get_dir_test_logs()
		remote += Config().get_dir_test_logs_remote()
	else:
		origin += Config().get_dir_logs()
		remote += Config().get_dir_logs_remote()

	log_name = Config().get_log_filename(date)

	cmd = "scp " + origin + log_name + " " + remote

	log_msg("Descargando " + log_name + " desde equipo remoto..")

	exec_proc(cmd)

	log_msg("Log " + log_name + " descargado OK")
