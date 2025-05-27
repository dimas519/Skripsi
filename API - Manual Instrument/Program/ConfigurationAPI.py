
import configparser
import os
class Configuration:

    def __init__(self) :
        print("getting configuration")

        

        

    def getDataBase(self):
    
        database={
            "port":os.getenv("DBPort")  if os.getenv("DBPort") is not None else 3306  ,
            "database":os.getenv("DBName") if os.getenv("DBName") is not None else "skripsi" ,
            "iPAddress":os.getenv("DBiPAddress") if os.getenv("DBiPAddress") is not None else "localhost",
            "username":os.getenv("DBusername") if os.getenv("DBusername") is not None else "root" ,
            "password":os.getenv("DBpassword") if os.getenv("DBpassword") is not None else "",
            }
   
        return database

    def getServer(self):
        server={
            "iPAddress":os.getenv("ApiPAddress") if os.getenv("ApiPAddress") is not None else "0.0.0.0",
            "port":os.getenv("ApiPort") if os.getenv("ApiPort") is not None else 5000,
            "reload":os.getenv("ApiReload") if os.getenv("ApiReload") is not None else True,
            "worker":os.getenv("ApiWorker") if os.getenv("ApiWorker")is not None else 1,
        }
        print("Server Config")
        print(server)
        return server
    


