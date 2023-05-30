
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
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="wrong arguments",
        )










@api.get("/")
async def Test():
    from fastapi.responses import HTMLResponse
#     a= """
#     <!DOCTYPE html>
# <html>
# <body>

# <h1>The template Element</h1>

# <p>Click the button below to display the hidden content from the template element.</p>

# <button onclick="showContent()">Show hidden content</button>

# <template>
#   <h2>Flower</h2>
#   <img src="img_white_flower.jpg" width="214" height="204">
# </template>

# <script>
# function showContent() {
#   var temp = document.getElementsByTagName("template")[0];
#   var clon = temp.content.cloneNode(true);
#   document.body.appendChild(clon);
# }
# </script>

# </body>
# </html>
#     """
#     return HTMLResponse(content=a, status_code=200)
    return {"Hello": "World"}


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
        offsetHour=data['offsetHour']
        offsetMinutes=data['offsetMinutes']
    except:
        raiseWrongArguments()

    result=databaseAPI.insertKota(nama, offsetHour, offsetMinutes)
    return {"result":result}


@api.get("/lokasi")
async def getLocation(value: Request):
    result=databaseAPI.getLocation()
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
        raiseWrongArguments()

    result=databaseAPI.insertLocation(nama,latitude,longtitude,indoor,idKota)
    return {"result":result}


@api.get("/bs")
async def getBaseStasion(value: Request):
    data= await value.json()
    try:
        idLokasi=data['idLokasi']
    except:
        raiseWrongArguments()

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
        raiseWrongArguments()
    
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
        raiseWrongArguments()

    result=databaseAPI.getNodeSensor(identifier)
    return {"result":result}


@api.post("/node")
async def insertNodeSensor(value: Request):
    data= await value.json()
    try :
        tipeSensor=data['tipeSensor']
        identifier=data['idBS'].lower()
    except:
        raiseWrongArguments()    


    result=databaseAPI.insertNodeSensor(tipeSensor,identifier)
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
async def insertSensingdata(value: Request):
    data= await value.json()
    try:
        identifier=data['idBS'].lower()
        time=data['time']
        sensingData=data['result']
    except :
        raiseWrongArguments()

    result=wsnController.sensingProcedure(databaseAPI,identifier,time,sensingData)
    
    return result
    
@api.post("/interval")
async def insertSensingdata(value: Request):
    data= await value.json()
    try:
        identifier=data['idBS'].lower()
    except :
        raiseWrongArguments()

    result=wsnController.getInterval(identifier)

    return {"setInterval":result}

@api.post("/data")
async def insertSensingdata(value: Request):
    data= await value.json()
    try:
        identifier=data['idBS'].lower()
        start=data['start']
        end=data['end']
        interval=data['interval']
    except :
        raiseWrongArguments()
       
    statistics=None; 
    try:
        statistics=data['stat']
    except:
        statistics='avg'
        

    result=wsnController.getData(databaseAPI,identifier,start,end,interval,statistics)

    return {"result":result}


    









