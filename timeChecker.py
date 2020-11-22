
from datetime import datetime

def timeLimitExceeded(timeStamp , currentTime: datetime , portNo):
    timeLimit = 30

    lastRecieved_hour = int(timeStamp.split(":")[0]) * 120
    lastRecieved_minute =  int(timeStamp.split(":")[1]) * 60
    lastRecieved_second = int(timeStamp.split(":")[2])

    currentHr = int(currentTime.hour) * 120
    currentMin = int(currentTime.minute) * 60
    currentSec = int(currentTime.second)

    prevTime_inSeconds = lastRecieved_hour + lastRecieved_minute + lastRecieved_second
    currentTime_inSeconds = currentHr + currentMin + currentSec
    difference = abs(prevTime_inSeconds - currentTime_inSeconds)

    if difference%15 == 0 and difference != 0: 
        print(f"{difference} seconds have passed since the last beat from {portNo}")
    

    return True if difference >= timeLimit else False


# print(timeLimitExceeded("3:0:0" , datetime.now()))