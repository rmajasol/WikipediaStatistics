#!/usr/bin/python
# -*- coding: utf8 -*-

# prueba para popular la BD analysis

import os
os.chdir("..")

# añadimos al PYTHONPATH /home/ramon/Dropbox/tfg/proyecto para así poder importar
# el módulo que queramos probar, situado 1 nivel más arriba en el árbol de directorios
import sys
sys.path.append(os.getcwd())

from config_helper import Config
import logging
from datetime import date


RUN_LOGS_DIR = Config().get_run_logs_dir()
date = date.today()
logging.basicConfig(filename=RUN_LOGS_DIR + "run-" + date.strftime('%Y%m%d') + ".test.log",
	format='%(asctime)s - %(message)s',
	level=logging.INFO)
