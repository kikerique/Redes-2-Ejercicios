import speech_recognition as sr
import time
from os import path

class handlerJugadas:
    def __init__(self,socket,nombre,tab):
        #Constructor de la clase personajes aquí se llenará el diccionario personajes al azar
        self.cliente=socket
        self.name=nombre
        self.tablero=tab
        self.bloqueados=[]
    def pideJugada(self):
        intentosConexion=0
        intentosJugada=0
        jugada=self.recibeJugada()
        while jugada=="Audio Ilegible" or jugada=="No se puede acceder al servicio":
            if jugada=="No se puede acceder al servicio":
                intentosConexion+=1
                self.cliente.send("No se puede acceder al servicio, reintentando".encode())
                time.sleep(0.5)
            if jugada=="Audio Ilegible":
                intentosJugada+=1
                self.cliente.send("Audio ilegible".encode())
                time.sleep(0.5)
            if intentosConexion>3:
                self.cliente.send("Numero de intentos de conexion maximos alcanzado, revisa tu conexion".encode())
                break
            if intentosJugada>3:
                self.cliente.send("Hay mucho ruido en tus grabaciones, revisa tu microfono".encode())
                break
            jugada=self.recibeJugada()
        return jugada
    def verificaJugada(self,comando):
        #Función que se encargará de responder al cliente el resultado de su jugada
        caracteristica=""
        correcto,diccionario=self.tablero.getGanador()
        caracteristicas=diccionario.keys()
        #Se asume que el comando es "El personaje correcto es (nombre)"
        if "correcto" in comando:
            for element in comando:
                if element.lower()==correcto.lower():
                    return "Has adivinado"
            return "No, sigue intentando"
        for element in comando:
            if element in caracteristicas:
                caracteristica=element
                break
        if caracteristica=="":
            return "Comando invalido"
        else:
            valor=diccionario[caracteristica].lower()
            for element in comando:
                if element==valor:
                    return "SI"
            return "NO"


        pass
    def recibeJugada(self):
        #Función que se encargará de recolectar los datos del cliente y de pasar de audio a texto
        self.cliente.send("Ya es tu turno".encode())
        time.sleep(0.5)
        self.cliente.send("Juega:".encode())
        time.sleep(0.5)  
        data = self.cliente.recv(32)
        #print("Bytes del archivo: "+data.decode())
        f=open(self.name+"-jugada.wav","wb")
        while True:
            datos=self.cliente.recv(2048)
            try:
                if datos.decode()=="Archivo enviado":
                    break
            except:
                pass
            f.write(datos)
        f.close()
        #print("Archivo recibido")
        #print("Archivo guardado")
        return self.speechRecognizer()
    def limpiaJugada(self,comando):
        resultado=comando
        reemplazar={"á":"a","é":"e","í":"i","ó":"o","ú":"u"}
        llaves=reemplazar.keys()
        conectores=['el','la','los','de','es','tiene']
        for element in conectores:
            while (element in comando):
                resultado.remove(element)
        for i in range(len(comando)):
            string=""
            for j in range(len(comando[i])):
                if (comando[i][j] in llaves):
                    string+=str(reemplazar[comando[i][j]])
                else:
                    string+=str(comando[i][j])
            comando[i]=string
        return resultado
    def dimeComando(self,jugada):
        #Función que se encargará de traducir el texto de la jugada a un comando
        #print("INICIANDO reconocimiento de comando")
        comando=jugada.split()
        comando=self.limpiaJugada(comando)
        if ("quiero" in comando) and ("salir" in comando):
            return (1,"Salir")
        if ("bloquea" in comando):
            self.bloqueaJugador(comando)
            return (2,comando)
        else:
            return (3,comando)
    def speechRecognizer(self):
        #Funcion encargada de pasar de un archivo de audio a texto
        #print("INICIANDO speechRecognizer")
        AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), self.name+"-jugada.wav")
        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)  # read the entire audio file
        #print("datos del audio recogidos")
        try:
            text=r.recognize_ibm(audio)
            #print("finalizo la traduccion")
            return text
        except sr.UnknownValueError:
            return "Audio Ilegible"
        except sr.RequestError as e:
            return "No se puede acceder al servicio"
    def bloqueaJugador(self,comando):
        #Se asume que el comando es "bloquea al personaje nombre"
        if len(comando)==4:
            for i in range(len(comando)):
                if comando[i]=="personaje" and i+1<len(comando):
                    nombre=comando[i+1].lower()
                    if not(nombre in self.bloqueados):
                        self.bloqueados.append(nombre)
                        self.cliente.send(str("Personaje "+ nombre+ " bloqueado").encode())
                        time.sleep(0.1)
                    else:
                        self.cliente.send("El personaje ya estaba bloqueado".encode())
                        time.sleep(0.1)
        else:
            self.cliente.send("Comando incorrecto".encode())
            time.sleep(0.1)
    