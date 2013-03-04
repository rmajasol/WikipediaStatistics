class A(object):
	att1 = "casa"

	# ATT2 = "casa " + self.m2("..mi casa")

	@classmethod
	def m1(self, txt):
		return self.att1 + txt

	@classmethod
	def m3(self, txt):
		return self.m2("/home/rmaja/") + txt

	@staticmethod
	def m2(txt):
		return txt


print A.att1
print A.m1(" es tuya")

# print A.ATT2

print A.m2("hola")

print A.m3("uno.txt")
