#!/usr/bin/env python3
import speech_recognition as sr
import socket
import os
import time

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
buffer_size = 1024
r = sr.Recognizer()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    while True:
    	data = TCPClientSocket.recv(buffer_size)
    	print(data.decode())
    	if data.decode()=="Dime tu nombre: ":
    		request=input("R: ")
    		TCPClientSocket.send(request.encode())
    	if data.decode()=="Juega:":
            input("Presiona [Enter] para hablar")
            with sr.Microphone() as source:
                audio=r.listen(source)
            print("Tu respuesta se ha guardado")
            with open(request+"-microphone-results.wav", "wb") as f:
                f.write(audio.get_wav_data())
            t=os.stat(request+"-microphone-results.wav").st_size
            TCPClientSocket.send(str(t).encode())
            time.sleep(1)
            TCPClientSocket.send(audio.get_wav_data())
    	if data.decode()=='':
    		print("Error, saliendo")
    		break
    	if data.decode()=="Hasta luego":
    		break