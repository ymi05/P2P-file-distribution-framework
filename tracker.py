from socket import *
import threading
import os


class Tracker():
    trackerCounter = 0

    def __init__(self):
        self.trackerID = Tracker.trackerCounter
        Tracker.trackerCounter += 1
        self.manifestFile = None
        self.trackerSocket = None

    def setSocket(self, host="127.0.0.1", port=5000):
        self.trackerSocket = socket(AF_INET, SOCK_STREAM)
        self.trackerSocket.bind((host, port))
        self.trackerSocket.listen(5)
        self.runServer()

    def runServer(self):
        print("Server started.")
        while True:
            connection, addr = self.trackerSocket.accept()
            print(f"Client connected IP < {addr} >")
            t = threading.Thread(target=self.sendFile,
                                 args=("sendingThread", connection))  # runs send file for each connection
            t.start()
        self.trackerSocket.close()

    @staticmethod
    def fileExists(fileName):
        return os.path.isfile(fileName)

    def sendManifestFile(self, volunteerID):
        pass

    def sendFile(self, name,  connection):
        fileName = connection.recv(1024)
        if Tracker.fileExists(fileName):
            connection.send(f"EXISTS {os.path.getsize(fileName)}".encode())
            userResponse = connection.recv(1024).decode()
            if userResponse[:2] == "OK":
                with open(fileName, 'rb') as f:  # we read the file as bytes
                    bytesToSend = f.read(1024)
                    connection.send(bytesToSend)
                    while bytesToSend != "":  # since we cannot garuntee that the file size will be 1024 bytes, we keep sending until there is nothing
                        bytesToSend = f.read(1024)
                        connection.send(bytesToSend)

        else:
            connection.send("ERR".encode())

        connection.close()

    def deleteFile(self, fileName):
        pass

    def sendChunksToVolunteer(self, data):
        pass


def Main():
    server = Tracker()
    server.setSocket()


if __name__ == "__main__":
    Main()
