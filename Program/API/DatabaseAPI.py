import mysql.connector 


class Database:
    def __init__(self,ip,port,database,username,password) :
        self.mydb = mysql.connector.connect(
        
        host=ip,
        port=port,
        database=database,

        user=username,
        password=password
        )

    def encrypt(self,password):
        import hashlib
        password=hashlib.sha256(password.encode()).hexdigest()
        return password

    def processToJson(self,feature,data):
        result={}
        if (len(feature)>1):
            jsonData=[]
            for i in range(0,len(data)) :
                jsonSingleData={}
                for j in range (0,len(feature)):
                    jsonSingleData[feature[j]]=data[i][j]
                print(jsonSingleData)


        







    def getTables(self):
        mycursor = self.mydb.cursor()
        sql = "SHOW TABLES"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()


        arr=[];
        
        for x in myresult:
            arr.append(x[0])

        return arr

    def Login(self,username, password):
      
        password=self.encrypt(password)

        mycursor = self.mydb.cursor()
        sql = "SELECT `role` FROM `user` WHERE `username` = '{}' AND `password` = '{}'".format(username,password)
     
        mycursor.execute(sql)
        myresult = mycursor.fetchone()
        if(myresult is None):
            return -9;
        else :
            return myresult[0]

    def signUP(self,username, password,email):
    
        password=self.encrypt(password)
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO `user`(`username`,`password`,`email`,`role`) VALUES('{}','{}','{}',0)".format(username,password,email)
        try: 
            mycursor.execute(sql)
        
            self.mydb.commit()
        except:
            return False
        if(mycursor.rowcount==1):
            return True
        else :
            return False

    def getKota(self):
        sql="SELECT * FROM `kota`"
        mycursor = self.mydb.cursor( dictionary=True)
        mycursor.execute(sql)
        data=mycursor.fetchall()
        return data

    def insertKota(self,namaKota):
        try:
            sql="INSERT INTO `kota`(`id`,`nama`) VALUES('','{}')".format(namaKota)
            mycursor = self.mydb.cursor()
            mycursor.execute(sql)
            self.mydb.commit()
            return True
        except:
            return False

    def getLocation(self,id):
        sql="SELECT `id`, `nama`, `latitude`, `longtitude`, `indoor`  FROM `lokasi` WHERE `idKota`={}".format(id)
        mycursor = self.mydb.cursor( dictionary=True)
        mycursor.execute(sql)
        data=mycursor.fetchall()
        return data
    
    def insertLocation(self,nama,latitude,longtitude,indoor,fk):
        try:
            sql="INSERT INTO `lokasi`(`id`,`nama`,`latitude`,`longtitude`,`indoor`,`idKota`) VALUES('','{}','{}',{},{},{})".format(nama,latitude,longtitude,indoor,fk)
            mycursor = self.mydb.cursor()
            mycursor.execute(sql)
            self.mydb.commit()
            return True
        except:
            return False

    def getBaseStasion(self,id):
        sql="SELECT `id`, `token`, `addedTimeStamp`, `lastEditTimeStamp` FROM `basestasion` WHERE `idLokasi`={}".format(id)
        mycursor = self.mydb.cursor( dictionary=True)
        mycursor.execute(sql)
        data=mycursor.fetchall()
        return data


    def insertBaseStasion(self,idLokasi):
        import random
        token=""
        avaiableCharacter="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        numOfAvaiableCharacter=len(avaiableCharacter)
        for i in range(0,10):
            num=random.randint(0,numOfAvaiableCharacter)
            token+=avaiableCharacter[num]


        try:
            sql="INSERT INTO `basestasion`(`id`,`token`,`idLokasi`) VALUES('','{}',{})".format(token,idLokasi)
            mycursor = self.mydb.cursor()
            mycursor.execute(sql)
            self.mydb.commit()
            return True,token
        except:
            return (False)




    def getNodeSensor(self,id):
        sql="SELECT `id`, `tipeSensor`, `interval` FROM `nodesensor` WHERE `idBaseStasion`={}".format(id) 
        mycursor = self.mydb.cursor(dictionary=True)
        mycursor.execute(sql)
        data=mycursor.fetchall()
        return data


    def insertNodeSensor(self,tipeSensor,interval,idBaseStasion):
        try:
            for currTipeSensor in tipeSensor:
                print(currTipeSensor)
                sql="INSERT INTO `nodesensor`(`id`,`tipeSensor`,`interval`,`idBaseStasion`) VALUES('','{}',{},{})".format(currTipeSensor,interval,idBaseStasion)
                mycursor = self.mydb.cursor()
                mycursor.execute(sql)
            self.mydb.commit()
            return True
        except:
            return False

        


