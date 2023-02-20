class ServerQueue:
    def __init__(self,database):
        self.sensingTables=database.getTables()
        print("getting update queue")
        self.queue=database.getQueue() #id,command,idbs
        print("update queue done ",self.queue)



    def getQueue(self,identifier):
        for i in range(0,len(self.queue),1):
            if(identifier==self.getQueue[i][2]):
                return self.queue[1]

        return None;

    def insertNewQueue(self,identifier,command):
        #mencari apakah udh ada command yang sama
        overlap=self.overlapCommand(identifier,command)
        if(bool(overlap)): #kalau overlap drop yg lama
            self.database.deleteQueue(overlap)

        newID=self.database.insertQueue(identifier,command)
        if(newID !=-1):
            self.queue.append((newID,command,identifier))
            return True
        else:
            return False
        
    def overlapCommand(self,identifier,command):
        #mencari apakah udh ada command yang sama

        commandBaru=command.split(":")[0]
        for i in range(0,len(self.queue),1):    
            if(self.queue[i][2]==identifier):        
                commandQueue=self.queue[i][1].split(":")[0]
                if(commandQueue==commandBaru): #kalau sama
                    temp=self.queue[i][0]
                    del self.queue[i]
                    return temp

        return 0
