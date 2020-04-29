"""
Ejemplo de un servidor HTTP simple usando la libreria http.server de python

Equipo: Los 4 fantásticos 
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO

#Clase que implementa la clase BaseHTTPRequestHandler para atender a las peticiones 
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        #Método necesario para manejar las peticiones GET
        self.send_response(200)         #Método que envia un codigo de status de respuesta al buffer interno
        self.end_headers()              #Método necesario para indicar el fin de las cabeceras HTTP en el buffer de respuesta
        self.wfile.write(b'Hola, hiciste una peticion GET') #Contiene el flujo de salida para regresarle una respuesta al cliente

    def do_POST(self):
        #Método necesario para manejar las peticiones POST
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)  #rfile especifica el flujo de entrada para leer los datos recibidos
        self.send_response(200)
        self.end_headers()
        response = BytesIO()  #Crea un buffer para escribir datos
        response.write(b'Hiciste una peticion POST. ') #El metodo write agrega los datos enviados como parámetros al buffer creado
        response.write(b'Recibi esto: ')
        response.write(body)
        self.wfile.write(response.getvalue())
    def do_HEAD(self):
        """
        Método necesario para manejar las peticiones HEAD
        estas peticiones no se contestan con ningún mensaje, sólo con un código de status de respuesta
        """
        self.send_response(200)
        self.end_headers()


try:
    #Instanciamos la clase HTTPServer, establecemos su dirección de HOST y  el PORT junto con la clase que atenderá las peticiones
    server = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler) 
    print("Servidor listo en la direccion: localhost:8000")
    server.serve_forever()  #Ponemos el servidor en espera de manera indefinida para que acepte las peticiones de los clientes

except KeyboardInterrupt:
    print(' recibido, se cerrara el Servidor')
    server.socket.close() #Cerramos el socket por donde se comunicaba el servidor
