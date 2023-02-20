
import configparser
import os
class Configuration:

    def __init__(self) :
        print("getting configuration")


        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'Config/serverConf.ini')

        self.config = configparser.ConfigParser()
        self.config.read(filename)
        if type(self.config) is None:
            print("not found config file")
        server=self.config['API_SERVER']

        

    def getDataBase(self):
        database=self.config['Database']
        return database

    def getServer(self):
        server=self.config['API_SERVER']
        return server
    


