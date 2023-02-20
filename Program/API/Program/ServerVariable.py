from datetime import datetime as DateTime
from datetime import timezone
from datetime import timedelta

def getTime(offsetHour=0,offsetMinutes=0):
    utcTime=DateTime.now(timezone.utc)
    localtime=utcTime+timedelta(hours=offsetHour,minutes=offsetMinutes)
    result=localtime.strftime("%Y-%m-%d %H:%M:%S")
    return result  