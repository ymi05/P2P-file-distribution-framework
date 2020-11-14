from socket import *
import os , time
from server import Server


class Peer(Server):
    def __init__(self, name, *, portNumber=5001, allowConnection=False):
        super().__init__(portNumber)
       
        self.__peerName__ = name

        # incase we want to store peer data at the tracker without having to connect each time
        self.__peerID__ = None
        self.newPeer = True
        self.newConnectionsHandler = self.handleConnection
        self.extraOperationsHandler = self.connect

    def handleConnection(self , name , connection):
        request = connection.recv(1024)
        request = request.decode()
        print(request)
        if(request[:3] == "NEW"):  # NEW command is for new peers connecting to the server
            peerID = (len(self.connectedPeers)+1)
            connection.send(f"{peerID}".encode())
            information = request[5:].split(":")
            # we save the information of the new peer and store a Peer object inside the dirctionary
            self.connectedPeers[peerID] = Peer(str(information[0]),
                                               portNumber=int(information[1]))

        elif(request[:4] == "SAVE"):  # REQ command is for requesting a file
            information = request.split("|")
            fileSize = int(information[1])
            fileName = information[2]
            self.saveChunk(fileName,fileSize , connection)

    def getIDFromServer(self):
        # get the port number of the socket and assign it to this peer

        time.sleep(1)
        self.tempSocket.send(
            f"NEW {self.__peerName__}:{self.__listeningPortNumber__}".encode())  # send the port number along with the name
      
        self.__peerID__ = self.tempSocket.recv(1024).decode()  # get your ID from the tracker
        
        self.newPeer = False
        self.tempSocket.close()

    def connect(self, host="127.0.0.1", port=5000 , justGetID = True):

        if(self.newPeer) or justGetID:
            self.tempSocket = self.establishTCPConnection(port)
            self.getIDFromServer()

        if(not self.newPeer) and not justGetID:
           self.tempSocket = self.establishTCPConnection(port)

    def requestFile(self, fileName):

        if fileName != "q":  # to quit
            self.tempSocket.send(f"REQ {fileName}".encode())
            data = self.tempSocket.recv(1024).decode()

            if data[:6] == "EXISTS":  # server tells us if the file exists and sedns the size
                filesize = int(data[6:])
                message = input(f"File Exists , {filesize} Bytes. Download?(Y/N):\t")

                if message.upper() == "Y":
                    self.tempSocket.send("OK".encode())

                    dir = f"Peers/{self.__peerName__}/Downloads"
                    if not os.path.exists(dir):
                        os.makedirs(f"./{dir}")

                    newFile = open(f"{dir}/new_{fileName}", "wb")
                    data = self.tempSocket.recv(1024)

                    totalReceived = len(data)
                    newFile.write(data)
                    while totalReceived < filesize:  # in case the file is bigger than 1024 bytes, we keep checking if the total recieved is equal to the actual file size
                        data = self.tempSocket.recv(1024)

                        totalReceived += len(data)
                        newFile.write(data)

                    newFile.close()
                    print("Download Complete!")

            else:
                print("File does not exist!")

    def sendChunks(self, requestedFileChunks):
        pass

    def saveChunk(self , fileName , fileSize, connection):
        connection.send("OK".encode())
        dir = f"Peers/{self.__peerName__}/Chunks"
        if not os.path.exists(dir):
      
            os.makedirs(f"./{dir}")

        with open(f"{dir}/{fileName}", "wb") as newChunk:

            data = connection.recv(1024)

            totalReceived = len(data)
            newChunk.write(data)
            while totalReceived < fileSize:  # in case the file is bigger than 1024 bytes, we keep checking if the total recieved is equal to the actual file size
                data = connection.recv(1024)

                totalReceived += len(data)
                newChunk.write(data) 

    def joinNetwork(self):
        pass

    @staticmethod
    def mergeFiles(requestFileName):

        fileList = os.listdir('./DividedFiles/')
        fileList = list(filter(lambda file: file.startswith(f"{requestFileName.split('.')[0]}_chunk_"), fileList))
        fileList.sort(key = len)
        print(fileList)

        for file in fileList:
            with open(requestFileName, 'ab') as total_file: 
                with open(f"DividedFiles/{file}", 'rb') as chunk_file:
                    for line in chunk_file:
                        total_file.write(line)
    
    @property
    def id(self):  # use this to directly return a property instead of creating a getter function
        return self.__peerID__

    @property
    def name(self):
        return self.__peerName__
    
    @property
    def portNo(self):
        return self.__listeningPortNumber__

    


def Main():
    peer = Peer("Adam" , portNumber=5004)
    # peer.start()
    peer.start()
    


if __name__ == "__main__":
    Main()