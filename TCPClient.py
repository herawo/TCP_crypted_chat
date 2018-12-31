#!/usr/bin/python3
# -*- coding: utf-8 -*-
import socket
import sys
import threading
import time
from Crypto import Random
from CleverReceiver import CleverReceiver
from CleverReceiver import CleverSender
import hashlib

clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port = 5000

host = sys.argv[1]
pseudo = sys.argv[2]
md5 = ""
if len(sys.argv) >= 4:
	passphrase = sys.argv[3]
	md5 = hashlib.md5()
	md5.update(passphrase.encode("utf-8"))
	md5 = md5.hexdigest()

allow_no_encrypt = True
if len(sys.argv) >= 5:
	if sys.argv[4] == "-c":
		allow_no_encrypt = False
	else:
		raise Exception("unknown argument " + sys.argv[4])

receiver = CleverReceiver(md5, allow_no_encrypt)
sender = CleverSender(md5, allow_no_encrypt)

clientsocket.connect((host, port))
clientsocket.send(bytes("#pseudo=" + pseudo, 'utf-8'))
message = ""

def receive():
	while 1:
		rcv_message = clientsocket.recv(1024)
		
		decoded = receiver.decypher_and_decode(rcv_message)
		if receiver.pseudo :
			print(receiver.pseudo.decode() + " : " + decoded)
		else:
			print(decoded)

threading.Thread(target=receive).start()
time.sleep(1)

while message is not "\quit":
	message = input()
	encrypted_message = sender.send_message(message)
	clientsocket.send(encrypted_message)

clientsocket.close()

print(message.decode('ascii'))
