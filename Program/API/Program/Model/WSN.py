class WSN:
    def __init__(self, identifier:str, token:str 
                 ,sensorType:list, interval:int
                 ,latitude:str ,longtitude:str
                 , kota:str, queue:dict):
       
        self.identifier=identifier
        self.token=token

        self.sensorType=sensorType
        self.interval=interval;

        self.latitude=latitude
        self.longtitude=longtitude

        self.kota=kota
        self.queue=queue
        
        self.lastData={"time":"1970-00-00 00-00-00","idBS":self.identifier,"result":{"kelembapan":None,"tekanan":None,"suhu":None,"akselerasi":None}}
        
        
        
    def setSensingTable(self, sensingTable):
        self.sensingTable=sensingTable
        print(self.sensingTable)

    def setQueue(self, queue):
        self.queue=queue

    def addSensingTable(self,nameNewTable):
        self.sensingTable.append(nameNewTable)

    def setLastData(self, data):
        self.lastData=data;
        
    def setInterval(self,interval):
        self.interval=interval;
    
    
    
    
    

    def getIdentifier(self):
        return self.identifier

    def getToken(self):
        return self.token
    
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
    
    def getLastData(self):
        return self.lastData
    
