#!/usr/bin/python

import os
import ConfigParser
import subprocess
import time
import signal

# Leemos del archivo de configuracion 'config.cfg'
cfg = ConfigParser.ConfigParser()
cfg.read(["config.cfg"])
USER = cfg.get("bd_connection", "user")
PASS = cfg.get("bd_connection", "pass")
LOGS_DIR = cfg.get("other", "logs_dir")

os.chdir("wikisquilter")

cmd = "java -cp " + \
	"./build/classes:./dist/lib/mysql-connector-java-5.1.5-bin.jar " + \
	"wikisquilter.Main 'jdbc:mysql://localhost:3306/squidlogs' " + \
	USER + " " + PASS + ' AllRequests Filtered Searches ' + \
	'cfgWPFilter.xml ' + LOGS_DIR + " -f log-20120615.gz 06 " + \
	'sal33.txt err33.txt -d -f -i -r &'

pro = subprocess.Popen(cmd, stdout=subprocess.PIPE,
	shell=True, preexec_fn=os.setsid)

time.sleep(10)

os.killpg(pro.pid, signal.SIGTERM)
