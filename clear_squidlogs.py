#!/usr/bin/python

import os
import ConfigParser

# Leemos del archivo de configuracion 'config.cfg'
cfg = ConfigParser.ConfigParser()
cfg.read(["config.cfg"])
USER = cfg.get("bd_connection", "user")
PASS = cfg.get("bd_connection", "pass")

os.system("mysql -u " + USER + " -p" + PASS + \
	" < sql_scripts/clear_squidlogs.sql")
