#!/usr/bin/python
# -*- coding: utf8 -*-

import add_to_pythonpath
from log_generator2 import crear_log
from helpers.config_helper import Config
from helpers.exec_helper import exec_proc
from helpers.date_helper import *
from helpers.parser_helper import init_argparser


# transfiere a ~/logs del remoto el log generado
def transfer_to_remote(date):
	crear_log(date)

	local = Config().get_dir_test_logs()
	remote = Config().get_dir_test_logs_remote()
	log_name = Config().get_log_filename(date)

	cmd = "scp " + local + log_name + " " + remote

	print "Subiendo " + log_name + " a equipo remoto.."
	exec_proc(cmd)
	print "Log " + log_name + " subido\n"


args = init_argparser(
	date="Sube logs para la/s fecha/s dada/s en el equipo remoto")

do_for_dates(transfer_to_remote, args)


# d = get_now_to_zero()
# d = d.replace(year=2012, month=1, day=30)
# d2 = d.replace(year=2013, month=2, day=1)

# # mientras que la fecha d sea menor o igual a la final (d2)..
# while d <= d2:
# 	crear_log(d)
# 	transfer_to_remote(d)
# 	d += timedelta(1)
