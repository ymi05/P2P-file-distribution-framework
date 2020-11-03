from server import Server
from peer import Peer


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
        if(request[:3] == "NEW"):  # NEW code is for new peers connecting to the server
            peerID = (len(self.connectedPeers))
            connection.send(f"{peerID}".encode())
            information = request[8:].split(":")
            # we save the information of the new peer and store a Peer object inside the dirctionary
            self.connectedPeers[peerID] = Peer(str(information[0]),
                                               portNumber=int(information[1]))

        elif(request[:3] == "REQ"):  # REQ command is for requesting a file
            self.sendFile(self, connection, request[4:])

    def sendManifestFile(self, volunteerAddress):
        pass

    def deleteFile(self, fileName):
        pass

    def sendChunksToVolunteer(self, volunteerAddress, data):
        pass


def Main():
    server = Tracker()
    server.runServer()


if __name__ == "__main__":
    Main()
