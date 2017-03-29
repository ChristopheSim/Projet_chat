import pickle
import socket 
import struct
import sys
import time
import json

SERVERADDRESS = (socket.gethostname(),6005)
 
class ChatServer:
        def __init__(self):
                 self.__s = socket.socket()
                 self.__s.bind(SERVERADDRESS)
                 self.__curClient = ()
                 self._connected = {}

        def run(self):
                self.__s.listen()
                while True:
                        self.__curClient = self.__s.accept()
                        try:
                                data = self.__curClient[0].recv(1024).decode()
                                print(data)
                                data = data.split(',')
                                print('data: ',data[1:])
                                try:
                                        getattr(self,data[0])(data[1:])
                                except Exception as e:
                                        print(e)
                                        print ("commande non valide")
                                        self.__curClient[0].close()
                        except OSError:
                                print("erreur lors de la requète")


        def connect(self, cmd):
                stat = cmd[0] == 'True'
                if stat:
                        self._connected[self.__curClient[1][0]] = {'port' : cmd[1],'pseudo' : 'Jhon Doe'}
                elif not stat:
                        try:
                                del self._connected[self.__curClient[1][0]]
                        except:
                                pass

        def connected(self,*args):
                print('s')
                print(str(self._connected))
                self.send(json.dumps(self._connected))

        def send(self, message):
                msg = message.encode()
                totalsent = 0
                while totalsent < len(msg):
                        sent = self.__curClient[0].send(msg[totalsent:])
                        totalsent += sent       

class ChatClient:
        def __init__(self,command):
                self.__s = socket.socket()
                self.command = command
                self.__s.settimeout(0.5)

        def run(self):
                try:
                        self.__s.connect(SERVERADDRESS)
                        try:
                                self.send(",".join(self.command))
                        except :
                                print ("commande non valide")

                        data = json.loads(self.__s.recv(1024).decode())
                        self.connectedRecv(data)
                        self.__s.close()
                        
                except socket.timeout:
                        pass
                except OSError as e:
                        print (e)
                        print("Problème lors de la connection au server")
                        
        def connectedRecv(self, data):
                for ip in data:
                        print("[{}]    {}\n".format(data[ip]["pseudo"],ip))
                        
        def send(self, message):
                msg = message.encode()
                totalsent = 0
                while totalsent  < len(msg):
                        sent = self.__s.send(msg[totalsent:])
                        totalsent += sent


if __name__ == '__main__':
        if len(sys.argv) == 2 and sys.argv[1] == 'server':
                ChatServer().run()
        elif len(sys.argv) >= 3 and sys.argv[1] == 'client':
                ChatClient(sys.argv[2:]).run()
