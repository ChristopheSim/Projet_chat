import pickle
import socket 
import struct
import sys
import time
import json
import threading

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
                                data = data.split(',')
                                try:
                                        getattr(self,data[0])(data[1:])
                                except Exception as e:
                                        print(e)
                                        print ("commande non valide")
                                        
                        except OSError:
                                print("erreur lors de la requète")

                        finally:
                                self.__curClient[0].close()
                                

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
                print(str(self._connected))
                self.send(json.dumps(self._connected))

        def editPseudo(self,pseudo):
                pseudo = pseudo[0]
                self._connected[self.__curClient[1][0]]["pseudo"] = pseudo

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
                        except Exception as e:
                                
                                print ("commande non valide: ",e)

                        data = json.loads(self.__s.recv(1024).decode())
                        self.connectedRecv(data)
                        
                except socket.timeout:
                        pass
                except OSError as e:
                        print("Problème lors de la connection au server",e)
                except:
                        pass
                finally:
                        self.__s.close()
                        
        def connectedRecv(self, data):
                for ip in data:
                        print("[{}]    {}\n".format(data[ip]["pseudo"],ip))
                        
        def send(self, message):
                msg = message.encode()
                totalsent = 0
                while totalsent  < len(msg):
                        sent = self.__s.send(msg[totalsent:])
                        totalsent += sent
class Chat:
        def __init__(self, host=socket.gethostname(), port=5000):
                s = socket.socket(type=socket.SOCK_DGRAM)
                s.settimeout(0.5)
                s.bind(("0.0.0.0", 5001))
                self.__s = s
                print('Écoute sur {}:{}'.format(host, port))
                self.__port = port
                

        def run(self):
                handlers = {
                '/exit': self._exit,
                '/quit': self._quit,
                '/connect': ChatClient(['connect','True', str(self.__port)]).run,
                '/disconnect': ChatClient(['connect','False']).run,
                '/connected': ChatClient(['connected']).run
            }
                self.__running = True
                self.__address = None
                threading.Thread(target=self._receive).start()
                while self.__running:
                        line = sys.stdin.readline().rstrip() + ' '
                        # Extract the command and the param
                        command = line[:line.index(' ')]
                        param = line[line.index(' ')+1:].rstrip()
                        # Call the command handler
                        if command in handlers:

                               
                                
                                try:
                                        # /!\ code bourriner. A réparer 
                                        if command == '/connected': ChatClient(['connected']).run()
                                        elif command == '/connect': ChatClient(['connect','True', str(self.__port)]).run()
                                        elif command == '/disconnect':  ChatClient(['connect','False']).run()
                                        else: handlers[command]()
                                        
                                except Exception as e:
                                        print (e)
                                        print("Erreur lors de l'exécution de la commande.")
                        else:
                                print('Command inconnue:', command)
        def _receive(self):
                while self.__running:
                        try:
                                data, address = self.__s.recvfrom(1024)
                                print('[', address, ']')
                                print(data.decode())
                                sys.stdout.flush()
                
                        except socket.timeout:
                                pass
                        except OSError:
                                return
        def _exit(self):
                self.__running = False
                self.__address = None
                self.__s.close()
    
        def _quit(self):
                self.__address = None

if __name__ == '__main__':
        if len(sys.argv) == 2 and sys.argv[1] == 'server':
                ChatServer().run()
        elif len(sys.argv) >= 3 and sys.argv[1] == 'client':
                ChatClient(sys.argv[2:]).run()
        elif len(sys.argv) == 3 and sys.argv[1] == 'chat':
                Chat(sys.argv[1], int(sys.argv[2])).run()
        else:
                Chat().run()

