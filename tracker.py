from server import Server
from peer import Peer
from manifest import ManifestFile
import math , os , random , time 

class Tracker(Server):


    def __init__(self):
        super().__init__(5000 , isTracker= True)

        self.connectedPeers = {}
        self.newConnectionsHandler = self.handlePeerArrival
        self.extraOperationsHandler = self.checkForNewFiles
        self.fileLimit = 3

    def handlePeerArrival(self, name, connection):
        request = connection.recv(1024)
        request = request.decode()
        print(F"Incoming Request: {request}")

        if(request[:3] == "NEW"):  # NEW command is for new peers connecting to the server
            peerID = (len(self.connectedPeers)+1)
            connection.send(f"{peerID}".encode())
            information = request[4:].split(":")
            # we save the information of the new peer and store a Peer object inside the dirctionary
            self.connectedPeers[peerID] = Peer(str(information[0]),
                                               portNumber=int(information[1]))

        elif(request[:3] == "REQ"):  # REQ command is for requesting a file
            requestedFile = request[4:]
            if Server.fileExists(f"Server_files/{requestedFile}"):
                self.sendFile("",connection, f"./Server_files/{requestedFile}")

            elif Tracker.manifestExists(requestedFile):
                self.sendManifestFile(connection , requestedFile)
            else:
                connection.send("ERR".encode())
            connection.close()

        for peer in self.connectedPeers:
            print(f"Name: {self.connectedPeers[peer].name} - Port: {self.connectedPeers[peer].portNo}")
            


   

    def sendCunkToVolunteer(self, portNo, fileName):

        self.tempSocket = self.establishTCPConnection(portNo)
        if self.tempSocket != None:
            time.sleep(3)
            self.tempSocket.send(f"SAVE|{os.path.getsize(f'./DividedFiles/{fileName}')}|{fileName}".encode())
            peerResponse = self.tempSocket.recv(1024).decode()
            if peerResponse[:2] == "OK":
                with open(f"DividedFiles/{fileName}", "rb") as fileChunk:
                    bytesToSend = fileChunk.read(1024)
                    self.tempSocket.send(bytesToSend)
                    while bytesToSend != b'':  
                        bytesToSend = fileChunk.read(1024)
                        self.tempSocket.send(bytesToSend)

            self.tempSocket.close()


    
  
    def divideFileToChunks(self, fileName, numberOfChunks = 1):
     
        # self.connectedPeers = {"1":Peer("Youssef" , portNumber=5003) , "2":Peer("Adam" , portNumber=5002)} #hardcoded values
        
        manifestFile = ManifestFile(f"Server_files/{fileName}")
        manifestFile.prepareManifestFile(numberOfChunks)

        if len(self.connectedPeers) < numberOfChunks:
            numberOfChunks = len(self.connectedPeers)
        #the division could lead to a float , but the file can read # bytes that are integers.
        CHUNK_SIZE = math.ceil(os.path.getsize(
            f"Server_files/{fileName}") / numberOfChunks)     # We take the cieling of the divison result and not the floor to avoid losing data

        chunkNO = 1
        with open(f"Server_files/{fileName}", "rb") as chosenFile:
            chosenPeersIDs = { id : 0 for id in self.connectedPeers} #used to keep track of the selected peers to avoid sending to the same peer more than once
            newFileName = fileName.split('.')[0]
            while (newChunk:= chosenFile.read(CHUNK_SIZE)) != b'': #if what we read is not empty then we assign what was read to newChunk
                if chunkNO > numberOfChunks: #in case things go bad
                    break

                
                fileExtention = fileName.split('.')[1]
                fileName = f"{newFileName}_chunk{chunkNO}.{fileExtention}"

                if not os.path.exists("DividedFiles"):
                    os.makedirs(f"./DividedFiles")

                with open(f"DividedFiles/{fileName}", "wb") as fileChunk:
                    fileChunk.write(newChunk)

             
                for i in range(2):
                    chosenIDs = []
                    chosenID = random.choice(list(self.connectedPeers))

                    while chosenPeersIDs[chosenID] == 2 and chosenID not in chosenIDs: #we set it to two so two peers could have a copy of the same file
                        chosenID = random.choice(list(self.connectedPeers))

                    chosenPeersIDs[chosenID] +=1
                    chosenIDs.append(chosenID)
                    self.sendCunkToVolunteer(int(self.connectedPeers[chosenID].portNo), fileName) 
               
             
               
                
                manifestFile.addChunkDetails(chunkNO , "127.0.0.1" , self.connectedPeers[chosenID].portNo)
                os.remove(f"DividedFiles/{fileName}")

                chunkNO += 1
        
            manifestFile.saveAsFile()
        
	        

    


    def deleteFile(self , fileName):
        filePath = f"Server_files/{fileName}"
        if os.path.exists(filePath):
            self.divideFileToChunks(fileName , len(self.connectedPeers))
            os.remove(filePath)
    
   
    def checkForNewFiles(self):
        while True:
            if len(self.connectedPeers) > 0:
                fileList = os.listdir('./Server_files')
                if(len(fileList) > self.fileLimit):
                    self.deleteFile(random.choice(fileList))
            # else:
            #     time.sleep(10)

    @staticmethod
    def getManifestFileName(fileName):
        fileName = fileName.split('.')[0]
        manifestFileName = fileName + "_manifest.json"
        return manifestFileName
    
    @staticmethod
    def manifestExists(fileName):
        return Server.fileExists(f"Manifests/{Tracker.getManifestFileName(fileName)}")
        
    def sendManifestFile(self, connection , fileName):
        fileName = Tracker.getManifestFileName(fileName)
        filePath =  f"Manifests/{fileName}"
        print(filePath)
        self.sendFile("" , connection , filePath)


def Main():
    server = Tracker()
    server.start()
    # trackerObj = Tracker()
    # # trackerObj.deleteFile("app.txt")
    # fileList = os.listdir('./random_files')
    # for file in fileList:
    #     trackerObj.addFile(f"./random_files/{file}")


if __name__ == "__main__":
    Main()
