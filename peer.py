from socket import *
import os , time
from server import Server
from jsonFileHandler import getDataAndRequestChunks
from md5_handler import *
from datetime import datetime


class Peer(Server):
    def __init__(self, name, *, portNumber=5001, allowConnection=False):
        super().__init__(portNumber)
       
        self.__peerName__ = name

        # incase we want to store peer data at the tracker without having to connect each time
        self.__peerID__ = None
        self.newPeer = True
        self.newConnectionsHandler = self.handleConnection
        self.extraOperations = [self.connect , self.sendBeats]

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
        elif(request [:3] == "REQ"):
            requestedFile = request[4:]
            self.sendFile(name , connection , f"Peers/{self.__peerName__}/Chunks/{requestedFile}")
            os.remove(f"Peers/{self.__peerName__}/Chunks/{requestedFile}")

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

    def requestFile(self, fileName , requestFromPeer = False):

        if fileName != "q":  # to quit
            self.tempSocket.send(f"REQ {fileName}".encode())
            data = self.tempSocket.recv(1024).decode()

            if data[:6] == "EXISTS":  # server tells us if the file exists and sedns the size
                isManifestFile = False
                information = data.split("--")
                filesize = int(information[1])
                requestedFileName = fileName
                recievedFileName = information[2].split("/")[-1]

                #the below indicates whether we have recieved a manifest file or not
                if requestedFileName != recievedFileName:
                    isManifestFile = True
                message = ""
                if not requestFromPeer:
                    message = input(f"File Exists , {filesize} Bytes. Download?(Y/N):\t")
                  
                if message.upper() == "Y" or requestFromPeer:
                    self.tempSocket.send("OK".encode())

                    dir = f"Peers/{self.__peerName__}/Downloads"
                    if not os.path.exists(dir):
                        os.makedirs(f"./{dir}")

                    newFile = open(f"{dir}/{recievedFileName}", "wb")
                    data = self.tempSocket.recv(1024)

                    totalReceived = len(data)
                    newFile.write(data)
                    while totalReceived < filesize:  # in case the file is bigger than 1024 bytes, we keep checking if the total recieved is equal to the actual file size
                        data = self.tempSocket.recv(1024)

                        totalReceived += len(data)
                        newFile.write(data)
                    newFile.close()

                    #if the file we got is a manifest file
                    if isManifestFile:
                        actual_MD5_OfFile = getDataAndRequestChunks(self.__peerName__, recievedFileName, self.requestChunks)

                        os.remove(f"{dir}/{recievedFileName}")

                        self.mergeFiles(requestedFileName)
                        time.sleep(1)
                        if compare_md5(actual_MD5_OfFile , convert_to_md5(f"Peers/{self.__peerName__}/Downloads/{requestedFileName}")):
                            print("Download Complete!")
                        else:
                            print("Download Failed.")
                
                  

            else:
                print("File does not exist!")

 
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

    def requestChunks(self, manifestFileName , port):
        self.connect(port = port , justGetID = False)
        self.requestFile(manifestFileName , requestFromPeer= True)


    
    def mergeFiles(self, requestFileName):

        fileList = os.listdir(f'./Peers/{self.__peerName__}/Downloads')
        fileList = list(filter(lambda file: file.startswith(f"{requestFileName.split('.')[0]}_"), fileList))
        # fileList.sort(key = len)
        print(fileList)

        for file in fileList:
            with open(f'./Peers/{self.__peerName__}/Downloads/{requestFileName}', 'ab') as total_file: 
                with open(f'./Peers/{self.__peerName__}/Downloads/{file}', 'rb') as chunk_file:
                    for line in chunk_file:
                        total_file.write(line)
            os.remove(f'./Peers/{self.__peerName__}/Downloads/{file}')
      
  
    def sendBeats(self):
        addr = ("127.0.0.1", 5500) #target tracker
        while True:
            self.UDP_socket =  socket(AF_INET, SOCK_DGRAM)
            dateTimeObj = datetime.now()
            timeStamp = f"{dateTimeObj.year}/{dateTimeObj.month}/{dateTimeObj.day}_{dateTimeObj.hour}:{dateTimeObj.minute}:{dateTimeObj.second}"
            message = f'PING|{self.__listeningPortNumber__}|{timeStamp}'.encode()
            self.UDP_socket.sendto(message, addr)
            time.sleep(15) #send a beat/ping every 15 seconds
        
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
    peer = Peer("nassar" , portNumber=5007)
    peer.start()
    


if __name__ == "__main__":
    Main()