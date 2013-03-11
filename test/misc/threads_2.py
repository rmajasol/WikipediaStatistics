#!/usr/bin/python
# Nombre de Fichero : lote.py
import threading
from os import system
from time import sleep


class Trabajo(threading.Thread):
    """
    Esta es la clase Trabajo. Los Trabajos  se pueden ejecutar de 4 maneras
    Que esperen a estar solos para ejecutarse.
    Que esperen a estar solos para ejecutarse y no dejar ejecutar ningun otro
    hasta terminar.
    Que no dejen ejecutar a ninguno otro hasta terminar.
    Que se ejecuten sin restricciones mientras los otros lo dejen
    """
    def __init__(self, id, cmd, entroSolo=False, salgoSolo=False):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.id = id
        self.entroSolo = entroSolo
        self.salgoSolo = salgoSolo

    def run(self):
        system(self.cmd)

print "lotePy  0.0.1"

tabajos = [Trabajo(1, "calc", True, True),
    Trabajo(2, "Notepad", True),
    Trabajo(3, "dir c:\\", True)]

for t in tabajos:
    while (t.entroSolo) and (threading.activeCount() != 1):
        pass
    t.start()
    if (t.salgoSolo):
        t.join()
