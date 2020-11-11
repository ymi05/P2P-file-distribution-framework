from socket import *
import threading
import os


class Server:

    def __init__(self, portNumber):
        self.__portNumber__ = portNumber
        self.__socket__ = None
        # each server can handle new connections differently, so we assign the function based on the class
        self.newConnectionsHandler = None

    def startListening(self, host="127.0.0.1"):
        self.__socket__ = socket(AF_INET, SOCK_STREAM)
        self.__socket__.bind((host, self.__portNumber__))
        self.__socket__.listen(5)

    def runServer(self):
        self.startListening()
        print(f"Server started. @ port: {self.__portNumber__}")
        while True:

            connection, addr = self.__socket__.accept()
            print(f"Client connected IP < {addr} >")

            t = threading.Thread(target=self.newConnectionsHandler,  # this depends on what each of the inherited class will use
                                 args=("sendingThread", connection))  # runs send file for each connection

            t.start()
            

        self.__socket__.close()

    def sendFile(self, name, connection, filePath):
        if Server.fileExists(filePath):
            
            connection.send(
                f"EXISTS {os.path.getsize(f'./{filePath}')}".encode())

            userResponse = connection.recv(1024).decode()
            if userResponse[:2] == "OK":
                # we read the file as bytes
                with open(f'./{filePath}', 'rb') as f:
                    bytesToSend = f.read(1024)
                    connection.send(bytesToSend)
                    while bytesToSend != "":  # since we cannot garuntee that the file size will be 1024 bytes, we keep sending until there is nothing
                        bytesToSend = f.read(1024)
                        connection.send(bytesToSend)

        else:
            connection.send("ERR".encode())

        connection.close()

    def establishTCPConnection(self , port , IPAddress = "127.0.0.1"):
        self.__socket__ = socket(AF_INET, SOCK_STREAM)
        self.__socket__.connect((IPAddress, port))
        
    @staticmethod
    def fileExists(filePath) -> bool:
        return os.path.isfile(f"./{filePath}")

    @property
    def portNumber(self):
        return self.__portNumber__

    @property
    def socket(self):
        return self.__socket__
