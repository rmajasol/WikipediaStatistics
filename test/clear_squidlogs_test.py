#!/usr/bin/python
# -*- coding: utf8 -*-

# prueba para script clear_squidlogs

import os

print "1. " + os.getcwd()
os.chdir("..")

print "2. " + os.getcwd()
# añadimos al PYTHONPATH /home/ramon/Dropbox/tfg/proyecto para así poder importar
# el módulo clear_squidlogs, situado 1 nivel más arriba en el árbol de directorios
import sys
sys.path.append(os.getcwd())
from clear_squidlogs import run
run()
