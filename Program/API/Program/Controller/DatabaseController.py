from Controller.Database import mysqlDB
import bcrypt


class DataBaseContoller:
    def __init__(self, ip, port, database, username, password) :
        self.db=mysqlDB(ip, port, database, username, password)
        
    def getTables(self):
        sql = "CALL `getAllTables`"
        result=self.db.executeSelectQuery(sql, dictionary=False)
        return result

    def Login(self, username, password, token):
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
        sql="call insertKota('{}')".format(namaKota)
        row=self.db.executeSelectQuery(sql) #menggunakan execute select karena dia akan mengembalikan id
        return {"result":bool(row),"id":row[0]["last_insert_id()"]}
    
    def getKota(self):
        sql="CALL getKota()";
        result=self.db.executeSelectQuery(sql)
        return result
    
    def getBaseStasion(self):
        sql="CALL getBaseStasion()";
        resultLokasi=self.db.executeSelectQuery(sql)
        return resultLokasi
    
    def insertBaseStation(self, nama, latitude, longtitude, fk):
        sql="CALL insertBaseStation('{}','{}','{}',{})".format(nama, latitude, longtitude, fk)
        row=self.db.executeSelectQuery(sql)
        if(row ==False):
            return row
        else:
            return {"result":bool(row),"id":row[0]["last_insert_id()"]}
    
    def getNodeSensor(self, id):
        sql="CALL getNodeSensor({})".format(id);
        result=self.db.executeSelectQuery(sql)
        return result

    def insertNodeSensor(self, identifier, nama, token, indoor, interval, idBS):
        
        sql="CALL insertNodeSensor('{}','{}','{}',{},{},'{}')".format(identifier, nama, token, indoor, interval, idBS)
        row=self.db.executeSelectQuery(sql)
        return row

    def getSensorType(self,id):
        sql="CALL getTipeSensor({})".format(id)
        result=self.db.executeSelectQuery(sql)
        return result


    def insertTipe(self,tipeSensor,idNode):
        sql="INSERT INTO `tipesensor`(`tipeSensor`,`identifier`) VALUES"

        for i in range(0,len(tipeSensor),1):
            if(i!=0):
                sql+=","
            sql+="('{}','{}')".format(tipeSensor[i],idNode)
        row=self.db.executeNonSelectQuery(sql)
        return bool(row)
    
    def insertSensing(self,time,identifier,data):
        tahun=time[2:4]
        bulan=time[5:7]
        sql="INSERT INTO `{}`(`timeStamp`,`suhu`,`kelembapan`,`tekanan`,`akselerasi`) VALUES".format(str(identifier)+"-"+bulan+"-"+tahun)
        sql+="('{}',{},{},{},'{}')".format(time,data['T'],data['rh'],data['Pa'],data['a'])

        row=self.db.executeNonSelectQuery(sql)
        return bool(row)


    def getQueue(self):
        sql="CALL getQueue()"
        result=self.db.executeSelectQuery(sql,True)
        return result
    
    def insertQueue(self,indentifier,command):

        sql="CALL insertQueue('{}','{}')".format(command,indentifier)

        row=self.db.executeNonSelectQuery(sql)
        return row

    def deleteQueue(self,id):
        sql="CALL deleteQueue('{}')".format(id)
        self.db.executeNonSelectQuery(sql);
        
    def getSensingData(self,namaTable,start,end):      
        sql="SELECT * FROM `{}` WHERE `timeStamp`>='{}' AND `timeStamp`<='{}' ORDER BY `timeStamp` ASC".format(namaTable,start,end)
        # return sql

        return self.db.executeSelectQuery(sql)


    def executeDb(self,query):
        return self.db.executeSelectQuery(query)
   
    def updateInterval(self,identifier,interval):
        query ="CALL updateInterval('{}',{})".format(identifier,interval)
        return self.db.executeNonSelectQuery(query)
   



        


