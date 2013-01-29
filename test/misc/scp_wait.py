#!/usr/bin/python
# -*- coding: utf8 -*-

import subprocess


import os
os.chdir("../..")
# añadimos al PYTHONPATH /home/ramon/Dropbox/tfg/proyecto para así poder importar
# el módulo que queramos probar, situado 1 nivel más arriba en el árbol de directorios
import sys
sys.path.append(os.getcwd())

from config_helper import Config


# transfiere desde una maquina a otra y no pausa el script hasta que termine la transferencia
ORIGIN = Config().read("hosts", "origin")
DESTINY = Config().read("hosts", "destiny")

log_name = "log-20090601.gz"
cmd = "scp " + ORIGIN + log_name + " " + DESTINY

print cmd

print "iniciando transferencia.."

output, error = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

print "transferido!"
