import pickle
import socket 
import struct
import sys

SERVERADDRESS = (socket.gethostname(),6000)

class ChatServer:
 	def __init__(self):
 		self.__s = socket.socket()
 		self.__s.bind(SERVERADDRESS)
 		self._connected = []

 	def run(self):
 		self.__s.listen()
 		while True:
 			print("hellow")
 			client, address = self.__s.accept()
 			self._connected.append((client,address)) 
 			try:
 				print(client,address)
 				client.close()
 			except OSError:
 				print("erreur lors de la requète") 

class ChatClient:
	def __init__(self,command = '' ):
		self.__data = [int(x) for x in command]
		self.__s = socket.socket()

	def run(self):
		try:
			self.__s.connect(SERVERADDRESS)
			self.__s.close()
		except OSError:
			print("Problème lors de la connection au server")

if __name__ == '__main__':
	if len(sys.argv) == 2 and sys.argv[1] == 'server':
		ChatServer().run()
	elif len(sys.argv) > 2 and sys.argv[1] == 'client':
		ChatClient().run()