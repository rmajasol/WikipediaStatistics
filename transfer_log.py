#!/usr/bin/python
# -*- coding: utf8 -*-

from helpers.exec_helper import *
from helpers.config_helper import *
from helpers.logging_helper import *


# transfiere de remoto a local un log para una fecha dada
def run(date, test):
	if test:
		local = Config().get_dir_test_logs()
		remote = Config().get_dir_test_logs_remote()
	else:
		local = Config().get_dir_logs()
		remote = Config().get_dir_logs_remote()

	log_name = Config().get_log_filename(date)

	log_msg2("Descargando " + log_name + " desde equipo remoto..")
	cmd = "scp " + remote + log_name + " " + local
	exec_proc(cmd)
	log_msg_ok2()
