#!/usr/bin/python
# -*- coding: utf8 -*-

# prueba para ejecutar wikisquilter sobre el log-20120615.gz

# ejecutamos wikisquilter sobre el log-20120615.gz

import os
os.chdir("..")

from datetime import date
date = date.today()
date = date.replace(year=2012, month=06, day=15)

# añadimos al PYTHONPATH /home/ramon/Dropbox/tfg/proyecto para así poder importar
# el módulo run_wikisquilter, situado 2 niveles más arriba en el árbol de directorios
import sys
sys.path.append(os.getcwd())
from run_wikisquilter import run
run(date, test=True)
