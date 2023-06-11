
import uvicorn 
from fastapi import FastAPI ,Request, status, HTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer



#configurasi db dll
from ConfigurationAPI import Configuration


import Initialization
from Controller.WSNController import WSNController

# server 
from ServerQueue import ServerQueue
# import ServerVariable


# INITIALIZING
print("initializing")

print("getting Configuration")
Config=Configuration()

# INTIALIZING DB
databaseAPI=Initialization.initDatabase(Config)

# INITALIZING WSN
WSN=Initialization.initWSN(databaseAPI)
wsnController=WSNController(WSN)




queueServer = ServerQueue(databaseAPI)

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

                




api=FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

serverAlowed=[
"*"
,"http://www.google.com"
,"http://dimas519.com"
]

api.add_middleware(
CORSMiddleware,
allow_credentials=False,
allow_origins=serverAlowed,
allow_methods=["*"],
allow_headers=['Content-Type, Authorization, Content-Length, X-Requested-With, Accept'],
)

def raiseWrongArguments():
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="wrong arguments",
        )

# @api.get("/")
# async def Test():
#     from fastapi.responses import HTMLResponse


@api.post("/login")
async def login(value: Request):
    data= await value.json()
    try:
        username=data['username']
        password=data['password']
        token=data['token']
    except:
        raiseWrongArguments()

    result=databaseAPI.Login(username,password,token)
    return {"result": result}


@api.post("/signup")
async def signUp(value: Request):
    data= await value.json()
    try :
        username=data['username']
        password=data['password']
        email=data['email']
    except:
        raiseWrongArguments()

    result=databaseAPI.signUP(username,password,email)
    return {"result": result}


@api.post("/kota")
async def insertKota(value: Request):
    data= await value.json()
    try:
        nama=data['nama']
    except:
        raiseWrongArguments()

    result=databaseAPI.insertKota(nama)
    return {"result":result}


#mengambil semua informasi bs (node sensor,kota)
@api.get("/bs") 
async def getBS():
    result=databaseAPI.getBaseStasion()
    return {"result":result}

#menginput base stasion baru
@api.post("/bs")
async def insertBS(value: Request):
    data= await value.json()
    try:
        nama=data['nama']
        latitude=data['latitude']
        longtitude=data['longtitude']
        idKota=data['idKota']
    except:
        raiseWrongArguments()

    result=databaseAPI.insertBaseStation(nama,latitude,longtitude,idKota)
    return {"result":result}


#mengambil node sensor 
@api.get("/node")
async def getBaseStasion(value: Request):
    data= await value.json()
    try:
        idBS=data['idBS']
    except:
        raiseWrongArguments()

    result=databaseAPI.getNodeSensor(idBS)
    return {"result":result}

#menginputkan node baru
@api.post("/node")
async def insertBaseStasion(value: Request):
    data= await value.json()
    try:
        identifier=data['identifier'].lower()
        idBS=data['idBS']
        nama=data['nama']
        indoor=int(data['indoor'])
        interval=int(data['interval'])
    except:
        raiseWrongArguments()
        
    if(interval<1000):
        raiseWrongArguments()
        return None    
    
    result=databaseAPI.insertNodeSensor(identifier, nama, indoor, interval, idBS)

    if(result[0]):
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
        raiseWrongArguments()

    result=databaseAPI.getNodeSensor(identifier)
    return {"result":result}


@api.post("/tipe")
async def insertNodeSensor(value: Request):
    data= await value.json()
    try :
        tipeSensor=data['tipeSensor']
        identifier=data['idBS'].lower()
    except:
        raiseWrongArguments()    


    result=databaseAPI.insertTipe(tipeSensor,identifier)
    return {"result":result}





@api.post("/update")
async def insertNodeSensor(value: Request):
    data= await value.json()
    try:
        identifier=data['idBS'].lower()
        command=data['command']
    except:
        raiseWrongArguments()

    result=wsnController.updateQueue(databaseAPI,identifier.lower(),command)

   
    return {"result":result}


@api.post("/sensing")
async def sensing(value: Request):
    data= await value.json()
    try:
        identifier=data['idBS'].lower()
        time=data['time']
        sensingData=data['result']
    except :
        raiseWrongArguments()
    wsnController.setRealTime(identifier,data)  
    result=wsnController.sensingProcedure(databaseAPI,identifier,time,sensingData)
    
    return result
    
@api.post("/interval")
async def changeInterval(value: Request):
    data= await value.json()
    try:
        identifier=data['idBS'].lower()
    except :
        raiseWrongArguments()

    result=wsnController.getInterval(identifier)

    return {"setInterval":result}



@api.post("/data")
async def getData(value: Request):
    data= await value.json()
    try:
        identifier=data['idBS']
        start=data['start']
        end=data['end']
        interval=int(data['interval'])
    except :
        raiseWrongArguments()
       
    statistics=None; 
    try:
        statistics=data['stat']
    except:
        statistics='avg'
          

    result=wsnController.getData(databaseAPI,identifier,start,end,interval,statistics)

    return {"result":result}



@api.get("/realTime")
async def getDataRealTime(idBS: str):
    identifier=idBS.lower() 
    result=wsnController.getRealTime(identifier)
    return result


    









