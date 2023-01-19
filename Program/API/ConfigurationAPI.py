
import configparser

class Configuration:

    def __init__(self) :
        print("getting configuration")
        self.config = configparser.ConfigParser()
        self.config.read("Config/serverConf.ini")
        
        print(self.config)
        # if type(self.config) is None:
        #     print("not found config file")
        #     print(type(self.config))

    def getDataBase(self):
        database=self.config['Database']
       


        return database

    def getServer(self):
        server=self.config['API_SERVER']
        return server
    


