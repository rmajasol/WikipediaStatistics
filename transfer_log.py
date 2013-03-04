#!/usr/bin/python
# -*- coding: utf8 -*-

from helpers.exec_helper import *
from helpers.config_helper import *
from helpers.logging_helper import *
from helpers.date_helper import do_for_dates


if test:
	local = Config().get_dir_test_logs()
	remote = Config().get_dir_test_logs_remote()
else:
	local = Config().get_dir_logs()
	remote = Config().get_dir_logs_remote()


def transfer(date, local, remote):
	"""
	Descarga el log para la fecha dada
	"""
	log_name = Config().get_log_filename(date)

	log_msg2("Descargando " + log_name + " desde equipo remoto..")
	cmd = "scp " + remote + log_name + " " + local
	exec_proc(cmd)
	log_msg_ok2()


def run(dates):
	"""
	Descarga desde el equipo remoto el log para la fecha dada o bien
	para fechas entre una inicial (date) y final (date2) dadas
	"""
	do_for_dates(transfer ,dates)


