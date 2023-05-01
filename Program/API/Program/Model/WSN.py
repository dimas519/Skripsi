class WSN:
    def __init__(self, identifier:str, token:str 
                 ,offsetHour:int, offsetMinutes:int 
                 ,sensorType:list, interval:int
                 ,latitude:str ,longtitude:str
                 , kota:str, queue:dict):
       
        self.identifier=identifier
        self.token=token

        self.offsetHour=offsetHour
        self.offsetMinutes=offsetMinutes

        self.sensorType=sensorType
        self.interval=interval;

        self.latitude=latitude
        self.longtitude=longtitude

        self.kota=kota
        self.queue=queue
        
        
    def setSensingTable(self, sensingTable):
        self.sensingTable=sensingTable
        print(self.sensingTable)

    def setQueue(self, queue):
        self.queue=queue

    def addSensingTable(self,nameNewTable):
        self.sensingTable.append(nameNewTable)


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
    
    def getInterval(self):
        return self.interval