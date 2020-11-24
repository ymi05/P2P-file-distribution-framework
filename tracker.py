from server import Server
from peer import Peer
from manifest import ManifestFile
from datetime import datetime
from timeChecker import timeLimitExceeded
import math , os , random , time , threading
import threading
from socket import *

class Tracker(Server):


    def __init__(self):
        super().__init__(5000 , isTracker= True)

        self.connectedPeers = {}
        self.beats_status = {}
        self.newConnectionsHandler = self.handlePeerArrival
        self.extraOperations = [self.checkForNewFiles , self.monitorUDPBeats]
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
        
        manifestFile = ManifestFile(fileName)
        manifestFile.prepareManifestFile(numberOfChunks)

        if len(self.beats_status) < numberOfChunks:
            numberOfChunks = len(self.beats_status)
        #the division could lead to a float , but the file can read # bytes that are integers.
        CHUNK_SIZE = math.ceil(os.path.getsize(
            f"Server_files/{fileName}") / numberOfChunks)     # We take the cieling of the divison result and not the floor to avoid losing data
        
        chunkNO = 1
        choshenReciver = None #we pick a certain receiver at certain points:
        #EXPLANATION:
        #in cases like 3 peers, if the first two chunks and their respective copies were sent to the same peers
        #the last peer will only be able to get only one chunk and this chunk will not have a copy at one of the peers

        with open(f"Server_files/{fileName}", "rb") as chosenFile:
            chosenPeersIDs = { id : 0 for id in self.beats_status} #used to keep track of the selected peers to avoid sending to the same peer more than once
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

             
                chosenIDs = []
                for i in range(2):
                    chosenPort = random.choice(list(self.beats_status))
                    if(len(chosenPeersIDs) != 1 or choshenReciver != None ):
                        while chosenPeersIDs[chosenPort] == 2 or chosenPort in chosenIDs or chosenPort == choshenReciver: #we set it to two so two peers could have a copy of the same file
                            chosenPort = random.choice(list(self.beats_status))
                    if(chunkNO % 2 != 0): #take one of the chosen peers, wait for the next new chunk to be sent
                        choshenReciver = chosenPort
                    elif(chunkNO % 2 == 0): # when we skip a chunk, we use the port and send the next chunk to it
                        choshenReciver = None
                    chosenPeersIDs[chosenPort] +=1
                    chosenIDs.append(chosenPort)

                    self.sendCunkToVolunteer(int(chosenPort), fileName) 
                    manifestFile.addChunkDetails(chunkNO , "127.0.0.1" , int(chosenPort))
               
             
               
                # manifestFile.addChunkDetails(chunkNO , "127.0.0.1" , self.connectedPeers[chosenPort].portNo)
                os.remove(f"DividedFiles/{fileName}")

                chunkNO += 1
        
            manifestFile.saveAsFile()
        
	        

    


    def deleteFile(self , fileName):
        filePath = f"Server_files/{fileName}"
        if os.path.exists(filePath):
            self.divideFileToChunks(fileName , len(self.beats_status))
            os.remove(filePath)
    
   
    def checkForNewFiles(self):
        while True:
            if len(self.beats_status) > 0:
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

    

    def monitorUDPBeats(self):
        self.UDP_socket = socket(AF_INET , SOCK_DGRAM)
        self.UDP_socket.bind(('', 5500)) #create a seperate socket with a different port to listen to the UPD heartbeats
        while True:
            try:
                checkerThread = threading.Thread(target=self.checkPeerStatus)  #
                checkerThread.start()
                listeningThread = threading.Thread(target=self.listenToBeats) 
                
                listeningThread.start()
                time.sleep(2) 
            
            except :
                print("Cannot listen to beats anymore")
                break
        self.UDP_socket.close()
    
    def updatePeerStatus(self , address , portNo,  timeStamp):
        self.beats_status[portNo] = timeStamp #we keep track of the peers by saving their ports along with the timestamp of the last beat

    def listenToBeats(self):
        message, address = self.UDP_socket.recvfrom(1024)    
        messageContent = message.decode().split("|")
        timeStamp = messageContent[2]
        portNo = messageContent[1]
        print(f"UDP Beat from < port: {portNo} >")
     
        self.updatePeerStatus( address , portNo,  timeStamp)

    def checkPeerStatus(self):
        if len(self.beats_status) > 0: #no need to check if we have nothing stored
            dateTimeObj = datetime.now()
            current_Statuses = self.beats_status.copy() #the dict size might change while looping so this will cause an error
            timeLimit_seconds = 30 #if we do not receive a beat within 30 seconds, tracker will remove the peer
            for port in current_Statuses:
                timeStamp = current_Statuses[port].split("_")[1]


                if timeLimitExceeded( timeStamp , dateTimeObj , port):
                    print(f"No more beats from port: {port}")
                    self.handlePeerChurn(port)
                    self.beats_status.pop(port) #if there are no beats for the specific port, then remove it from the dict

    def handlePeerChurn(self , portNo):
        pass

def Main():
    server = Tracker()
    server.start()

if __name__ == "__main__":
    Main()
