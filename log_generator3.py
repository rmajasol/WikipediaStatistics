#!/usr/bin/python
# -*- coding: utf8 -*-

from datetime import date, timedelta
from log_generator2 import crear_log
from helpers.config_helper import Config
from helpers.exec_helper import exec_proc


# transfiere a ~/logs del remoto el log generado
def transfer_to_remote(date):
	ORIGIN = Config().get_test_logs_dir()
	DESTINY = Config().read("hosts", "skynet_test")

	log_name = "log-" + date.strftime('%Y%m%d') + ".gz"

	cmd = "scp " + ORIGIN + log_name + " " + DESTINY

	print "Subiendo " + log_name + " a equipo remoto.."

	exec_proc(cmd)

	print "Log " + log_name + " subido\n"


d = date.today()
d = d.replace(year=2013, month=1, day=1)
d2 = d.replace(year=2013, month=3, day=1)

# mientras que la fecha d sea menor a la final (d2)..
while d < d2:
	crear_log(d)
	transfer_to_remote(d)
	d += timedelta(1)
