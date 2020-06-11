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
            with open(request+"-microphone-results.wav", "wb") as f:
                f.write(audio.get_wav_data())
            t=os.stat(request+"-microphone-results.wav").st_size
            TCPClientSocket.send(str(t).encode())
            time.sleep(1)
            with open(request+"-microphone-results.wav", "rb") as f:
                datos=f.read(2048)
                while datos:
                    TCPClientSocket.send(datos)
                    time.sleep(0.1)
                    datos=f.read(2048)
    	if data.decode()=='':
    		print("Error, saliendo")
    		break
    	if data.decode()=="Hasta luego":
    		break
    try:
        os.remove(request+"-microphone-results.wav")
    except:
        pass