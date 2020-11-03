from socket import *
import os
from server import Server


class Peer(Server):
    peerCounter = 0

    def __init__(self, name):
        self.__peerName__ = name
        self.fileChunksSaved = None
        self.peerSocket = None

        self.__peerID__ = self.getIDFromServer()

    def getIDFromServer(self) -> int:
        self.connect()
        self.peerSocket.send(f"NEW {self.__peerName__}".encode())
        peerID = self.peerSocket.recv(1024).decode()
        self.peerSocket.close()
        return peerID

    def connect(self, host="127.0.0.1", port=5000):
        self.peerSocket = socket(AF_INET, SOCK_STREAM)
        self.peerSocket.connect((host, port))

    def requestFile(self, fileName):

        if fileName != "q":  # to quit
            self.peerSocket.send(fileName.encode())
            data = self.peerSocket.recv(1024).decode()

            if data[:6] == "EXISTS":  # server tells us if the file exists and sedns the size
                filesize = int(data[6:])
                message = input(
                    f"File Exists , {filesize} Bytes. Download?(Y/N)")

                if message.upper() == "Y":
                    self.peerSocket.send("OK".encode())

                    dir = f"Client_downloads/{self.__peerName__}"
                    if os.path.isdir(dir) == False:
                        os.mkdir(dir)

                    newFile = open(f"{dir}/new_{fileName}", "wb")
                    data = self.peerSocket.recv(1024)

                    totalReceived = len(data)
                    newFile.write(data)
                    while totalReceived < filesize:  # in case the file is bigger than 1024 bytes, we keep checking if the total recieved is equal to the actual file size
                        data = self.peerSocket.recv(1024)

                        totalReceived += len(data)
                        newFile.write(data)

                    newFile.close()
                    print("Download Complete")

            else:
                print("File does not exist!")

    def sendChunks(self, requestedFileChunks):
        pass

    def leaveNetwork(self):
        pass

    def joinNetwork(self):
        pass

    @property
    def id(self):  # use this to directly return a property instead of creating a getter function
        return self.__peerID__

    @property
    def name(self):
        return self.__peerName__
