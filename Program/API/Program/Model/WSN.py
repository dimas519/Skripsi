class WSN:
    def __init__(self, identifier:str, token:str 
                 ,offsetHour:int, offsetMinutes:int 
                 ,sensorType:list, latitude:str
                 ,longtitude:str, kota:str
                 ,queue:dict):
       
       
       
       
        self.identifier=identifier
        self.token=token
        self.offsetHour=offsetHour
        self.offsetMinutes=offsetMinutes
        self.sensorType=sensorType
        self.latitude=latitude
        self.longtitude=longtitude
        self.kota=kota
        self.queue=queue


    def setSensingTable(self, sensingTable):
        self.sensingTable=sensingTable

    def setQueue(self, queue):
        self.queue=queue






    def getIdentifier(self):
        return self.identifier

    def getToken(self):
        return self.token
    
    def getOffsetHour(self):
        return self.offsetHour
    
    def getOffsetMinutes(self):
        return self.offsetMinutes
    
    def getSensorType(self):
        return self.sensorType
    
    def getSensingTable(self):
        return self.sensingTable
    
    def getLangtitude(self):
        return self.latitude
    
    def getLongtitude(self):
        return self.longtitude
    
    def getKota(self):
        return self.kota
    
    def getQueue(self):
        return self.queue