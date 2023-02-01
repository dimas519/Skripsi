while True:
    try:
        import uvicorn 
        break
    except:
        import subprocess
        subprocess.call("pip install uvicorn==0.20.0") #dilakukan agar pip terinstall di containernya, bukan python global
        continue

while True:
    try:
        from fastapi import FastAPI,Request
        from starlette.middleware.cors import CORSMiddleware
        from fastapi import FastAPI
        from fastapi.security import OAuth2PasswordBearer
        break
    except:
        import subprocess
        subprocess.call("pip install fastapi==0.87.0")
        continue






from ConfigurationAPI import Configuration



#configurasi db dll
from ConfigurationAPI import Configuration
from Controller.databaseController import DataBaseContoller
from InitializingConfiguration import Initialization

print("initializing")
Config=Configuration()
databaseConf=Config.getDataBase();

databaseAPI=DataBaseContoller(
            databaseConf['iPAddress'],
            int(databaseConf['port']),
            databaseConf['database'],
            databaseConf['username'],
            databaseConf['password']
        )



init = Initialization(databaseAPI)




print("initializing Done")







#start api
if __name__ == "__main__":
    from ConfigurationAPI import Configuration

    print("initializing api")
    Config=Configuration()
    serverConf=Config.getServer();
  
    uvicorn.run("Main:api", 
                host=serverConf['iPAddress'], 
                port=int(serverConf['port']), 
                reload=serverConf['reload'],
                workers=int(serverConf['worker'])
                )
    print("initializing api done")
    # api=FastAPI()
                




api=FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

serverAlowed=[
"http://www.google.com",
"http://dimas519.com"
]

api.add_middleware(
CORSMiddleware,
allow_credentials=False,
allow_origins=serverAlowed,
allow_methods=["*"],
allow_headers=['Content-Type, Authorization, Content-Length, X-Requested-With, Accept'],
)

@api.get("/")
async def Test():
    return {"Hello": "World"}



@api.post("/login")
async def login(value: Request):
    data= await value.json()
    try:
        username=data['username']
        password=data['password']
    except:
        return "wrong arguments"

    result=databaseAPI.Login(username,password)
    return {"result": result}


@api.post("/signup")
async def signUp(value: Request):
    data= await value.json()
    try :
        username=data['username']
        password=data['password']
        email=data['email']
    except:
        return "wrong arguments"

    result=databaseAPI.signUP(data['username'],data['password'],data['email'])
    return {"result": result}

@api.get("/kota")
async def getKota():
    result=databaseAPI.getKota()
    return {"result":result}

@api.post("/kota")
async def insertKota(value: Request):
    data= await value.json()
    try:
        nama=data['kota']
    except:
        return "wrong arguments"

    result=databaseAPI.insertKota(nama)
    return {"result":result}

@api.get("/lokasi")
async def getLocation(value: Request):
    data= await value.json()
    try:
        idKota=data['idKota']
    except:
        return "wrong arguments"

    result=databaseAPI.getLocation(idKota)
    return {"result":result}

@api.post("/lokasi")
async def insertLocation(value: Request):
    data= await value.json()
    try:
        nama=data['nama']
        latitude=data['latitude']
        longtitude=data['longtitude']
        indoor=data['indoor']
        idKota=data['idKota']
    except:
        return "wrong arguments"

    result=databaseAPI.insertLocation(nama,latitude,longtitude,indoor,idKota)
    return {"result":result}


@api.get("/bs")
async def getBaseStasion(value: Request):
    data= await value.json()
    try:
        idLokasi=data['idLokasi']
    except:
        return "wrong arguments"

    result=databaseAPI.getBaseStasion(idLokasi)
    return {"result":result}


@api.post("/bs")
async def insertBaseStasion(value: Request):
    data= await value.json()
    try:
        identifier=data['identifier'].lower()
        idLokasi=data['idLokasi']
        interval=data['interval']
    except:
        return "wrong arguments"
    
    result=databaseAPI.insertBaseStasion(identifier,idLokasi,interval)

    
    if(result):
        res={
            "success":True,
            "token":result[1]
        }
        return {"result":res}
    else:
        return {"result":False}


@api.get("/node")
async def getNode(value: Request):
    data= await value.json()
    try:
        identifier=data['idBS'].lower()
    except:
        return "wrong arguments"

    result=databaseAPI.getNodeSensor(identifier)
    return {"result":result}


@api.post("/node")
async def insertNodeSensor(value: Request):
    data= await value.json()
    try :
        tipeSensor=data['tipeSensor']
        identifier=data['idBS'].lower()
    except:
        return "wrong arguments"    


    result=databaseAPI.insertNodeSensor(tipeSensor,identifier)
    return {"result":result}



@api.post("/update")
async def insertNodeSensor(value: Request):
    data= await value.json()
    try:
        identifier=data['idBS'].lower()
        command=data['command']
    except:
        return "wrong arguments"


    result=init.insertNewQueue(identifier.lower(),data['command'])
    return {"result":result}

@api.post("/sensing")
async def insertSensingdata(value: Request):
    import time as Time
    data= await value.json()
    try:
        identifier=data['idBS'].lower()
        sensingData=data['result']
    except :
        return "wrong arguments"

    second=Time.time()
    Ltime=Time.localtime(second)

    year=Ltime.tm_year
    month=Ltime.tm_mon
    day=Ltime.tm_mday

    hour=Ltime.tm_hour
    min=Ltime.tm_min
    sec=Ltime.tm_sec

    time=str(year)+"-"+str(month)+"-"+str(day)+"-"+str(hour)+"-"+str(min)+"-"+str(sec)

    
    init(identifier,time)
    result=databaseAPI.insertSensing(time,identifier,sensingData)
    
    return {"result":result}
    












