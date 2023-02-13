from Controller.database import mysqlDB



class DataBaseContoller:
    def __init__(self,ip,port,database,username,password) :
        self.db=mysqlDB(ip,port,database,username,password)
        

    def encrypt(self,password):
        import hashlib
        hashString=hashlib.sha256(password.encode()).hexdigest()
        return hashString

    # def processToJson(self,feature,data):
    #     result={}
    #     if (len(feature)>1):
    #         jsonData=[]
    #         for i in range(0,len(data)) :
    #             jsonSingleData={}
    #             for j in range (0,len(feature)):
    #                 jsonSingleData[feature[j]]=data[i][j]

    #KAYAKNYA BUTUH SP 
    def getTables(self):
        sql = "SHOW TABLES WHERE `Tables_in_skripsi` != 'basestasion' AND  `Tables_in_skripsi` != 'kota' AND  `Tables_in_skripsi` != 'lokasi' AND `Tables_in_skripsi` != 'nodesensor' AND `Tables_in_skripsi` != 'user'  AND `Tables_in_skripsi` != 'queue_update' "
        result=self.db.executeSelectQuery(sql,dictionary=False)
        return result

    def Login(self,username, password):
        password=self.encrypt(password)
        sql = "SELECT `role` FROM `user` WHERE `username` = '{}' AND `password` = '{}'".format(username,password)
        result=self.db.executeSelectQuery(sql)
        if(len(result)==0):
            return -9;
        else :
            return result

    def signUP(self,username, password,email):
        password=self.encrypt(password)
        sql = "INSERT INTO `user`(`username`,`password`,`email`,`role`) VALUES('{}','{}','{}',0)".format(username,password,email)
        try: 
            result=self.db.executeNonSelectQuery(sql)
        except:
            return False
        if(result !=-1):
            return True
        else :
            return False

    def getKota(self):
        sql="SELECT * FROM `kota`"
        result=self.db.executeSelectQuery(sql)
        return result

    def insertKota(self,namaKota):
        sql="INSERT INTO `kota`(`nama`) VALUES('{}')".format(namaKota)
        row=self.db.executeNonSelectQuery(sql)
        return bool(row)

    def getLocation(self,id):
        sql="SELECT `id`, `nama`, `latitude`, `longtitude`, `indoor`  FROM `lokasi` WHERE `idKota`={}".format(id)
        result=self.db.executeSelectQuery(sql)
        return result
    
    def insertLocation(self,nama,latitude,longtitude,indoor,fk):
        sql="INSERT INTO `lokasi`(`nama`,`latitude`,`longtitude`,`indoor`,`idKota`) VALUES('{}','{}',{},{},{})".format(nama,latitude,longtitude,indoor,fk)
        row=self.db.executeNonSelectQuery(sql)
        return bool(row)

    def getBaseStasion(self,id):
        sql="SELECT `identifier`, `token`, `addedTimeStamp`, `lastEditTimeStamp`,`interval` FROM `basestasion` WHERE `idLokasi`={}".format(id)
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
<<<<<<< HEAD
        sql="SELECT `tipeSensor` FROM `nodesensor` WHERE `identifier`='{}'".format(id) 
=======
        sql="SELECT `tipeSensor` FROM `nodesensor` WHERE `idBS`='{}'".format(id) 
>>>>>>> ee561acae2165edc460f0d5466d26aae2edd1f8a
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
        sql+="('{}',{},{},{},'{}','{}')".format(time,result['s'],result['t'],result['k'],result['a'],identifier)

        row=self.db.executeNonSelectQuery(sql)
        return bool(row)


    def getQueue(self):
        sql="SELECT `id`,`command`,`idBS` FROM `queue_update`"
        result=self.db.executeSelectQuery(sql,False)
        return result
    
    def insertQueue(self,indentifier,command):
        sql="INSERT INTO `queue_update`(`command`,`idBS`)  VALUES('{}','{}')".format(command,indentifier)

        row=self.db.executeNonSelectQuery(sql)
        return row

    def deleteQueue(self,id):
        sql="DELETE FROM `queue_update` WHERE `id`={}".format(id)
        self.db.executeNonSelectQuery(sql);


    def executeDb(self,query):
        self.db.executeNonSelectQuery(query)
   





        


