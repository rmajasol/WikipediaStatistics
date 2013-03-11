# -*- coding: utf8 -*-

# tenemos hebras:
# 		t1, t2 .. tn
# 		p1, p2 .. pn

# hebra t1 arranca, imprimiendo  't1_n'
# hebra p1 'p1_n' espera a finalización de t1
# hebra t2 espera a finalización de t1
# hebra p2 espera a finalización de t2 y p2

import threading
from time import sleep

cond_t = threading.Condition()
cond_p = threading.Condition()


class Hilo_t(threading.Thread):
	def __init__(self, id):
		threading.Thread.__init__(self)
		self.id = id

	def run(self):
		cond_t.acquire()
		sleep(self.id)
		print "t%s\n" % (self.id)
		cond_t.release()
		# for i in range(0, 3):
		# 	sleep(1)
		# 	print "t%s_%s" % (self.id, i)
		# 	sleep(1)


class Hilo_p(threading.Thread):
	def __init__(self, id):
		threading.Thread.__init__(self)
		self.id = id

	def run(self):
		print "p%s\n" % (self.id)
		# for i in range(0, 3):
		# 	sleep(1)
		# 	print "p%s_%s" % (self.id, i)
		# 	sleep(1)

# hago que el hilo p1_1 espere a que finalice el hilo t1_1
t1 = Hilo_t(5)
t2 = Hilo_t(4)
t3 = Hilo_t(3)

t1 = Hilo_t(5)
t2 = Hilo_t(4)
t3 = Hilo_t(3)

t1.start()
t2.start()


# p1 = Hilo_p(1)
# p1.start()


# p1.join()

# for i in range(1, 4):
# 	Hilo_t(i).start()
# 	Hilo_p(i).start()
