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
    allWSN=databaseControler.getBaseStasion(-1) #-1 tidak spesifik lokasi (ambil semua)
    allQueue=databaseControler.getQueue()
    allSensor=databaseControler.getNodeSensor(None)
    allSensingTable=databaseControler.getTables()
    
    
    print(str(len(allWSN))+" WSN load")
    for i in range(0,len(allWSN)):
        currWSN=allWSN[i]
        listSensor=[]

        for sensor in allSensor:
            if(sensor['identifier']==currWSN['identifier']):
                listSensor.append(sensor['tipeSensor'])


        queuedWSN=None;
        for queue in allQueue:

            if queue['idBS']==currWSN['identifier']:
                queuedWSN=queue

        newWSN=WSN(identifier= currWSN['identifier'], token=currWSN["token"]
                ,offsetHour=currWSN['offsetHour'], offsetMinutes=currWSN['offsetMinutes']
                ,sensorType=listSensor, interval=currWSN['interval']
                ,latitude=currWSN['latitude'], longtitude=currWSN["longtitude"]
                ,kota=currWSN["namaKota"],queue=queuedWSN)


        wsnSensingTable=[]

        for sensingTable in allSensingTable:
            if(sensingTable[0].split("-")[0]==currWSN['identifier']):
                wsnSensingTable.append(sensingTable[0])

        newWSN.setSensingTable(wsnSensingTable)
        wsnRegisterd.append(newWSN)
        print("wsn "+str(i+1)+" loaded")
    print(str(len(allWSN))+" WSN loaded")
    return wsnRegisterd

        