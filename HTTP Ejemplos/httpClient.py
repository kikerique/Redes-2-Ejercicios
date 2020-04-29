"""
Ejemplo de un cliente HTTP simple usando la libreria http.client de python

Equipo: Los 4 fantásticos 
"""
import argparse
import http.client, urllib.parse
REMOTE_SERVER_HOST = 'localhost:8000'
params = urllib.parse.urlencode({'number':12524, 'type': 'issue', 'action':'show'}).encode() #codifica los parametros de la peticion POST
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"} #Cabeceras para la petición POST

conn = http.client.HTTPConnection(REMOTE_SERVER_HOST) #Instanciamos la clase HTTPConnection en la URL de nuestro servidor

conn.request("POST", "", params, headers) #Mandamos una peticion tipo POST al servidor
r1 = conn.getresponse()	#Obtenemos la respuesta del servidor
print(r1.status, r1.reason)  #Imprimimos el codigo de Status y la descripción
while True:
     chunk = r1.read(200)  #Leemos los datos de la respuesta con un valor arbitrario de 200 bytes
     if not chunk:
          break
     print(repr(chunk))  #Imprimimos la respuesta del servidor

conn.request("GET", "") #Mandamos una peticion tipo GET al servidor
r1 = conn.getresponse()
print(r1.status,r1.reason)
while True:
     chunk = r1.read(200)  # 200 bytes
     if not chunk:
          break
     print(repr(chunk))

conn.close()     #Cerramos la conexion con el servidor