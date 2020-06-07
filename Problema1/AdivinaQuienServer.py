# !/usr/bin/env python3

import socket
import sys
from hiloServidor import hiloServidor
import threading
import time
from Personajes import personajes


def servirPorSiempre(socketTcp,condition):
    tablero=None
    try:
        while True:
            client_conn, client_addr = socketTcp.accept()
            if (threading.active_count()-1)<int(sys.argv[3]):
                if threading.active_count()-1==0:
                    #Crea un nuevo tablero para jugar
                    tablero=personajes()
                print("Conectado a", client_addr)
                client_conn.send("Bienvenido Usuario".encode())
                time.sleep(0.5)
                client_conn.send("Escribe tu nombre: ".encode())
                nombre=client_conn.recv(1024).decode()
                nuevoCliente = hiloServidor(client_conn,condition,int(sys.argv[3]),nombre,tablero)
                nuevoCliente.start()
            else:
                client_conn.send("Servidor lleno".encode())
                client_conn.send("Hasta luego".encode())
                client_conn.close()
    except KeyboardInterrupt:
        print("Deteniendo el servidor")
        socketTcp.close()
        sys.exit(1)
    except Exception as e:
        print(e)





host, port, numConn = sys.argv[1:4]

if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <num_connections>")
    sys.exit(1)

serveraddr = (host, int(port))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind(serveraddr)
    TCPServerSocket.listen(int(numConn))
    print("El servidor TCP está disponible y en espera de solicitudes")
    condition = threading.Condition()
    servirPorSiempre(TCPServerSocket,condition)
