
import configparser
import os
class Configuration:

    def __init__(self) :
        print("getting configuration")

        cwd = os.getcwd()
        print(os.path)


        self.config = configparser.ConfigParser()
        self.config.read("Config/serverConf.ini")

        if type(self.config) is None:
            print("not found config file")

    def getDataBase(self):
        database=self.config['Database']
        return database

    def getServer(self):
        server=self.config['API_SERVER']
        return server
    


