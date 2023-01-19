
import uvicorn
from fastapi import FastAPI,Request
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer


from ConfigurationAPI import Configuration
from DatabaseAPI import Database

databaseAPI=None;


if __name__ == "__main__":
    from ConfigurationAPI import Configuration
    from DatabaseAPI import Database


    print("initializing")
    Config=Configuration()
    serverConf=Config.getServer();
    print("initializing Done")
  
    uvicorn.run("Main:api", 
                host=serverConf['iPAddress'], 
                port=int(serverConf['port']), 
                reload=serverConf['reload'],
                workers=int(serverConf['worker'])
                )
                


from ConfigurationAPI import Configuration
from DatabaseAPI import Database


print("initializing")
Config=Configuration()
databaseConf=Config.getDataBase();

databaseAPI=Database(
            databaseConf['iPAddress'],
            int(databaseConf['port']),
            databaseConf['database'],
            databaseConf['username'],
            databaseConf['password']
        )










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
    return result;

@api.post("/kota")
async def insertKota(value: Request):
    data= await value.json()
    result=databaseAPI.insertKota(data['kota'])
    return {"success":result}

@api.get("/lokasi")
async def getLocation(value: Request):
    data= await value.json()
    result=databaseAPI.getLocation(data['idKota'])
    return result

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
    return {"success":result}


@api.get("/bs")
async def getBaseStasion(value: Request):
    data= await value.json()
    result=databaseAPI.getBaseStasion(data['idLokasi'])
    return result


@api.post("/bs")
async def insertBaseStasion(value: Request):
    data= await value.json()
    result=databaseAPI.insertBaseStasion(data['idLokasi'])

    
    if(result[0]):
        res={
            "success":True,
            "token":result[1]
        }
        return res
    else:
        return {"success":False}


@api.get("/node")
async def getNode(value: Request):
    data= await value.json()
    result=databaseAPI.getNodeSensor(data['idBaseStasion'])
    return {"success":result}


@api.post("/node")
async def insertNodeSensor(value: Request):
    data= await value.json()
    result=databaseAPI.insertNodeSensor(
        data['tipeSensor']
        ,data['interval']
        ,data['idBaseStasion']
        )
    
    return {"success":result}












