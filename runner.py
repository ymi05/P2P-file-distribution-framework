from tracker import Tracker
from peer import runPeer
import threading , time



def Main():
    trackerServer = Tracker()
    
    trackerThread =  threading.Thread(target=trackerServer.start) 
    trackerThread.start()
    time.sleep(5)
    peerNames = ["Youssef" , "Adam"]
    intialPeerPort = 5004
    
    for name in peerNames:
        peerThread = threading.Thread(target=runPeer, 
                                 args=(name, intialPeerPort)) 
           
        intialPeerPort +=1
        peerThread.start()
    

if __name__ == '__main__':
    Main()

