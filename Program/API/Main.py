
import uvicorn
from fastapi import FastAPI,Request
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer


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
    result=databaseAPI.Login(data['username'],data['password'])
    return {"result": result}


@api.post("/signup")
async def signUp(value: Request):
    data= await value.json()
    result=databaseAPI.signUP(data['username'],data['password'],data['email'])
    return {"result": result}

@api.get("/kota")
async def getKota():
    result=databaseAPI.getKota()
    return {"result":result}

@api.post("/kota")
async def insertKota(value: Request):
    data= await value.json()
    result=databaseAPI.insertKota(data['kota'])
    return {"result":result}

@api.get("/lokasi")
async def getLocation(value: Request):
    data= await value.json()
    result=databaseAPI.getLocation(data['idKota'])
    return {"result":result}

@api.post("/lokasi")
async def insertLocation(value: Request):
    data= await value.json()
    result=databaseAPI.insertLocation(
        data['nama']
        ,data['latitude']
        ,data['longtitude']
        ,data['indoor']
        ,data['fk']
        )
    return {"result":result}


@api.get("/bs")
async def getBaseStasion(value: Request):
    data= await value.json()
    result=databaseAPI.getBaseStasion(data['idLokasi'])
    return {"result":result}


@api.post("/bs")
async def insertBaseStasion(value: Request):
    data= await value.json()
    result=databaseAPI.insertBaseStasion(data['identifier'].lower(),data['idLokasi'],data['interval'])

    
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
    result=databaseAPI.getNodeSensor(data['idBaseStasion'].lower())
    return {"result":result}


@api.post("/node")
async def insertNodeSensor(value: Request):
    data= await value.json()
    result=databaseAPI.insertNodeSensor(
        data['tipeSensor']
        ,data['idBaseStasion'].lower()
        )
    return {"result":result}



@api.post("/update")
async def insertNodeSensor(value: Request):
    data= await value.json()
    result=init.insertNewQueue(data['baseId'].lower()
                                ,data['command'])
    return {"result":result}

@api.post("/sensing")
async def insertSensingdata(value: Request):
    data= await value.json()
    try:
        time=data['time']
        identifier=data['baseId'].lower()
        sensingData=data['result']
    except :
        return "wrong arguments"
    
    init(identifier,time)
    result=databaseAPI.insertSensing(time,identifier,sensingData)
    
    return {"result":result}
    












