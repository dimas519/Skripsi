from OTEL.DT_OTEL_Manual import *

class ServerQueue:
    def __init__(self,database):
        self.sensingTables=database.getTables()
        print("getting update queue")
        self.queue=database.getQueue() #id,command,idbs
        print("update queue done ",self.queue)
        self.tracer = get_tracer_provider().get_tracer(__name__) ##add this



    def getQueue(self,identifier):
        with self.tracer.start_as_current_span("getQueue()") as span:
            for i in range(0,len(self.queue),1):
                

                attributes = {"action.type": "getQueue()" }


                if(identifier==self.getQueue[i][2]):
                    return self.queue[1]

            return None;

    def insertNewQueue(self,identifier,command):
        #mencari apakah udh ada command yang sama
        with self.tracer.start_as_current_span("insertNewQueue()") as span:
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
        with self.tracer.start_as_current_span("overlapCommand()") as span:
            commandBaru=command.split(":")[0]
            meter = get_meter_provider().get_meter("queue", len(self.queue)) #NOTE OTEL report metric
            for i in range(0,len(self.queue),1):    
                if(self.queue[i][2]==identifier):        
                    commandQueue=self.queue[i][1].split(":")[0]
                    if(commandQueue==commandBaru): #kalau sama
                        temp=self.queue[i][0]
                        del self.queue[i]
                        return temp

            return 0
