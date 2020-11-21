
from datetime import datetime
dateTimeObj = datetime.now()
print(dateTimeObj.year, '/', dateTimeObj.month, '/', dateTimeObj.day)
print(dateTimeObj.hour, ':', dateTimeObj.minute, ':', dateTimeObj.second)


timeStamp = f"{dateTimeObj.hour}:{dateTimeObj.minute}:{dateTimeObj.second}"

print(timeStamp < f"{12}:{5}:{dateTimeObj.second}")


