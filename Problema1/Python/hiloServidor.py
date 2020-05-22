import speech_recognition as sr
import threading
import time
from os import path


class hiloServidor(threading.Thread):
    cliente=None
    ventana=None
    MAX_Conexiones=0
    bandera=False
    intentos=0
    #Agregar una lista que contenga los nombres de los jugadores bloqueados por el usuario
    def __init__(self,socket,condition,jugadores,nombre):
        super(hiloServidor,self).__init__()
        self.cliente = socket
        self.ventana=condition
        self.MAX_Conexiones=jugadores
        self.name=nombre
    def jugadoresIncompletos(self):
        self.cliente.send("Debes de esperar a que se conecten todos los jugadores".encode())
        self.cliente.send(str("Jugadores necesarios para iniciar: "+str(self.MAX_Conexiones)).encode())
        time.sleep(0.5)
        self.cliente.send(str("Jugadores actualmente conectados: "+ str(threading.active_count()-1)).encode())
        self.bandera=True

    def verificaJugada(self):
        #Función que se encargará de responder al cliente el resultado de su jugada
        pass
    def recibeJugada(self,data):
        #Función que se encargará de recolectar los datos del cliente y de pasar de audio a texto
        self.cliente.send("Ya es tu turno".encode())
        time.sleep(0.5)
        self.cliente.send("Juega:".encode())
        time.sleep(0.5)  
        data = self.cliente.recv(1024)
        print("Bytes del archivo: "+data.decode())
        f=open(path.join(path.dirname(path.realpath(__file__)), self.name+"-jugada.wav"),"wb")
        leidos=0
        while leidos<int(data):
            escribir=self.cliente.recv(2048)
            f.write(escribir)
            leidos+=2048
        f.close()
        return self.speechRecognizer()
    def dimeComando(self,jugada):
        #Función que se encargará de traducir el texto de la jugada a un comando
        self.cliente.send(str("Dijiste esto: "+jugada).encode())
        time.sleep(0.5)
    def speechRecognizer(self):
        #Funcion encargada de pasar de un archivo de audio a texto
        AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), self.name+"-jugada.wav")
        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source,)  # read the entire audio file
        try:
            text=r.recognize_ibm(audio,language="es-MX")
            return text
        except sr.UnknownValueError:
            return "Audio Ilegible"
        except sr.RequestError as e:
            return "No se puede acceder al servicio"
    def run(self):
        try:
            while True:
                with self.ventana:
                    if ((threading.active_count()-1)<self.MAX_Conexiones and self.bandera==False):
                        self.jugadoresIncompletos()
                        self.ventana.wait()
                    if((threading.active_count()-1==self.MAX_Conexiones and self.MAX_Conexiones>1) and self.bandera==False):
                        self.cliente.send("Todos los jugadores se han conectado, ahora espera tu turno".encode())
                        self.ventana.notify()
                        self.bandera=True
                        self.ventana.wait()  
                    jugada=self.recibeJugada(data.decode())
                    while jugada=="Audio Ilegible" or jugada=="No se puede acceder al servicio":
                        if jugada=="No se puede acceder al servicio":
                            self.intentos+=1
                        if intentos>3:
                            self.cliente.send("Numero de intentos de conexion maximos alcanzado, revisa tu conexion".encode())
                            break
                        jugada=self.recibeJugada(data.decode())
                    if jugada.lower()=="quiero salir":
                        self.ventana.notify()
                        break
                    self.dimeComando(jugada)
                    self.ventana.notify()
                    if (threading.active_count()-1)>1:
                        self.ventana.wait()
            self.cliente.send("Hasta luego".encode())
            self.cliente.close()
        except IOError as e:
            with self.ventana:
                self.ventana.notify()
            print(e)