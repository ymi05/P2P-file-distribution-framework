class Peer():
    peerCounter = 0

    def __init__(self, name):
        self.peerID = peerCounter
        Peer.peerCounter += 1
        self.name = name
        self.fileChunksSaved = None
        self.network = None

    def requestFile(self):
        pass

    def sendChunks(self, requestedFileChunks):
        pass

    def leaveNetwork(self):
        pass

    def joinNetwork(self):
        pass
