from Controller.Database import mysqlDB
import bcrypt
from OTEL.DT_OTEL_Manual import *


class DataBaseContoller:
    def __init__(self, ip, port, database, username, password) :
        self.db=mysqlDB(ip, port, database, username, password)
        self.tracer = get_tracer_provider().get_tracer(__name__) #NOTE OTEL traces
        
    def getTables(self):
        with self.tracer.start_as_current_span("getTables()") as span: #NOTE OTEL span
            sql = "CALL `getAllTables`"
            result=self.db.executeSelectQuery(sql, dictionary=False)
            # queueGauge.set(len(result))

            span.set_attribute("numberOfTable", len(result))

            return result

    def Login(self, username, password, token):
        with self.tracer.start_as_current_span("login()") as span: #NOTE OTEL traces
            sql = "CALL login('{}')".format(username)
            result=self.db.executeSelectQuery(sql)
            if(len (result)==0):
                return -8
            hashPassword=(result[0]['password']).encode()
            truePassword=bcrypt.checkpw(password.encode(), hashPassword)
            if(not truePassword):
                return -9;
            else :
                sql = "CALL loginSuccess('{}','{}')".format(token, username)
                self.db.executeNonSelectQuery(sql)
                return result[0]['role']

    def signUP(self, username, password, email, role=0):
        with self.tracer.start_as_current_span("signUP()") as span: #NOTE OTEL traces
            hashedPassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            sql = "CALL signUp('{}','{}','{}',{})".format(username, hashedPassword.decode(), email, role)
            try: 
                result=self.db.executeNonSelectQuery(sql)
            except:
                return False
            if(result == None):
                return False
            else :
                return True

    def insertKota(self, namaKota):
        with self.tracer.start_as_current_span("insertKota()") as span: #NOTE OTEL traces
            sql="call insertKota('{}')".format(namaKota)
            row=self.db.executeSelectQuery(sql) #menggunakan execute select karena dia akan mengembalikan id
            return {"result":bool(row),"id":row[0]["last_insert_id()"]}
    
    def getKota(self):
        with self.tracer.start_as_current_span("getKota()") as span: #NOTE OTEL traces
            sql="CALL getKota()";
            result=self.db.executeSelectQuery(sql)
            return result
    
    def getBaseStasion(self):
        with self.tracer.start_as_current_span("getBaseStasion()") as span: #NOTE OTEL traces
            sql="CALL getBaseStasion()";
            resultLokasi=self.db.executeSelectQuery(sql)
            return resultLokasi
    
    def insertBaseStation(self, nama, latitude, longtitude, fk):
        with self.tracer.start_as_current_span("insertBaseStation()") as span: #NOTE OTEL traces
            sql="CALL insertBaseStation('{}','{}','{}',{})".format(nama, latitude, longtitude, fk)
            row=self.db.executeSelectQuery(sql)
            if(row ==False):
                return row
            else:
                return {"result":bool(row),"id":row[0]["last_insert_id()"]}
    
    def getNodeSensor(self, id):
        with self.tracer.start_as_current_span("getNodeSensor()") as span: #NOTE OTEL traces
            sql="CALL getNodeSensor({})".format(id);
            result=self.db.executeSelectQuery(sql)
            return result

    def insertNodeSensor(self, identifier, nama, token, indoor, interval, idBS): #NOTE OTEL traces
        with self.tracer.start_as_current_span("insertNodeSensor()") as span:
            sql="CALL insertNodeSensor('{}','{}','{}',{},{},'{}')".format(identifier, nama, token, indoor, interval, idBS)
            row=self.db.executeSelectQuery(sql)
            return row

    def getSensorType(self,id):
        with self.tracer.start_as_current_span("getSensorType()") as span: #NOTE OTEL traces
            sql="CALL getTipeSensor({})".format(id)
            result=self.db.executeSelectQuery(sql)
            return result


    def insertTipe(self,tipeSensor,idNode):
        with self.tracer.start_as_current_span("insertTipe()") as span: #NOTE OTEL traces
            sql="INSERT INTO `tipesensor`(`tipeSensor`,`identifier`) VALUES"

            for i in range(0,len(tipeSensor),1):
                if(i!=0):
                    sql+=","
                sql+="('{}','{}')".format(tipeSensor[i],idNode)
            row=self.db.executeNonSelectQuery(sql)
            return bool(row)
    
    def insertSensing(self,time,identifier,data):
        with self.tracer.start_as_current_span("insertSensing()") as span: #NOTE OTEL traces
            tahun=time[2:4]
            bulan=time[5:7]
            sql="INSERT INTO `{}`(`timeStamp`,`suhu`,`kelembapan`,`tekanan`,`akselerasi`) VALUES".format(str(identifier)+"-"+bulan+"-"+tahun)
            sql+="('{}',{},{},{},'{}')".format(time,data['T'],data['rh'],data['Pa'],data['a'])

            row=self.db.executeNonSelectQuery(sql)
            return bool(row)


    def getQueue(self):
        with self.tracer.start_as_current_span("getQueue()") as span: #NOTE OTEL traces
            sql="CALL getQueue()"
            result=self.db.executeSelectQuery(sql,True)
            return result
    
    def insertQueue(self,indentifier,command):
        with self.tracer.start_as_current_span("insertQueue()") as span: #NOTE OTEL traces
            sql="CALL insertQueue('{}','{}')".format(command,indentifier)

            row=self.db.executeNonSelectQuery(sql)
            return row

    def deleteQueue(self,id):
        with self.tracer.start_as_current_span("deleteQueue()") as span: #NOTE OTEL traces
            sql="CALL deleteQueue('{}')".format(id) 
            self.db.executeNonSelectQuery(sql);
        
    def getSensingData(self,namaTable,start,end):      
        with self.tracer.start_as_current_span("getSensingData()") as span: #NOTE OTEL traces
            sql="SELECT * FROM `{}` WHERE `timeStamp`>='{}' AND `timeStamp`<='{}' ORDER BY `timeStamp` ASC".format(namaTable,start,end)
            # return sql

            return self.db.executeSelectQuery(sql)


    def executeDb(self,query):
        with self.tracer.start_as_current_span("executeDb()") as span: #NOTE OTEL traces
            return self.db.executeSelectQuery(query)
   
    def updateInterval(self,identifier,interval):
        with self.tracer.start_as_current_span("updateInterval()") as span: #NOTE OTEL traces
            query ="CALL updateInterval('{}',{})".format(identifier,interval)
            return self.db.executeNonSelectQuery(query)
   



        


