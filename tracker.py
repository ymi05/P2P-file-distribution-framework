from server import Server
from peer import Peer
import math , os

class Tracker(Server):
    trackerCounter = 0

    def __init__(self):
        super().__init__(5000)
        self.trackerID = Tracker.trackerCounter
        Tracker.trackerCounter += 1
        self.connectedPeers = {}
        self.manifestFile = None
        self.newConnectionsHandler = self.handlePeerArrival

    def handlePeerArrival(self, name, connection):
        request = connection.recv(1024)
        request = request.decode()
        print(request)
        if(request[:3] == "NEW"):  # NEW command is for new peers connecting to the server
            peerID = (len(self.connectedPeers)+1)
            connection.send(f"{peerID}".encode())
            information = request[8:].split(":")
            # we save the information of the new peer and store a Peer object inside the dirctionary
            self.connectedPeers[peerID] = Peer(str(information[0]),
                                               portNumber=int(information[1]))

        elif(request[:3] == "REQ"):  # REQ command is for requesting a file
            self.sendFile(self, connection, request[4:])

    def sendManifestFile(self, volunteerAddress):
        pass

   

    def sendCunkToVolunteer(self, volunteerAddress, data):
        pass
    
  
    def divideFileToChunks(self, fileName, numberOfChunks = 1):
        #the division could lead to a float , but we the file can read # bytes that are integers.
        CHUNK_SIZE = math.ceil(os.path.getsize(
            f"Server_files/{fileName}") / numberOfChunks)     # We take the cieling of the divison result and no the floor to avoid losing data

        chunkNO = 1
        with open(f"Server_files/{fileName}", "rb") as chosenFile:
            
            while (newChunk:= chosenFile.read(CHUNK_SIZE)) != b'': #if what we read is not empty then we assign what was read to newChunk
                if chunkNO > numberOfChunks:
                    break
      
                with open(f"DividedFiles/{fileName.split('.')[0]}_chunk_{chunkNO}.{fileName.split('.')[1]}", "wb") as fileChunk:
                    fileChunk.write(newChunk)

                with open(f"DividedFiles/{fileName.split('.')[0]}_chunk_{chunkNO}.{fileName.split('.')[1]}", "rb") as fileChunk:
                    self.sendCunkToVolunteer(self.connectedPeers[chunkNO] , fileChunk) 

                chunkNO += 1
  

    @staticmethod
    def deleteFile(fileName):
        Tracker.divideFileToChunks(fileName)
        pass

def Main():
    server = Tracker()
    server.runServer()


if __name__ == "__main__":
    Main()
