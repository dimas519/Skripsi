from Model.WSN import WSN
from Controller.DatabaseController import DataBaseContoller

def initDatabase(Config):
    print("intializing database")
    databaseConf=Config.getDataBase();

    databaseAPI=DataBaseContoller(
            databaseConf['iPAddress'],
            int(databaseConf['port']),
            databaseConf['database'],
            databaseConf['username'],
            databaseConf['password']
        )
    print("database intialized")
    return databaseAPI

def initWSN(databaseControler):
    wsnRegisterd=[]
    print("load WSN")
    allNodes=databaseControler.getNodeSensor(-1) #-1 tidak spesifik lokasi (ambil semua)
    allQueue=databaseControler.getQueue()
    allSensor=databaseControler.getSensorType(-1)
    allSensingTable=databaseControler.getTables()
    

  
    print(str(len(allNodes))+" WSN load")

    for i in range(0,len(allNodes)):
        currNodes=allNodes[i]
        listSensor=[]
        


        for sensor in allSensor:
            if(sensor['identifier']==currNodes['identifier']):
                listSensor.append(sensor['tipeSensor'])
            
        queuedWSN=None;
        for queue in allQueue:

            if queue['idBS']==currNodes['identifier']:
                queuedWSN=queue



        newWSN=WSN(identifier= currNodes['identifier'], token= currNodes['token']
                ,sensorType=listSensor, interval=currNodes['interval']
                ,latitude=currNodes['latitude'], longtitude=currNodes["longtitude"]
                ,kota=currNodes["namaKota"],queue=queuedWSN)


        wsnSensingTable=[]
        
        for sensingTable in allSensingTable:
            if(sensingTable[0].split("-")[2]==currNodes['identifier']   or sensingTable[0].split("-")[0]==currNodes['identifier']):
                wsnSensingTable.append(sensingTable[0])
                


        newWSN.setSensingTable(wsnSensingTable)
        
        
        wsnRegisterd.append(newWSN)
        print(str(i+1)+". wsn "+currNodes['identifier']+" loaded")
    print(str(len(allNodes))+" WSN loaded")
    return wsnRegisterd

        