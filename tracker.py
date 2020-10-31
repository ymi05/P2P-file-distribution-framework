class Tracker():
    trackerCounter = 0

    def __init__(self):
        self.trackerID = trackerCounter
        Tracker.trackerCounter += 1
        self.manifestFile = None

    def fileExists(self, fileName):
        pass

    def sendManifestFile(self, volunteerID):
        pass

    def sendFile(self, fileName, volunteerID):
        pass

    def deleteFile(self, fileName):
        pass

    def sendChunksToVolunteer(self, data):
        pass
