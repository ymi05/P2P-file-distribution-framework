from socket import *
import time
import threading
from datetime import datetime









def updatePeerStatus(address , portNo,  timeStamp):
    connectedPeers_Status[portNo] = timeStamp


def checkPeerStatus():
    if len(connectedPeers_Status) > 0:
        dateTimeObj = datetime.now()
        current_Statuses = connectedPeers_Status.copy() #the dict size might change while looping so this will cause an error
        for port in current_Statuses:
            lastRecieved_hour = int(current_Statuses[port].split("_")[1].split(":")[0])
            lastRecieved_minute =  int(current_Statuses[port].split("_")[1].split(":")[1])
            lastRecieved_second = int(current_Statuses[port].split("_")[1].split(":")[2])

            if  (int(dateTimeObj.minute) > lastRecieved_minute or lastRecieved_second + 30 <= int(dateTimeObj.second)) and int(dateTimeObj.hour) >= lastRecieved_hour:
                print(f"Connection with port {port} is dead")
                connectedPeers_Status.pop(port)


def listenToBeats():
    message, address = listeningSocket.recvfrom(1024)    
    print(f"Client connected IP < {address} >")
    messageContent = message.decode().split("|")
    timeStamp = messageContent[2]
    portNo = messageContent[1]
    updatePeerStatus( address , portNo,  timeStamp)












connectedPeers_Status = {}
listeningSocket = socket(AF_INET , SOCK_DGRAM)
listeningSocket.bind(('', 5000))

while True:
    try:
        checkerThread = threading.Thread(target=checkPeerStatus) 
        checkerThread.start()
        listeningThread = threading.Thread(target=listenToBeats) 
        
        listeningThread.start()
        time.sleep(2)
       
    except :
        break
    

listeningSocket.close()
