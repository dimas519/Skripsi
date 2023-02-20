import  ServerVariable
class WSNController:
    def __init__(self,allWSN) :
        self.allWSN=allWSN

    def __searchWSN(self,identifier):
        for wsn in self.allWSN:
            if(wsn.getIdentifier()==identifier):
                return wsn
        return None
    
    def __isTableCreated(self,identifier,time,selectedWSN):

        tableCreated=False
        tahun=time[2:4]
        bulan=time[5:7]
        namaTabel=(str(identifier)+"-"+str(bulan)+"-"+str(tahun))
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

        print("sql test",sql)
        return sql
    
    def sensingProcedure(self, dbController, identifier, sensingData):
        selectedWSN=self.__searchWSN(identifier)
        time=ServerVariable.getTime(selectedWSN.getOffsetHour(), selectedWSN.getOffsetMinutes())
        
        isCreated=self.__isTableCreated(identifier,time,selectedWSN)
        if(not isCreated):
            sql=self.__createTable(selectedWSN.getSensorType(), identifier
                               ,time)
            dbController.executeDb(sql)
        
        result=dbController.insertSensing(time,identifier,sensingData)

        if(selectedWSN.getQueue()==None):
            return {"result":result}
        else:
            queue=selectedWSN.getQueue();

            # hapus lagi queue
            dbController.deleteQueue(selectedWSN.getQueue()['id'])
            selectedWSN.setQueue(None)
            


            return queue;

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
        

