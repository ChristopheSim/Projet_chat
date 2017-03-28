 import pickle
 import socket 
 import struct
 import sys

SERVERADDRESS = (socket.gethostname(),6000)
 class ChatServer:
 	def __init__(self):
 		self.__s = socket.socket()
 		self.__s.bind(SERVERADDRESS)