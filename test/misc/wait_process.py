
# http://stackoverflow.com/questions/12057794/python-using-popen-poll-on-background-process

import time
import subprocess

s = "jajajaja/"
print s[0:len(s) - 1]

if s is None:
	a = "hola"
else:
	a = "adios"

print a

p = subprocess.Popen("sleep 10", shell=True)
# Better: p = subprocess.Popen(["sleep", "30"])

# Wait until process terminates
while p.poll() is None:
	time.sleep(0.5)

# It's done
print "Process ended, ret code:", p.returncode
