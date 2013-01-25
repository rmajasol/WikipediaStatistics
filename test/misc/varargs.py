

def f(a, *b):
	if b:
		print "hay argumento b" + "".join(str(b))
	else:
		print "no hay argumento"

f('arbol', 3, 5, 6)
f('arbol')
