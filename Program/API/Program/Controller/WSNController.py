
import numpy as np
from Model.WSN import WSN

class WSNController:
    def __init__(self,allWSN) :
        self.allWSN=allWSN

    def __searchWSN(self,identifier):
        for wsn in self.allWSN:
            if(wsn.getIdentifier()==identifier):
                return wsn
        return None
    
    def __nameTable(self,identifier,time,newFormat=False):
        tahun=time[2:4]
        bulan=time[5:7]
        namaTabel=(str(identifier)+"-"+str(bulan)+"-"+str(tahun))

        return namaTabel
    
    def __isTableCreated(self, namaTabel,selectedWSN):
        
        tableCreated=False
        for table in selectedWSN.getSensingTable():
            if(table==namaTabel):
                tableCreated=True
                break

        return tableCreated
    
    def __createTable(self, allSensor, identifier, time):
        
        namaTabel=self.__nameTable(identifier,time)


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
    

        sql+=",PRIMARY KEY(`timeStamp`))"
        return sql
    
   
    
    def sensingProcedure(self, dbController, identifier, token, time, sensingData, dataJSON):
        selectedWSN=self.__searchWSN(identifier)
        
        if(selectedWSN==None):
            return 401
        
        if not (selectedWSN.getToken()==token):
            return 401
      
        selectedWSN.setLastData(dataJSON)
        # time=ServerVariable.getTime(selectedWSN.getOffsetHour(), selectedWSN.getOffsetMinutes())
        nameTable=self.__nameTable(identifier,time)
        isCreated=self.__isTableCreated(nameTable,selectedWSN)
   
        if(not isCreated):
            
            sql=self.__createTable(selectedWSN.getSensorType(), identifier,time)
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

        commandSplit=command.split(":")
        if(commandSplit[0]=='setInterval'):
            print("setNewInterval")
            dbController.updateInterval(identifier,commandSplit[1])
            selectedWSN.setInterval(commandSplit[1])

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
        
    def getData(self, dbController,identifier,start,end,interval,statistics):
        if (type(identifier)==list):
            result={}
            for bs in identifier:
                bsData=self.getData(dbController,bs,start,end,interval,statistics)
                result[bs]=bsData
            
            
            
            return result
        else:
            identifier=identifier.lower()
            selectedWSN=self.__searchWSN(identifier)
            if (selectedWSN==None):
                return False
            
            nameTable=self.__nameTable(identifier,start)
            isCreated=self.__isTableCreated(nameTable,selectedWSN)
        
            if isCreated:
                sensingData=dbController.getSensingData(nameTable,start,end)
            
                if(len(sensingData)==0): #mengembalikan false kalau dia kosong
                    return False
            
                if(statistics=='raw'):
                    output=self.rawData(sensingData,interval)
                elif (statistics=='median'):
                    output=self.medianData(sensingData,interval)
                    
                elif(statistics=="inQ"):
                    output=self.statDataQuartile(sensingData)
                elif("split" in statistics):
                    stat=statistics.split("-")
                    if(len(stat)==0):
                        return False
                    try:
                        interval=int(stat[1])
                        output=self.statDataRange(sensingData,interval)    
                    except:
                        return False

                   
                    
                else:
                    output=self.averageData(sensingData,interval)
                
                return output
            else:
                return False
        
        
        
        
        
        
        
    def averageData(self,sensingData,interval):
        
        currTime=sensingData[0]['timeStamp'];
        currIntervalLeft=interval
        output=[]
        tempTime=[sensingData[0]['timeStamp']]
        tempSuhu=[sensingData[0]['suhu']]
        tempkelembapan=[sensingData[0]['kelembapan']]
        tempTekanan=[sensingData[0]['tekanan']]
        
        akselerasiData=sensingData[0]['akselerasi']
        akselerasiData=akselerasiData.replace("[","")
        akselerasiData=akselerasiData.replace("]","")
        
        splitAkselerasi=akselerasiData.split(",")
        tempX=[float(splitAkselerasi[0])]
        tempY=[float(splitAkselerasi[1])]
        tempZ=[float(splitAkselerasi[2])]

        # tempAkselerasi=[sensingData[0]['alse;erasi']]
        for i in range(1,len(sensingData)):
            currData=sensingData[i]
            
            diffInterval=(currData['timeStamp']-currTime).total_seconds()
            currIntervalLeft-=diffInterval

            currTime=currData['timeStamp']

            if(currIntervalLeft <=0): #kalau habis
                
                currIntervalLeft=interval
                cell={};
                lengthData=len(tempSuhu)
                cell['timeStamp']= tempTime[int(lengthData/2)]  
                cell['suhu']= round(sum(tempSuhu)/len(tempSuhu) ,2)
                cell['kelembapan']=round( sum(tempkelembapan)/len(tempkelembapan) ,2)
                cell['tekanan']= round (sum(tempTekanan)/len(tempTekanan),2)
                cell['akselerasi']={
                    "x":round(sum(tempX)/len(tempX),2),
                    "y":round(sum(tempY)/len(tempY),2),
                    "z":round(sum(tempZ)/len(tempZ),2)
                }
                
                output.append(cell)
                tempTime=[currData['timeStamp']]
                tempSuhu=[currData['suhu']]
                tempkelembapan=[currData['kelembapan']]
                tempTekanan=[currData['tekanan']]
                
                akselerasiData=currData['akselerasi']
                akselerasiData=akselerasiData.replace("[","")
                akselerasiData=akselerasiData.replace("]","")
                
                splitAkselerasi=akselerasiData.split(",")
                
                tempX=[float(splitAkselerasi[0])]
                tempY=[float(splitAkselerasi[1])]
                tempZ=[float(splitAkselerasi[2])]
                
            else:
                tempTime.append(currData['timeStamp'])
                tempSuhu.append(currData['suhu'])
                tempkelembapan.append(currData['kelembapan'])
                tempTekanan.append(currData['tekanan'])
                
                akselerasiData=currData['akselerasi']
                akselerasiData=akselerasiData.replace("[","")
                akselerasiData=akselerasiData.replace("]","")
                
                splitAkselerasi=akselerasiData.split(",")
                
                tempX.append(float(splitAkselerasi[0]))
                tempY.append(float(splitAkselerasi[1]))
                tempZ.append(float(splitAkselerasi[2]))
         
         
        if(len(tempSuhu)>0): 
            cell={};
            lengthData=len(tempSuhu)
            cell['timeStamp']= tempTime[int(lengthData/2)]    
            cell['suhu']= round(sum(tempSuhu)/len(tempSuhu) ,2)
            cell['kelembapan']=round( sum(tempkelembapan)/len(tempkelembapan) ,2)
            cell['tekanan']= round (sum(tempTekanan)/len(tempTekanan),2)
            cell['akselerasi']={
                    "x":round(sum(tempX)/len(tempX),2),
                    "y":round(sum(tempY)/len(tempY),2),
                    "z":round(sum(tempZ)/len(tempZ),2)
                }
                    
            output.append(cell)       
                
        return output
    
    def medianData(self,sensingData,interval):
        
        currTime=sensingData[0]['timeStamp'];
        currIntervalLeft=interval
        output=[]
        tempTime=[sensingData[0]['timeStamp']]
        tempSuhu=[sensingData[0]['suhu']]
        tempkelembapan=[sensingData[0]['kelembapan']]
        tempTekanan=[sensingData[0]['tekanan']]
        
        akselerasiData=sensingData[0]['akselerasi']
        akselerasiData=akselerasiData.replace("[","")
        akselerasiData=akselerasiData.replace("]","")
        
        splitAkselerasi=akselerasiData.split(",")
        tempX=[float(splitAkselerasi[0])]
        tempY=[float(splitAkselerasi[1])]
        tempZ=[float(splitAkselerasi[2])]

        # tempAkselerasi=[sensingData[0]['alse;erasi']]
        for i in range(1,len(sensingData)):
            currData=sensingData[i]
            
            diffInterval=(currData['timeStamp']-currTime).total_seconds()
            currIntervalLeft-=diffInterval

            currTime=currData['timeStamp']

            if(currIntervalLeft <=0 ): #kalau habis
                
                
                currIntervalLeft=interval
                cell={};
                medPos=(int)(round((len(tempSuhu)+1)/2,0)) #kalau dia .5 maka +1
                

                medSuhu=tempSuhu[medPos]
                medKelembapan=tempkelembapan[medPos]
                medTekanan=tempTekanan[medPos]
                medX=tempX[medPos]
                medY=tempY[medPos]
                medZ=tempZ[medPos]
                
                if(len(tempSuhu)%2==1):
                    medPos=(int)(len(tempSuhu)/2)
                    
                    medSuhu+=tempSuhu[medPos]
                    medKelembapan+=tempkelembapan[medPos]
                    medTekanan+=tempTekanan[medPos]
                    medX+=tempX[medPos]
                    medY+=tempY[medPos]
                    medZ+=tempZ[medPos]
                        
                
                cell['timeStamp']= tempTime[medPos]  
                cell['suhu']= medSuhu
                cell['kelembapan']=medKelembapan
                cell['tekanan']= medTekanan
                cell['akselerasi']={
                    "x":medX,
                    "y":medY,
                    "z":medZ
                }
                
                output.append(cell)
                tempTime=[currData['timeStamp']]
                tempSuhu=[currData['suhu']]
                tempkelembapan=[currData['kelembapan']]
                tempTekanan=[currData['tekanan']]
                
                akselerasiData=currData['akselerasi']
                akselerasiData=akselerasiData.replace("[","")
                akselerasiData=akselerasiData.replace("]","")
                
                splitAkselerasi=akselerasiData.split(",")
                
                tempX=[float(splitAkselerasi[0])]
                tempY=[float(splitAkselerasi[1])]
                tempZ=[float(splitAkselerasi[2])]
                
            else:
                tempTime.append(currData['timeStamp'])
                tempSuhu.append(currData['suhu'])
                tempkelembapan.append(currData['kelembapan'])
                tempTekanan.append(currData['tekanan'])
                
                akselerasiData=currData['akselerasi']
                akselerasiData=akselerasiData.replace("[","")
                akselerasiData=akselerasiData.replace("]","")
                
                splitAkselerasi=akselerasiData.split(",")
                
                tempX.append(float(splitAkselerasi[0]))
                tempY.append(float(splitAkselerasi[1]))
                tempZ.append(float(splitAkselerasi[2]))
                
                
        if(len(tempSuhu)>0): 
            medSuhu=tempSuhu[medPos]
            medKelembapan=tempkelembapan[medPos]
            medTekanan=tempTekanan[medPos]
            medX=tempX[medPos]
            medY=tempY[medPos]
            medZ=tempZ[medPos]
                
            if(len(tempSuhu)%2==1):
                medPos=(int)(len(tempSuhu)/2)
                    
                medSuhu+=tempSuhu[medPos]
                medKelembapan+=tempkelembapan[medPos]
                medTekanan+=tempTekanan[medPos]
                medX+=tempX[medPos]
                medY+=tempY[medPos]
                medZ+=tempZ[medPos]
                        
                
                cell['timeStamp']= tempTime[medPos]  
                cell['suhu']= medSuhu
                cell['kelembapan']=medKelembapan
                cell['tekanan']= medTekanan
                cell['akselerasi']={
                    "x":medX,
                    "y":medY,
                    "z":medZ
                }
                
                output.append(cell)
                
                
        return output
    
    
    

    def rawData(self,sensingData,interval):
        
        currTime=sensingData[0]['timeStamp'];
        currIntervalLeft=interval
        output=[]
        tempTime=[sensingData[0]['timeStamp']]
        tempSuhu=[sensingData[0]['suhu']]
        tempkelembapan=[sensingData[0]['kelembapan']]
        tempTekanan=[sensingData[0]['tekanan']]
        
        akselerasiData=sensingData[0]['akselerasi']
        akselerasiData=akselerasiData.replace("[","")
        akselerasiData=akselerasiData.replace("]","")
        
        splitAkselerasi=akselerasiData.split(",")
        tempX=[float(splitAkselerasi[0])]
        tempY=[float(splitAkselerasi[1])]
        tempZ=[float(splitAkselerasi[2])]

        # tempAkselerasi=[sensingData[0]['alse;erasi']]
        for i in range(1,len(sensingData)):
            currData=sensingData[i]
            
            diffInterval=(currData['timeStamp']-currTime).total_seconds()
            currIntervalLeft-=diffInterval

            currTime=currData['timeStamp']

            if(currIntervalLeft <=0 ): #kalau habis
                
                
                currIntervalLeft=interval
                cell={};
                lengthData=len(tempSuhu)
                cell['timeStamp']= str(tempTime[int(lengthData/2)])  
                cell['suhu']= tempSuhu
                cell['kelembapan']=tempkelembapan
                cell['tekanan']= tempTekanan
                cell['akselerasi']={
                    "x":tempX,
                    "y":tempY,
                    "z":tempZ
                }
                
                output.append(cell)
                tempTime=[currData['timeStamp']]
                tempSuhu=[currData['suhu']]
                tempkelembapan=[currData['kelembapan']]
                tempTekanan=[currData['tekanan']]
                
                akselerasiData=currData['akselerasi']
                akselerasiData=akselerasiData.replace("[","")
                akselerasiData=akselerasiData.replace("]","")
                
                splitAkselerasi=akselerasiData.split(",")
                
                tempX=[float(splitAkselerasi[0])]
                tempY=[float(splitAkselerasi[1])]
                tempZ=[float(splitAkselerasi[2])]
                
            else:
                tempTime.append(currData['timeStamp'])
                tempSuhu.append(currData['suhu'])
                tempkelembapan.append(currData['kelembapan'])
                tempTekanan.append(currData['tekanan'])
                
                akselerasiData=currData['akselerasi']
                akselerasiData=akselerasiData.replace("[","")
                akselerasiData=akselerasiData.replace("]","")
                
                splitAkselerasi=akselerasiData.split(",")
                
                tempX.append(float(splitAkselerasi[0]))
                tempY.append(float(splitAkselerasi[1]))
                tempZ.append(float(splitAkselerasi[2]))
                
        if(len(tempSuhu)>0): 
            lengthData=len(tempSuhu)
            cell={}; 
            cell['timeStamp']= str(tempTime[int(lengthData/2)])   
            cell['suhu']= tempSuhu
            cell['kelembapan']=tempkelembapan
            cell['tekanan']= tempTekanan
            cell['akselerasi']={
                "x":tempX,
                "y":tempY,
                "z":tempZ
            }
                    
            output.append(cell)  
            
            
        return output
    
    def statDataQuartile(self,sensingData):
        result={};
        sensors=['suhu',"kelembapan","tekanan"]
        data={"suhu":[],"kelembapan":[],"tekanan":[]}
        for i in range(0,len(sensingData)):
            for sensor in sensors:
                data[sensor].append(sensingData[i][sensor])
  
        for sensor in sensors: 
            dataSensor=data[sensor]
            q3 = np.percentile(dataSensor, 75)
            q1 = np.percentile(dataSensor, 25)
            jumlahQ3=0;
            jumlahQ1=0;
            for i in range(0,len(data)):
                if(dataSensor[i]>=q3):
                    jumlahQ3+=1
                elif(dataSensor[i]<=q1):
                    jumlahQ1+=1
            jumlahQ2=len(dataSensor)-(jumlahQ3+jumlahQ1)
            result[sensor]={
                "Q3":q3
                ,"Q1":q1
                ,"numQ1":jumlahQ1
                ,"numQ2":jumlahQ2
                ,"numQ3":jumlahQ3
            }
        return result
    
    def count_range(self, data, start, end):
        count = 0
        for num in data:
            if start <= num < end:
                count += 1
        return count 
    
    def statDataRange(self, sensingData, span):
        result={"suhu":[],"kelembapan":[],"tekanan":[]}

        sensors=['suhu',"kelembapan","tekanan"]
        data={"suhu":[],"kelembapan":[],"tekanan":[]}
        for i in range(0,len(sensingData)):
            for sensor in sensors:
                data[sensor].append(sensingData[i][sensor])
        
        jumlahData=(100/span)
        print (jumlahData)
        for sensor in sensors:
            startNum=1
            for p in range(int(jumlahData)):
                end=startNum+span
                jumlah=self.count_range( data[sensor],    startNum,end)
                
                result[sensor].append(jumlah)
                startNum=startNum+span
  

        return result        
        
    
    def getRealTime(self, identifier):
        selectedWSN=self.__searchWSN(identifier)
        return selectedWSN.getLastData()
    
    

    def insertNewWSN(self,dbController, identifier, nama, indoor, interval, tipeSensor, idBS):
        import random
        token=""
        avaiableCharacter="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        numOfAvaiableCharacter=len(avaiableCharacter)-1
        for i in range(0,10):
            num=random.randint(0,numOfAvaiableCharacter)
            token+=avaiableCharacter[num]
        result=dbController.insertNodeSensor(identifier, nama, token, indoor, interval, idBS)
        
        if(not result):
            return False,False
        
        dbController.insertTipe(tipeSensor,identifier)
        
        latitude=result[0]['latitude']
        longtitude=result[0]['longtitude']
        kota=result[0]['namaKota']
           
        insertedWSN=WSN(identifier=identifier, sensorType=tipeSensor,
                        interval=interval,latitude=latitude,
                        longtitude=longtitude,kota=kota,
                        queue=None,token=token)
        self.allWSN.append(insertedWSN)
        return True,token
        
        
    