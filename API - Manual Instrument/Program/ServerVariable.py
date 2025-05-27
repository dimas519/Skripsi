from datetime import datetime as DateTime
from datetime import timezone
from datetime import timedelta
from OTEL.DT_OTEL_Manual import *


tracer = get_tracer_provider().get_tracer(__name__) ##add this

def getTime(offsetHour=0,offsetMinutes=0):
    with tracer.start_as_current_span("getTime()") as span:
        utcTime=DateTime.now(timezone.utc)
        localtime=utcTime+timedelta(hours=offsetHour,minutes=offsetMinutes)
        result=localtime.strftime("%Y-%m-%d %H:%M:%S")
        return result  