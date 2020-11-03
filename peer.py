from socket import *
import os
from server import Server


class Peer(Server):
    peerCounter = 0

    def __init__(self, name, allowConnection=False, *, portNumber=None):
        self.__peerName__ = name
        self.fileChunksSaved = None

        self.__portNumber__ = portNumber
        # incase we want to store peer data at the tracker without having to connect each time
        self.__peerID__ = self.getIDFromServer() if allowConnection else -1

    def getIDFromServer(self) -> int:
        self.connect()
        self.__socket__.send(f"NEW {self.__peerName__}".encode())
        peerID = self.__socket__.recv(1024).decode()
        self.__socket__.close()
        return peerID

    def connect(self, host="127.0.0.1", port=5000):
        self.__socket__ = socket(AF_INET, SOCK_STREAM)
        self.__socket__.connect((host, port))

    def requestFile(self, fileName):

        if fileName != "q":  # to quit
            self.__socket__.send(fileName.encode())
            data = self.__socket__.recv(1024).decode()

            if data[:6] == "EXISTS":  # server tells us if the file exists and sedns the size
                filesize = int(data[6:])
                message = input(
                    f"File Exists , {filesize} Bytes. Download?(Y/N)")

                if message.upper() == "Y":
                    self.__socket__.send("OK".encode())

                    dir = f"Client_downloads/{self.__peerName__}"
                    if os.path.isdir(dir) == False:
                        os.mkdir(dir)

                    newFile = open(f"{dir}/new_{fileName}", "wb")
                    data = self.__socket__.recv(1024)

                    totalReceived = len(data)
                    newFile.write(data)
                    while totalReceived < filesize:  # in case the file is bigger than 1024 bytes, we keep checking if the total recieved is equal to the actual file size
                        data = self.__socket__.recv(1024)

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
