#!/usr/bin/python

import os
import logging
from config_helper import Config


# transfiere desde una maquina a otra un log de una fecha dada
def run(date):
	ORIGIN = Config().read("hosts", "origin")
	DESTINY = Config().read("hosts", "origin")

	log_name = "log-" + date.strftime('%Y%m%d') + ".gz"
	os.system("scp" + " " + ORIGIN + log_name + " " + DESTINY)

	logging.info("Obteniendo " + log_name + " desde equipo remoto..")
