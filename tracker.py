from server import Server
from peer import Peer
import math , os , random

class Tracker(Server):
    trackerCounter = 0

    def __init__(self):
        super().__init__(5000)
        self.trackerID = Tracker.trackerCounter
        Tracker.trackerCounter += 1
        self.connectedPeers = {}
        self.newConnectionsHandler = self.handlePeerArrival
        self.filesLimit = 3

    def handlePeerArrival(self, name, connection):
        request = connection.recv(1024)
        request = request.decode()
        print(F"Incoming Request: {request}")

        if(request[:3] == "NEW"):  # NEW command is for new peers connecting to the server
            peerID = (len(self.connectedPeers)+1)
            connection.send(f"{peerID}".encode())
            information = request[5:].split(":")
            # we save the information of the new peer and store a Peer object inside the dirctionary
            self.connectedPeers[peerID] = Peer(str(information[0]),
                                               portNumber=int(information[1]))

        elif(request[:3] == "REQ"):  # REQ command is for requesting a file
            self.sendFile(self, connection, f"./Server_files/{request[4:]}")

    def sendManifestFile(self, volunteerAddress):
        pass

   

    def sendCunkToVolunteer(self, portNo, fileName):

        self.establishTCPConnection(portNo)
        self.__socket__.send(f"SAVE|{os.path.getsize(f'./DividedFiles/{fileName}')}|{fileName}".encode())
        peerResponse = self.__socket__.recv(1024).decode()
        if peerResponse[:2] == "OK":
            with open(f"DividedFiles/{fileName}", "rb") as fileChunk:
                bytesToSend = fileChunk.read(1024)
                self.__socket__.send(bytesToSend)
                while bytesToSend != b'':  
                    bytesToSend = fileChunk.read(1024)
                    self.__socket__.send(bytesToSend)

        self.__socket__.close()

    
  
    def divideFileToChunks(self, fileName, numberOfChunks = 2):
        #the division could lead to a float , but we the file can read # bytes that are integers.
        self.connectedPeers = {"1":Peer("Youssef" , portNumber=5003) , "2":Peer("Adam" , portNumber=5002)}
        if len(self.connectedPeers) < numberOfChunks:
            numberOfChunks = len(self.connectedPeers)

        CHUNK_SIZE = math.ceil(os.path.getsize(
            f"Server_files/{fileName}") / numberOfChunks)     # We take the cieling of the divison result and no the floor to avoid losing data

        chunkNO = 1
        with open(f"Server_files/{fileName}", "rb") as chosenFile:
            chosenPeersIDs = [] #used to keep track of the selected peers to avoid sending to the same peer more than once
            newFileName = fileName.split('.')[0]
            while (newChunk:= chosenFile.read(CHUNK_SIZE)) != b'': #if what we read is not empty then we assign what was read to newChunk
                if chunkNO > numberOfChunks:
                    break

                
                fileExtention = fileName.split('.')[1]
                fileName = f"{newFileName}_chunk{chunkNO}.{fileExtention}"
                with open(f"DividedFiles/{fileName}", "wb") as fileChunk:
                    fileChunk.write(newChunk)

                
                chosenID = random.choice(list(self.connectedPeers))
                while chosenID in chosenPeersIDs:
                    chosenID = random.choice(list(self.connectedPeers))
                chosenPeersIDs.append(chosenID)
             
                self.sendCunkToVolunteer(int(self.connectedPeers[chosenID].portNumber), fileName) 
                os.remove(f"DividedFiles/{fileName}")

                chunkNO += 1
  


    def deleteFile(self , fileName):
        filePath = f"Server_files/{fileName}"
        if os.path.exists(filePath):
            self.divideFileToChunks(fileName)
            os.remove(filePath)
    
    def addFile(self , filePath):
        newData = ""
        print(filePath)
        with open(filePath , "rb") as chosenFile:
            newData = chosenFile.read() 
        fileName = filePath.split("/")[2]



        with open(f"Server_files/{fileName}" , "wb") as newFile:
            fileList = os.listdir('./Server_files')
            if(len(fileList) >= self.filesLimit):
                self.deleteFile(random.choice(fileList))
            newFile.write(newData)
            


def Main():
    server = Tracker()
    # server.runServer()
    trackerObj = Tracker()
    # trackerObj.deleteFile("app.txt")
    fileList = os.listdir('./random_files')
    for file in fileList:
        trackerObj.addFile(f"./random_files/{file}")


if __name__ == "__main__":
    Main()
