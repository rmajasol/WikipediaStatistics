#!/usr/bin/python
# Nombre de Fichero : hilo.py
import threading
from time import sleep


class Hilo(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id

    def run(self):
        sleep(3 - self.id)
        print "Yo soy %s la variable d tiene el valor %s" % (self.id, d)

d = 1

hilos = [Hilo(1),
     Hilo(2),
     Hilo(3)]

for h in hilos:
    h.start()
