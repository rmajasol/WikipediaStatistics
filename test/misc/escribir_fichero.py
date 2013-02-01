#!/usr/bin/python


# http://chuwiki.chuidiang.org/index.php?title=Leer_y_escribir_ficheros_en_python
f = open("fichero.txt", "a")
f.write("hola\n")
f.close()

# http://maengora.blogspot.com.es/2010/10/receta-python-buscar-una-cadena-de-un.html
f = open("fichero.txt")
lines = f.readlines()
for l in lines:
	if l == "hola\n":
		print "existe!"
		break
	else:
		print "no existe.."
