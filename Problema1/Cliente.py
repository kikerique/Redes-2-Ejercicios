#!/usr/bin/env python3
import speech_recognition as sr
import socket
import os
import time
import sys

r = sr.Recognizer()
r.dynamic_energy_threshold = True

if len(sys.argv) != 3:
    print("uso:", sys.argv[0], "<host> <port>")
    sys.exit(1)
host, port= sys.argv[1:3]
buffer_size = 1024
serveraddr = (host, int(port))
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect(serveraddr)
    while True:
    	data = TCPClientSocket.recv(buffer_size)
    	print(data.decode())
    	if data.decode()=="Escribe tu nombre: ":
    		request=input("R: ")
    		TCPClientSocket.send(request.encode())
    	if data.decode()=="Juega:":
            input("Presiona [Enter] para hablar")
            with sr.Microphone() as source:
                audio=r.listen(source)
            print("Tu jugada se ha guardado")
            datos=audio.get_wav_data()
            t=len(datos)
            TCPClientSocket.send(str(t).encode())
            time.sleep(1)
            enviados=0
            while enviados<t:
                res=TCPClientSocket.send(datos[enviados:])
                if res == 0:
                    print("conexión interrumpida")
                    break
                enviados+=res
            time.sleep(0.1)
            TCPClientSocket.send("Archivo enviado".encode())
            print("Archivo enviado")
    	if data.decode()=='':
    		print("Error, saliendo")
    		break
    	if data.decode()=="Hasta luego":
    		break
    try:
        os.remove(request+"-microphone-results.wav")
    except:
        pass