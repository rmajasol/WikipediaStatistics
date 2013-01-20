#!/usr/bin/python

import os
from config_helper import Config


# se crea archivo ~/transferred_logs/log-[año][mes][dia].gz con el texto
# "Log generado para el dia [año][mes][dia]"
def crear_log(anio, mes, dia):
	transferred_logs_dir = Config().get_logs_dir()
	filename = transferred_logs_dir + "log-" + anio + mes + dia + ".gz"
	os.system("touch " + filename)
	texto = "Log generado para el dia " + anio + mes + dia
	os.system("echo '" + texto + "' > " + filename)


fInicio = 2009
fFin = 2012

for i in range(fInicio, fFin + 1):
	for j in range(1, 13):
		for k in range(1, 32):
			mes = str(j)
			if j < 10:
				mes = "0" + mes
			dia = str(k)
			if k < 10:
				dia = "0" + dia
			crear_log(str(i), mes, dia)
