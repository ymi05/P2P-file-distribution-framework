from socket import *
import time
from datetime import datetime



clientSocket = socket(AF_INET, SOCK_DGRAM)

#Set a timeout value of 1 second
# clientSocket.settimeout(1)

#Ping to server


addr = ("127.0.0.1", 5000)

#Send ping
# start = time.time()
# for i in range(5):
    # time.sleep(3)
dateTimeObj = datetime.now()
timeStamp = f"{dateTimeObj.year}/{dateTimeObj.month}/{dateTimeObj.day}_{dateTimeObj.hour}:{dateTimeObj.minute}:{dateTimeObj.second}"
message = f'PING|5005|{timeStamp}'.encode()
clientSocket.sendto(message, addr)