#!/usr/bin/python
# -*- coding: utf8 -*-


# script principal que realiza todo el proceso de popular la BD
# analysis a partir de los logs
#
#
# Cada día 1, 10 y 20 de cada mes se realizan las siguiente serie de tareas:
#
# 1. Tansferir logs de días anteriores -> transfer_log.py
# 2. Ejecutar wikisquilter sobre ellos -> run_wikisquilter.py
# 3. Popular BD de analysis -> populate_analysis.py
# 4. Vaciar la BD squidlogs -> clear_squidlogs.py


from datetime import date, timedelta

import transfer_log
import run_wikisquilter


# ejecuta toda la tarea para el dia dado
def run(date):
	print "Procesando dia: " + date.strftime('%Y%m%d')
	# transferimos
	#transfer_log.run(date)

	# ejecutamos wsq
	run_wikisquilter.run(date)

	# populamos analysis con resultados
	import populate_analysis

	# vaciamos BD squidlogs
	import clear_squidlogs


date = date.today()
today = date.day
if today == 1:
	date -= timedelta(1)
	top_day = date.day
	for i in range(20, top_day + 1):
		date = date.replace(day=i)  # http://docs.python.org/2/library/datetime.html
		run(date)
elif today == 19:
	date -= timedelta(9)
	for i in range(0, 9):
		run(date)
		date += timedelta(1)
elif today == 20:
	date -= timedelta(10)
	for i in range(0, 10):
		run(date)
		date += timedelta(1)


#print str(now.month)+"/"+str(now.day)+"/"+str(now.year) # 10/14/2012
#print str(now.hour)+":"+str(now.minute)+":"+str(now.second) # 20:19:38

# crea un .txt con la hora y lo mueve al 8
#filename = "~/"+str(now.hour)+str(now.minute)+str(now.second)+".txt"
#os.system("touch "+filename)
#os.system("scp "+filename+" rmaja@193.146.26.8:")




# from datetime import datetime
# now = datetime.now()
# print now			# 2012-10-14 20:19:38.804481
# print now.year		# 2012
# print now.month		# 10
# print now.day		# 14
# print str(now.month)+"/"+str(now.day)+"/"+str(now.year) # 10/14/2012
# print str(now.hour)+":"+str(now.minute)+":"+str(now.second) # 20:19:38

# crea un .txt con la hora y lo mueve al 8
# filename = "~/"+str(now.hour)+str(now.minute)+str(now.second)+".txt"
# os.system("touch "+filename)
# os.system("scp "+filename+" rmaja@193.146.26.8:")

# Para calcular la de ayer, restamos un dia
#ayer = hoy + datetime.timedelta(days=-1)
