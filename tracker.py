from server import Server


class Tracker(Server):
    trackerCounter = 0

    def __init__(self):
        super().__init__(5000)
        self.trackerID = Tracker.trackerCounter
        Tracker.trackerCounter += 1
        self.peerArray = []
        self.manifestFile = None
        self.trackerSocket = None
        self.newConnectionsHandler = self.handleNewPeerArrival

    def handleNewPeerArrival(self, name, connection):
        resp = connection.recv(1024).decode()
        if(resp[:3] == "NEW"):
            self.peerArray.append(connection)
            connection.send(f"{(len(self.peerArray)-1)}".encode())
        else:
            self.sendFile(self, connection, resp)

    def sendManifestFile(self, volunteerID):
        pass

    def deleteFile(self, fileName):
        pass

    def sendChunksToVolunteer(self, data):
        pass


def Main():
    server = Tracker()
    server.runServer()


if __name__ == "__main__":
    Main()
