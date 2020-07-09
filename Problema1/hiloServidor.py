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
        self.tablero.turnos.append(nombre)
        self.name=nombre
        self.bandera=False

    def jugadoresIncompletos(self):
        self.cliente.send("Debes de esperar a que se conecten todos los jugadores".encode())
        self.cliente.send(str("Jugadores necesarios para iniciar: "+str(self.MAX_Conexiones)).encode())
        time.sleep(0.5)
        self.cliente.send(str("Jugadores actualmente conectados: "+ str(threading.active_count()-1)).encode())
        self.bandera=True
    def bienvenidaUsuario(self):
        self.cliente.send(str("Bienvenido "+self.name+"\n").encode())
        self.cliente.send("Las reglas del juego son las siguientes:".encode())
        time.sleep(0.1)
        self.cliente.send("Para bloquear a un personaje y evitar que se muestre su descripción di exactamente esto: 'Bloquea al personaje (nombre del personaje)'\n".encode())
        self.cliente.send("Para salir del juego di: 'quiero salir'\n".encode())
        time.sleep(0.1)
        self.cliente.send("Para realizar una jugada debes de mencionar al menos la caracteristica y el valor de ella, por ejemplo:\n".encode())
        self.cliente.send("El personaje tiene PELO color NEGRO, siendo pelo y negro lo minimo que tienes que decir\n".encode())
        time.sleep(0.1)
        self.cliente.send("Cualquier otra cosa que digas sera tomada como un comando incorrecto y perderas el turno\n".encode())
        self.cliente.send("Disfruta del juego\n".encode())
        time.sleep(0.1)
    
    def imprimeTablero(self):
        for key in self.tablero.personajes:
            if not(key.lower() in self.handler.bloqueados):
                self.cliente.send(str(key + ":\n").encode())
                string=str(self.tablero.personajes[key])
                self.cliente.send(str(string + ":\n").encode())
                time.sleep(0.1)
        if self.tablero.ultimaJugada!=None:
            self.cliente.send(('\n'.join(self.tablero.ultimaJugada)).encode())
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
                            self.bienvenidaUsuario()
                            self.jugadoresIncompletos()
                            self.ventana.wait()
                        if((threading.active_count()-1==self.MAX_Conexiones and self.MAX_Conexiones>1) and self.bandera==False):
                            self.bienvenidaUsuario()
                            self.cliente.send("Todos los jugadores se han conectado, ahora espera tu turno".encode())
                            self.ventana.notify()
                            self.bandera=True
                            self.ventana.wait()
                        if (threading.active_count()-1)>1:
                            actual=self.tablero.turnos[0]
                            while actual!=self.name:
                                self.ventana.notify()
                                self.ventana.wait()
                                actual=self.tablero.turnos[0]
                        try:
                            self.tablero.turnos.pop(0)
                        except:
                            pass
                        self.imprimeTablero()
                        jugada=self.handler.pideJugada()
                        numero,descripcion=self.handler.dimeComando(jugada.lower())
                        if numero==2:
                            while numero==2:
                                #self.cliente.send(str("Este fue tu comando "+jugada).encode())
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
                                    self.tablero.ultimaJugada.append(str("Ultima Jugada: Intento de adivinar el personaje de parte del jugador "+self.name))
                                else:    
                                    self.tablero.ultimaJugada.append(str("Jugada: "+jugada+" respuesta: "+respuesta))
                                self.cliente.send(str("Tu jugada fue esta: "+jugada).encode())
                                self.cliente.send(str("Esta es la respuesta: "+respuesta).encode())
                        time.sleep(0.5)
                        self.cliente.send("Tu turno ha terminado, espera tu turno".encode())
                        self.ventana.notify()
                        if (threading.active_count()-1)>1:
                            self.tablero.turnos.append(self.name)
                            self.ventana.wait()
                    else:
                        self.cliente.send(str("El juego ha terminado, ha ganado el jugador "+ self.tablero.ganador).encode())
                        time.sleep(0.1)
                        break
            try:
                archivo=str(self.name+"-jugada.wav")
                os.remove(archivo)
            except:
                pass
            self.cliente.send("Hasta luego".encode())
            self.cliente.close()
        except IOError as e:
            with self.ventana:
                self.ventana.notify()
            print(e)