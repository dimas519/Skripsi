import  ServerVariable
class WSNController:
    def __init__(self,allWSN) :
        self.allWSN=allWSN

    def __searchWSN(self,identifier):
        for wsn in self.allWSN:
            if(wsn.getIdentifier()==identifier):
                return wsn
        return None
    
    def __nameTable(self,identifier,time,selectedWSN):
        tahun=time[2:4]
        bulan=time[5:7]
        namaTabel=(str(identifier)+"-"+str(bulan)+"-"+str(tahun))
        print(namaTabel)
        return namaTabel
    
    def __isTableCreated(self, namaTabel,selectedWSN):
        
        tableCreated=False
        for table in selectedWSN.getSensingTable():
            if(table==namaTabel):
                tableCreated=True
                break

        return tableCreated
    
    def __createTable(self, allSensor, identifier, time):
        

        tahun=time[2:4]
        bulan=time[5:7]
        namaTabel=(str(identifier)+"-"+str(bulan)+"-"+str(tahun))




        sql="""CREATE TABLE `{}` (
            `timeStamp` datetime NOT NULL DEFAULT current_timestamp(),""".format(namaTabel)
        concate=False
        for sensor in allSensor:
            if(concate):
                sql+=","

            if(sensor=="Suhu"):
                sql+="`suhu` float NOT NULL"
                concate=True
            elif(sensor =="Kelembapan"):
                sql+="`kelembapan` int(11) NOT NULL"
                concate=True
            elif(sensor=="Tekanan"):
                sql+="`tekanan` int(11) NOT NULL"
                concate=True
            elif(sensor=="Akselerasi"):
                sql+="`akselerasi` varchar(20) NOT NULL"
                concate=True
    

        sql+=""",`idBS` VARCHAR(4) NOT NULL,
            PRIMARY KEY(`timeStamp`)
            )"""

        return sql
    
    def sensingProcedure(self, dbController, identifier, time, sensingData):
        selectedWSN=self.__searchWSN(identifier)
        # time=ServerVariable.getTime(selectedWSN.getOffsetHour(), selectedWSN.getOffsetMinutes())
        nameTable=self.__nameTable(identifier,time,selectedWSN)
        isCreated=self.__isTableCreated(nameTable,selectedWSN)
        if(not isCreated):
            sql=self.__createTable(selectedWSN.getSensorType(), identifier
                               ,time)
            dbController.executeDb(sql)
            selectedWSN.addSensingTable(nameTable)
        
        result=dbController.insertSensing(time,identifier,sensingData)

        if(selectedWSN.getQueue()==None):
            return {"result":result}
        else:
            queue=selectedWSN.getQueue();

            # hapus lagi queue
            dbController.deleteQueue(selectedWSN.getQueue()['id'])
            selectedWSN.setQueue(None)
            command=queue['command'].split(":")

            return {str(command[0]):int(command[1])}
   

    def updateQueue(self, dbController, identifier, command):
        selectedWSN=self.__searchWSN(identifier)
        newID=dbController.insertQueue(identifier,command)


        if(selectedWSN.getQueue()==None):

            newQueue={
                "id":newID
                ,"command":command
                ,"idBS":identifier
            }
            selectedWSN.setQueue(newQueue)
        else:
            queue=selectedWSN.getQueue()
            dbController.deleteQueue(selectedWSN.getQueue()['id'])
            queue['id']=newID
            queue['command']=command
        
        return True
    
    def getInterval(self,identifier):
        selectedWSN=self.__searchWSN(identifier)
        return selectedWSN.getInterval()
        
    def getData(self, dbController,identifier,start,end,interval,clean):
        selectedWSN=self.__searchWSN(identifier)
        
        nameTable=self.__nameTable(identifier,start,selectedWSN)
        isCreated=self.__isTableCreated(nameTable,selectedWSN)
        
        if isCreated:
            intervalWsn=selectedWSN.getInterval()
            sensingData=dbController.getSensingData(nameTable,start,end)
            sensingDataNumber=len(sensingData)
            
            currTime=sensingData[0]['timeStamp'];
            currIntervalLeft=interval
            
            output=[]
            tempTime=[sensingData[0]['timeStamp']]
            tempSuhu=[sensingData[0]['suhu']]
            tempkelembapan=[sensingData[0]['kelembapan']]
            tempTekanan=[sensingData[0]['tekanan']]
            for i in range(1,sensingDataNumber):
                currData=sensingData[i]
                
                diffInterval=(currData['timeStamp']-currTime).total_seconds()
                currIntervalLeft-=diffInterval
  
                currTime=currData['timeStamp']
      
                if(currIntervalLeft <=0 ):
                    
                    currIntervalLeft=interval
                    cell={};
                    cell['timeStamp']= tempTime[0]  
                    cell['suhu']= round(sum(tempSuhu)/len(tempSuhu) ,2)
                    cell['kelembapan']=round( sum(tempkelembapan)/len(tempkelembapan) ,2)
                    cell['tekanan']= round (sum(tempTekanan)/len(tempTekanan),2)
                    output.append(cell)
                    tempTime=[currData['timeStamp']]
                    tempSuhu=[currData['suhu']]
                    tempkelembapan=[currData['kelembapan']]
                    tempTekanan=[currData['tekanan']]
                    
                else:
                    tempTime.append(currData['timeStamp'])
                    tempSuhu.append(currData['suhu'])
                    tempkelembapan.append(currData['kelembapan'])
                    tempTekanan.append(currData['tekanan'])
                                
            
            
            return output
        else:
            return False
        
        
        
        
        
        
    
    

