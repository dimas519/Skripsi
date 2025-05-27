
from datetime import datetime
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
        self.offlineData={"time":"1970-01-01 00:00:00","id":self.identifier,"key":"invalid","result":{"kelembapan":None,"tekanan":None,"suhu":None,"akselerasi":None}}

        self.lastData=self.offlineData
            
        
    def setSensingTable(self, sensingTable):
        self.sensingTable=sensingTable
        print(self.sensingTable)

    def setQueue(self, queue):
        self.queue=queue

    def addSensingTable(self,nameNewTable):
        self.sensingTable.append(nameNewTable)

    def setLastData(self, data):
        timeLastData=self.lastData['time']
        newDataTime=data['time']
        
        lastTime = datetime.strptime(timeLastData,"%Y-%m-%d %H:%M:%S")
        newTime = datetime.strptime(newDataTime,"%Y-%m-%d %H:%M:%S")
        
        
        if(newTime>lastTime):
            self.lastData=data;
        
        
    def setInterval(self,interval):
        self.interval=int(interval)
    

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
        timeLastData=self.lastData['time']
        lastTime = datetime.strptime(timeLastData,"%Y-%m-%d %H:%M:%S")
        timeNow= datetime.now()
        deltaTime=((timeNow-lastTime).seconds)  
        deltaTime*=1000
        
        if deltaTime> (self.interval*5):
            return self.offlineData
        else:
            return self.lastData
        
