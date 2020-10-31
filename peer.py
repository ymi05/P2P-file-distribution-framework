from socket import *


class Peer():
    peerCounter = 0

    def __init__(self, name):
        self.__peerID__ = Peer.peerCounter
        Peer.peerCounter += 1
        self.__peerName__ = name
        self.fileChunksSaved = None
        self.peerSocket = None
        self.network = None

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

                if message == "Y":
                    self.peerSocket.send("OK".encode())
                    f = open(f"Client_downloads/new_{fileName}", "wb")
                    data = self.peerSocket.recv(1024)

                    totalReceived = len(data)
                    f.write(data)
                    while totalReceived < filesize:  # in case the file is bigger than 1024 bytes, we keep checking if the total recieved is equal to the actual file size
                        data = self.peerSocket.recv(1024)

                        totalReceived += len(data)
                        f.write(data)
                        print("{0:.2f").format(
                            (totalReceived / float(filesize) * 100) + "%Done")
                    f.close()
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
    def id(self):
        return self.__peerID__

    @property
    def name(self):
        return self.__peerName__
