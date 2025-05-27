
import uvicorn 
from fastapi import FastAPI ,Request, status, HTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI



#configurasi db dll
from ConfigurationAPI import Configuration


import Initialization
from Controller.WSNController import WSNController

# server 
from ServerQueue import ServerQueue
# import ServerVariable
from OTEL.DT_OTEL_Manual import * #untuk import all termasuk dependency

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









##iseng
tracer = get_tracer_provider().get_tracer(__name__) ##add this
















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



serverAlowed=[
"*"
]

api.add_middleware(
CORSMiddleware,
allow_credentials=False,
allow_origins=serverAlowed,
allow_methods=["*"],
allow_headers=['Content-Type, Authorization, Content-Length, X-Requested-With, Accept'],
)

def raiseWrongArguments():
    msg="wrong arguments"
    logging.error(msg)
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=msg,
        )
    
def raiseUnAuth():
    msg="Key missmatch"
    logging.error(msg)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=msg,
        )

# @api.get("/")
# async def Test():
#     from fastapi.responses import HTMLResponse

# source:2,"time":1688456482563,"key":"0eO2khwvgj","id":"AAAc","T":28.39,"rh":51.92,"Pa":92.0,"a":[-0.14, 0.39, -0.97]



@api.post("/login")
async def login(value: Request): 
    with tracer.start_as_current_span("Call to /login") as span: #NOTE OTEL report metric
        span.set_attribute("http.method", "POST") #gk perlu ini kalau rum dia report value
        span.set_attribute("net.protocol.version", "1.1")


        data= await value.json()
        
        try:
            # carrier = {}
            # TraceContextTextMapPropagator().inject(carrier)
            # header = {"traceparent": carrier["traceparent"]}
            
            username=data['username']
            password=data['password']
            token=data['token']

            # span.set_attribute("username", username) #NOTE OTEL report metric
            # meter = get_meter_provider().get_meter("queue", len(result)) #NOTE OTEL report metric
            
            
        except:
            raiseWrongArguments()

        result=databaseAPI.Login(username,password,token)
        

        return {"result": result}



@api.post("/signup")
async def signUp(value: Request):
    with tracer.start_as_current_span("Call to /signup") as span: #NOTE OTEL report metric
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
    with tracer.start_as_current_span("Call to /kota") as span: #NOTE OTEL report metric
        data= await value.json()
        try:
            nama=data['nama']
        except:
            raiseWrongArguments()

        result=databaseAPI.insertKota(nama)
        return {"result":result}

@api.get("/kota")
async def getKota():
    with tracer.start_as_current_span("Call to /kota") as span: #NOTE OTEL report metric
        result=databaseAPI.getKota()
        return {"result":result}




#mengambil semua informasi bs (node sensor,kota)
@api.get("/bs") 
async def getBS():
    with tracer.start_as_current_span("Call to /bs") as span: #NOTE OTEL report metric
        result=databaseAPI.getBaseStasion()
        return {"result":result}

#menginput base stasion baru
@api.post("/bs")
async def insertBS(value: Request):
    with tracer.start_as_current_span("Call to /bs") as span: #NOTE OTEL report metric
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
async def getNodeSensor(idBS: str):
    with tracer.start_as_current_span("Call to /node") as span: #NOTE OTEL report metric
        # data= await value.json()
        # try:
        #     idBS=data['idBS']
        # except:
        #     raiseWrongArguments()
        
        if(idBS==None):
            raiseWrongArguments()

        result=databaseAPI.getNodeSensor(idBS)
        return {"result":result}

#menginputkan node baru
@api.post("/node")
async def insertNodeSensor(value: Request):
    with tracer.start_as_current_span("Call to /node") as span: #NOTE OTEL report metric
        data= await value.json()
        try:
            identifier=data['identifier'].lower()
            idBS=data['idBS']
            nama=data['nama']
            indoor=int(data['indoor'])
            interval=int(data['interval'])
            tipeSensor=data['tipeSensor']
        except:
            raiseWrongArguments()
            
        if(interval<1000):
            raiseWrongArguments()
            return None
        
        result=wsnController.insertNewWSN(databaseAPI,identifier, nama, indoor, interval, tipeSensor, idBS)
    
        # return True
        if(result[0]):
            res={
                "success":True,
                "key":result[1]
            }
            return {"result":res}
        else:
            return {"result":False}



@api.post("/tipe")
async def insertTipeSensor(value: Request):
    with tracer.start_as_current_span("Call to /tipe") as span: #NOTE OTEL report metric
        data= await value.json()
        try :
            tipeSensor=data['tipeSensor']
            identifier=data['node'].lower()
        except:
            raiseWrongArguments()    


        result=databaseAPI.insertTipe(tipeSensor,identifier)
        return {"result":result}





@api.post("/update")
async def update(value: Request):
    with tracer.start_as_current_span("Call to /update") as span: #NOTE OTEL report metric
        data= await value.json()
        try:
            identifier=data['node'].lower()
            command=data['command']
        except:
            raiseWrongArguments()

        result=wsnController.updateQueue(databaseAPI,identifier.lower(),command)

    
        return {"result":result}


@api.post("/sensing")
async def sensing(value: Request):
    with tracer.start_as_current_span("Call to /sensing") as span: #NOTE OTEL report metric
        data= await value.json()
        try:
            identifier=data['id'].lower()
            time=data['time']
            sensingData=data['result']
            token=data['key']
        except :
            raiseWrongArguments()
        
        result=wsnController.sensingProcedure(databaseAPI,identifier, token,time,sensingData, data)
        
        if(result==401):
            raiseUnAuth()
        else:
            return result
    
@api.get("/interval")
async def getInterval(node: str):
    with tracer.start_as_current_span("Call to /interval") as span: #NOTE OTEL report metric
        node=node.lower()
        result=wsnController.getInterval(node)

        return {"setInterval":result}



@api.post("/data")
async def getData(value: Request):
    with tracer.start_as_current_span("Call to /data") as span: #NOTE OTEL report metric
        data= await value.json()
        try:
            identifier=data['node']
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
            
        span.set_attribute("statistics", statistics) #NOTE OTEL report metric


        result=wsnController.getData(databaseAPI,identifier,start,end,interval,statistics)

        return {"result":result}



@api.get("/realTime")
async def getDataRealTime(node: str):
    with tracer.start_as_current_span("Call to /realTime") as span: #NOTE OTEL report metric
        identifier=node.lower() 
        result=wsnController.getRealTime(identifier)
        return result


    









