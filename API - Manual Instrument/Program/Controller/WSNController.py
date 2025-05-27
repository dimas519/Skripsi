
import numpy as np
from Model.WSN import WSN
from OTEL.DT_OTEL_Manual import *


class WSNController:
    def __init__(self,allWSN) :
        self.allWSN=allWSN
        self.tracer = get_tracer_provider().get_tracer(__name__) ##add this

    def __searchWSN(self,identifier):
        with self.tracer.start_as_current_span("__searchWSN()") as span:
            for wsn in self.allWSN:
                if(wsn.getIdentifier()==identifier):
                    return wsn
            return None
    
    def __nameTable(self,identifier,time,newFormat=False):
        with self.tracer.start_as_current_span("__nameTable()") as span:
            tahun=time[2:4]
            bulan=time[5:7]
            namaTabel=(str(identifier)+"-"+str(bulan)+"-"+str(tahun))
            span.set_attribute("tableName", namaTabel)

            return namaTabel
    
    def __isTableCreated(self, namaTabel,selectedWSN):
        with self.tracer.start_as_current_span("__isTableCreated()") as span:
        
            tableCreated=False
            for table in selectedWSN.getSensingTable():
                if(table==namaTabel):
                    tableCreated=True
                    break

            return tableCreated
    
    def __createTable(self, allSensor, identifier, time):

        with self.tracer.start_as_current_span("__createTable()") as span:
        
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
        with self.tracer.start_as_current_span("sensingProcedure()") as span:
            selectedWSN=self.__searchWSN(identifier)

            span.set_attribute("identifier", identifier) #NOTE OTEL report metric
            
            if(selectedWSN==None):
                return 401
            
            if not (selectedWSN.getToken()==token):
                return 401
        
            selectedWSN.setLastData(dataJSON) #not sure this working during implementing otel

            # time=ServerVariable.getTime(selectedWSN.getOffsetHour(), selectedWSN.getOffsetMinutes())
            nameTable=self.__nameTable(identifier,time)
            isCreated=self.__isTableCreated(nameTable,selectedWSN)
    
            if(not isCreated):
                sql=self.__createTable(selectedWSN.getSensorType(), identifier,time)
                dbController.executeDb(sql)
                selectedWSN.addSensingTable(nameTable)
            
            
            result=dbController.insertSensing(time,identifier,sensingData)

            #NOTE OTEL report metric
            attributes = {"identifier": identifier,"action":"sensingData"}
            counterMeter.add(1,attributes=attributes) #buat ngecount ada berapa kali sensing, tapi dalam sekali run. jadi mengecek apakah restart" atau tidak
            #NOTE OTEL report metric


            if(selectedWSN.getQueue()==None):
                histogramWSN.record(0,attributes=attributes)   #NOTE OTEL report metric pakai histogram agar dia ter aggregate tidak gauge

                return {"result":result}

          
            else:
                queue=selectedWSN.getQueue(); #ini queue buat commanding

                histogramWSN.record(len(queue),attributes=attributes)   #NOTE OTEL report metric
          
                # hapus lagi queue
                dbController.deleteQueue(selectedWSN.getQueue()['id'])
                selectedWSN.setQueue(None)
                command=queue['command'].split(":")

                return {str(command[0]):int(command[1])}
   

    def updateQueue(self, dbController, identifier, command):
        with self.tracer.start_as_current_span("updateQueue()") as span:
            selectedWSN=self.__searchWSN(identifier)
            newID=dbController.insertQueue(identifier,command)

            commandSplit=command.split(":")
            if(commandSplit[0]=='setInterval'):
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
            

            attributes = {"identifier": identifier,"action":"updateQueue"}
            histogramWSN.record(len(selectedWSN.getQueue()),attributes=attributes)
           

            return True
    
    def getInterval(self,identifier):
        with self.tracer.start_as_current_span("getInterval()") as span:
            selectedWSN=self.__searchWSN(identifier)
            return selectedWSN.getInterval()
        
    def getData(self, dbController,identifier,start,end,interval,statistics):
        with self.tracer.start_as_current_span("getData()") as span:
            if (type(identifier)==list):
                result={}
                for bs in identifier: #untuk ngambilin kalau base sehingga interval sudah pernah didapat
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

                    #NOTE OTEL report metric
                    attributes = {"identifier": identifier,"dataUnit":statistics} #mungkin butuh time biar bisa displit by time
                    gaugeRowData.set(attributes,identifier)
                    #NOTE OTEL report metric
                
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
        with self.tracer.start_as_current_span("averageData()") as span:
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
        with self.tracer.start_as_current_span("medianData()") as span:
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
        with self.tracer.start_as_current_span("rawData()") as span:
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
        with self.tracer.start_as_current_span("statDataQuartile()") as span:
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
        with self.tracer.start_as_current_span("count_range()") as span:
            count = 0
            for num in data:
                if start <= num < end:
                    count += 1
            return count 
    
    def statDataRange(self, sensingData, span):
            with self.tracer.start_as_current_span("statDataRange()") as span:
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
        with self.tracer.start_as_current_span("getRealTime()") as span:
            selectedWSN=self.__searchWSN(identifier)
            return selectedWSN.getLastData()
        
        

    def insertNewWSN(self,dbController, identifier, nama, indoor, interval, tipeSensor, idBS):
        with self.tracer.start_as_current_span("insertNewWSN()") as span:
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
    
        
    