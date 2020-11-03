from socket import *
import os
from server import Server


class Peer(Server):
    def __init__(self, name, *, portNumber=None, allowConnection=False):
        super().__init__(5001)
        self.__peerName__ = name

        # incase we want to store peer data at the tracker without having to connect each time
        self.__peerID__ = None
        self.fileChunksSaved = None
        self.newPeer = True

    def setIDFromServer(self):
        # get the port number of the socket and assign it to this peer
        self.__portNumber__ = self.__socket__.getsockname()[1]
        self.__socket__.send(
            f"NEW {self.__peerName__}:{self.__portNumber__}".encode())  # send the port number along with the name
        self.__peerID__ = self.__socket__.recv(
            1024).decode()  # get your ID from the tracker
        self.newPeer = False
        self.__socket__.close()

    def connect(self, host="127.0.0.1", port=5000):

        if(self.newPeer):
            self.__socket__ = socket(AF_INET, SOCK_STREAM)
            self.__socket__.connect((host, port))
            self.setIDFromServer()

        if(not self.newPeer):
            self.__socket__ = socket(AF_INET, SOCK_STREAM)
            self.__socket__.connect((host, port))

    def requestFile(self, fileName):

        if fileName != "q":  # to quit
            self.__socket__.send(f"REQ {fileName}".encode())
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
