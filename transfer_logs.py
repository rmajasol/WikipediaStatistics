#!/usr/bin/python

import os
import ConfigParser

# Leemos del archivo de configuracion 'config.cfg'
cfg = ConfigParser.ConfigParser()
cfg.read(["config.cfg"])
ORIGIN = cfg.get("hosts", "origin")
DESTINY = cfg.get("hosts", "destiny")


def get_log(date):
	log_name = "log-" + date.strftime('%Y%m%d') + ".gz"
	os.system("scp" + " " + ORIGIN + log_name + " " + DESTINY)


from datetime import date, timedelta

date = date.today()
today = date.day

if today == 1:
	date -= timedelta(1)
	top_day = date.day
	for i in range(20, top_day + 1):
		get_log(date.replace(day=i))
elif today == 10:
	date -= timedelta(9)
	for i in range(0, 9):
		get_log(date)
		date += timedelta(1)
elif today == 20:
	date -= timedelta(10)
	for i in range(0, 10):
		get_log(date)
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
