from socket import *
import threading
import os


class Server():

    def __init__(self, portNumber):
        self.__portNumber__ = portNumber
        self.__socket__ = None
        self.newConnectionsHandler = None

    def startListening(self, host="127.0.0.1"):
        self.__socket__ = socket(AF_INET, SOCK_STREAM)
        self.__socket__.bind((host, self.__portNumber__))
        self.__socket__.listen(5)

    def runServer(self):
        self.startListening()
        print("Server started.")
        while True:

            connection, addr = self.__socket__.accept()
            print(f"Client connected IP < {addr} >")

            t = threading.Thread(target=self.newConnectionsHandler,
                                 args=("sendingThread", connection))  # runs send file for each connection

            t.start()

        self.trackerSocket.close()

    @staticmethod
    def fileExists(fileName) -> bool:
        return os.path.isfile(f"./Server_files/{fileName}")

    def sendFile(self, name, connection, fileName):
        if Server.fileExists(fileName):
            connection.send(
                f"EXISTS {os.path.getsize(f'./Server_files/{fileName}')}".encode())

            userResponse = connection.recv(1024).decode()
            if userResponse[:2] == "OK":
                # we read the file as bytes
                with open(f'./Server_files/{fileName}', 'rb') as f:
                    bytesToSend = f.read(1024)
                    connection.send(bytesToSend)
                    while bytesToSend != "":  # since we cannot garuntee that the file size will be 1024 bytes, we keep sending until there is nothing
                        bytesToSend = f.read(1024)
                        connection.send(bytesToSend)

        else:
            connection.send("ERR".encode())

        connection.close()

    @property
    def portNumber(self):
        return self.__portNumber__
