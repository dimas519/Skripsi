from Controller.Database import mysqlDB
import bcrypt


class DataBaseContoller:
    def __init__(self,ip,port,database,username,password) :
        self.db=mysqlDB(ip,port,database,username,password)
        
    def getTables(self):
        sql = "CALL `getAllTables`"
        result=self.db.executeSelectQuery(sql,dictionary=False)
        return result

    def Login(self,username, password, token):
        sql = "CALL login('{}')".format(username)
        result=self.db.executeSelectQuery(sql)
        if(len (result)==0):
            return -8
        hashPassword=(result[0]['password']).encode()
        truePassword=bcrypt.checkpw(password.encode(), hashPassword)
        if(not truePassword):
            return -9;
        else :
            sql = "CALL loginSuccess('{}','{}')".format(token,username)
            self.db.executeNonSelectQuery(sql)
            return result[0]['role']

    def signUP(self,username, password,email,role=0):
        hashedPassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        sql = "CALL signUp('{}','{}','{}',{})".format(username,hashedPassword.decode(),email,role)
        try: 
            result=self.db.executeNonSelectQuery(sql)
        except:
            return False
        if(result == None):
            return False
        else :
            return True

    def insertKota(self,namaKota):
        sql="call insertKota('{}')".format(namaKota)
        row=self.db.executeSelectQuery(sql) #menggunakan execute select karena dia akan mengembalikan id
        return {"result":bool(row),"id":row[0]["last_insert_id()"]}

    def getLocation(self):
        sql="call getKota()"
        resultKota=self.db.executeSelectQuery(sql)
        
        sql="CALL getLocation()";
        resultLokasi=self.db.executeSelectQuery(sql)
        return {'kota':resultKota,"lokasi":resultLokasi}
    
    def insertLocation(self,nama,latitude,longtitude,indoor,fk):
        sql="CALL insertLocation('{}','{}','{}',{},{})".format(nama,latitude,longtitude,indoor,fk)
        row=self.db.executeSelectQuery(sql)
        return {"result":bool(row),"id":row[0]["last_insert_id()"]}

    def getBaseStasion(self,id):
        sql=None
        if (id >=0):
            sql="SELECT `identifier`, `token`, `addedTimeStamp`, `lastEditTimeStamp`,`interval` FROM `basestasion` WHERE `idLokasi`={}".format(id)
        else:
            sql="SELECT `identifier`, `token`, `interval`, `lokasi`.`nama` as 'namaLokasi', `latitude`, `longtitude`, `indoor`, `kota`.`nama` as 'namaKota'  FROM `basestasion` INNER JOIN `lokasi` ON `basestasion`.`idLokasi`=`lokasi`.`id` INNER JOIN `kota` ON `lokasi`.`idKota`=`kota`.`id`"
        result=self.db.executeSelectQuery(sql)
        return result


    def insertBaseStasion(self,identifier,idLokasi,interval):
        import random
        token=""
        avaiableCharacter="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        numOfAvaiableCharacter=len(avaiableCharacter)-1
        for i in range(0,10):
            num=random.randint(0,numOfAvaiableCharacter)
            token+=avaiableCharacter[num]


        
        sql="INSERT INTO `basestasion`(`identifier`,`token`,`idLokasi`,`interval`) VALUES('{}','{}',{},{})".format(identifier,token,idLokasi,interval)
        row=self.db.executeNonSelectQuery(sql)
        if(not bool(row)):
            return False
        else:
            return True,token



    def getNodeSensor(self,id):
        sql=None
        if (not id == None):
            sql="SELECT `tipeSensor` FROM `nodesensor` WHERE `identifier`='{}'".format(id) 
        else:
            sql="SELECT * FROM `nodesensor`"
        result=self.db.executeSelectQuery(sql)
        return result


    def insertNodeSensor(self,tipeSensor,idBaseStasion):
        sql="INSERT INTO `nodesensor`(`tipeSensor`,`identifier`) VALUES"

        for i in range(0,len(tipeSensor),1):
            if(i!=0):
                sql+=","
            sql+="('{}','{}')".format(tipeSensor[i],idBaseStasion)
        row=self.db.executeNonSelectQuery(sql)
        return bool(row)
        

    def insertSensing(self,time,identifier,result):
        tahun=time[2:4]
        bulan=time[5:7]
        sql="INSERT INTO `{}`(`timeStamp`,`suhu`,`kelembapan`,`tekanan`,`akselerasi`,`idBS`) VALUES".format(str(identifier)+"-"+bulan+"-"+tahun)
        sql+="('{}',{},{},{},'{}','{}')".format(time,result['T'],result['rh'],result['Pa'],result['a'],identifier)

        row=self.db.executeNonSelectQuery(sql)
        return bool(row)


    def getQueue(self):
        sql="SELECT `id`,`command`,`idBS` FROM `queue_update`"
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
   



        


