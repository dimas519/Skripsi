
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from fastapi import Depends,FastAPI

from fastapi.security import OAuth2PasswordBearer




api=FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

serverAlowed=[
    #  "http://localhost"
    "http://www.google.com"
]

api.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=serverAlowed,
    allow_methods=["*"],
    allow_headers=['Content-Type, Authorization, Content-Length, X-Requested-With, Accept'],
)

# allow origin responsestriving

@api.get("/")
async def read_root():
    return {"Hello": "World"}

@api.get("/testing")

async def read_root():
    return {"Hello": "World1"}


@api.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}

@api.post("/token/")
async def read_items( username,password,client_id,client_secret):
    return True