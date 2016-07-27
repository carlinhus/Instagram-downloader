# -*- coding: utf-8 -*-
#
#	@author Carlos Campo Liébana
#	@license MIT
#

import requests
from PIL import Image
from StringIO import StringIO
import sys
import json
import os
import sys

user = sys.argv[1]
urlBase = "https://www.instagram.com/" + user + "/media/"
max_id = ""
haySiguiente = True;
siguiente = ""
pagina = 1;
imagenes = list()
while(haySiguiente):
	response = requests.get(urlBase + siguiente)
	io = StringIO(response.content)
	jsonResponse = json.load(io)
	if not jsonResponse["items"]:
		print("El usuario tiene perfil privado, no tiene imágenes o no existe")
		sys.exit()
	print("Cargando página " + str(pagina) + "\n")
	for item in jsonResponse["items"]:
		siguiente = "?max_id=" + item["id"]
		imagenes.append(item["images"]["standard_resolution"]["url"])
	haySiguiente = jsonResponse["more_available"]
	pagina += 1
if not os.path.exists("./fotos/" + user + "/"):
    os.makedirs("./fotos/" + user + "/")
#Recorremos todas las imagenes
cuenta = 1

for ruta in imagenes:
	try:
		print ruta + "\n"
		response = requests.get(ruta + max_id)
		img = Image.open(StringIO(response.content))
		img.save("./fotos/" + user + "/" + str(cuenta) + ".jpg", "JPEG")
		cuenta += 1
	except IOError as err:
		print "AVISO: La imagen con url " + ruta + " no pudo ser descargada\n"
print "TERMINADO\n"