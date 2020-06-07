import speech_recognition as sr
import threading
import time
from os import path
from handlerJugadas import handlerJugadas

class hiloServidor(threading.Thread):
    def __init__(self,socket,condition,jugadores,nombre,personajes):
        super(hiloServidor,self).__init__()
        self.cliente = socket
        self.handler=handlerJugadas(socket,nombre,personajes)
        self.ventana=condition
        self.MAX_Conexiones=jugadores
        self.tablero=personajes
        self.name=nombre
        self.bandera=False

    def jugadoresIncompletos(self):
        self.cliente.send("Debes de esperar a que se conecten todos los jugadores".encode())
        self.cliente.send(str("Jugadores necesarios para iniciar: "+str(self.MAX_Conexiones)).encode())
        time.sleep(0.5)
        self.cliente.send(str("Jugadores actualmente conectados: "+ str(threading.active_count()-1)).encode())
        self.bandera=True
    
    def imprimeTablero(self):
        for key in self.tablero.personajes:
            if not(key.lower() in self.handler.bloqueados):
                self.cliente.send(str(key + ":\n").encode())
                string=str(self.tablero.personajes[key])
                self.cliente.send(str(string + ":\n").encode())
                time.sleep(0.1)
        if self.tablero.ultimaJugada!=None:
            self.cliente.send(self.tablero.ultimaJugada.encode())
    def juegoTerminado(self):
        return self.tablero.ganador

    def run(self):
        intentosConexion=0
        intentosJugada=0
        try:
            while True:
                with self.ventana:
                    if not(self.juegoTerminado()):
                        if ((threading.active_count()-1)<self.MAX_Conexiones and self.bandera==False):
                            self.jugadoresIncompletos()
                            self.ventana.wait()
                        if((threading.active_count()-1==self.MAX_Conexiones and self.MAX_Conexiones>1) and self.bandera==False):
                            self.cliente.send("Todos los jugadores se han conectado, ahora espera tu turno".encode())
                            self.ventana.notify()
                            self.bandera=True
                            self.ventana.wait()
                        self.imprimeTablero()
                        jugada=self.handler.pideJugada()
                        numero,descripcion=self.handler.dimeComando(jugada.lower())
                        if numero==2:
                            while numero==2:
                                self.cliente.send(str("Este fue tu comando "+jugada).encode())
                                self.imprimeTablero()
                                jugada=self.handler.pideJugada()
                                numero,descripcion=self.handler.dimeComando(jugada.lower())
                        if numero==1:
                            self.ventana.notify()
                            break
                        if numero==3:
                            #aquí se verifica la jugada
                            respuesta=self.handler.verificaJugada(descripcion)
                            if respuesta=="Has adivinado":
                                self.tablero.ganador=self.name
                                self.cliente.send("Felicidades, Has ganado el juego".encode())
                                time.sleep(0.1)
                                self.ventana.notify()
                                break
                            else:
                                if respuesta=="No, sigue intentando":
                                    self.tablero.ultimaJugada=str("Ultima Jugada: Intento de adivinar el personaje de parte del jugador "+self.name)
                                else:    
                                    self.tablero.ultimaJugada=str("Ultima Jugada: "+jugada+" respuesta: "+respuesta)
                                self.cliente.send(str("Tu jugada fue esta: "+jugada).encode())
                                self.cliente.send(str("Esta es la respuesta: "+respuesta).encode())
                        time.sleep(0.5)
                        self.cliente.send("Tu turno ha terminado, espera tu turno".encode())
                        self.ventana.notify()
                        if (threading.active_count()-1)>1:
                            self.ventana.wait()
                    else:
                        self.cliente.send(str("El juego ha terminado, ha ganado el jugador "+ self.tablero.ganador).encode())
                        time.sleep(0.1)
                        break
            try:
                archivo=path.join(path.dirname(path.realpath(__file__)), self.name+"-jugada.wav")
                os.remove(archivo)
            except:
                pass
            self.cliente.send("Hasta luego".encode())
            self.cliente.close()
        except IOError as e:
            with self.ventana:
                self.ventana.notify()
            print(e)