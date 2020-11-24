from socket import *
import threading
import os , time


class Server:

    def __init__(self, portNumber , isTracker = False):
        self.__portNumber__ = portNumber
        self.__listeningPortNumber__ = portNumber
        self.listeningSocket = None
        self.tempSocket = None
        # each server can handle connections differently, so we assign the function based on the class
        self.newConnectionsHandler = None
        self.extraOperations = [] #each child might have 0 or more extra and different operations
        self.isTracker = isTracker
        self.UDP_socket = None
        dir = f"Server_files"
        if not os.path.exists(dir):
            os.makedirs(f"./{dir}")


    def startListening(self, host="127.0.0.1"):
        self.listeningSocket = socket(AF_INET, SOCK_STREAM)
        self.listeningSocket.bind((host, self.__portNumber__))
        self.listeningSocket.listen(5)

    def runServer(self):
        self.startListening()
        print(f"Server started. @ port: {self.__portNumber__}")
        while True:

            connection, addr = self.listeningSocket.accept()
            print(f"Client connected IP < {addr} >")


            
            listeningThread = threading.Thread(target=self.newConnectionsHandler,  # this depends on what each of the inherited class will use
                                 args=("listeningThread", connection))  # runs send file for each connection
           
            listeningThread.start()
            

        self.listeningSocket.close()

    def start(self):
        if len(self.extraOperations) > 1 : #we run the opertaitions each child has 
            for opertaion in self.extraOperations:
                operationsThread = threading.Thread(target=opertaion)       
                operationsThread.start()
        time.sleep(4)
        runServerThread = threading.Thread(target=self.runServer)       
        runServerThread.start()
    

    def sendFile(self, name, connection, filePath):
        # if Server.fileExists(filePath):

            connection.send(
                f"EXISTS--{os.path.getsize(f'{filePath}')}--{filePath}".encode())
         
            userResponse = connection.recv(1024).decode()
            if userResponse[:2] == "OK":
                # we read the file as bytes
                with open(f'./{filePath}', 'rb') as f:
                    bytesToSend = f.read(1024)
                    connection.send(bytesToSend)
                    while bytesToSend != b'':  # since we cannot garuntee that the file size will be 1024 bytes, we keep sending until there is nothing
                        bytesToSend = f.read(1024)
                        connection.send(bytesToSend)
        
            connection.close()

    def establishTCPConnection(self , port , IPAddress = "127.0.0.1"):
        try:
            newSocket = socket(AF_INET, SOCK_STREAM)
            newSocket.connect((IPAddress, port))
            print(f"Connecting to {(IPAddress, port)}")
            time.sleep(2)
            return newSocket
        except:
            print("ERROR")
            return None
        
        
    @staticmethod
    def fileExists(filePath) -> bool:
        return os.path.isfile(filePath)

    @property
    def listeningPortNo(self):
        return self.__listeningPort__

    @property
    def tempPocket(self):
        return self.tempSocket
