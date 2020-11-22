
from datetime import datetime

def timeLimitExceeded(timeStamp , currentTime: datetime):
    lastRecieved_hour = int(timeStamp.split(":")[0]) * 120
    lastRecieved_minute =  int(timeStamp.split(":")[1]) * 60
    lastRecieved_second = int(timeStamp.split(":")[2])

    currentHr = int(currentTime.hour)
    currentMin = int(currentTime.minute)
    currentSec = int(currentTime.second)

    prevTime_inSeconds = lastRecieved_hour + lastRecieved_minute + lastRecieved_second
    currentTime_inSeconds = currentHr + currentMin + currentSec
    difference = abs(prevTime_inSeconds - currentTime_inSeconds)
    print(difference)
    return True if difference >= 30 else False


print(timeLimitExceeded("3:0:0" , datetime.now()))