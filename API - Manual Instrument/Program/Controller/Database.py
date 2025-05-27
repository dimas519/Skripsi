
import mysql.connector
from OTEL.DT_OTEL_Manual import * #untuk import all termasuk dependency

class mysqlDB:
    def __init__(self,ip,port,database,username,password) :
        self.ip=ip
        self.port=port
        self.database=database
        self.username=username
        self.password=password
        self.tracer = get_tracer_provider().get_tracer(__name__) ##add this
        
    def connect(self):
        self.mydb = mysql.connector.connect(
        
        host=self.ip,
        port=self.port,
        database=self.database,

        user=self.username,
        password=self.password
        )

    def closeConnect(self):
        self.mydb.close()

    def executeSelectQuery(self,query,dictionary=True):
        with self.tracer.start_as_current_span(query) as span:
            self.connect()
            mycursor = self.mydb.cursor( dictionary=dictionary)
            try:
                mycursor.execute(query,multi=True)
                data=mycursor.fetchall()
                return data
            except mysql.connector.IntegrityError as err:
                return False
            finally:
                self.closeConnect()
        
    
    def executeNonSelectQuery(self ,query):
        with self.tracer.start_as_current_span(query) as span:
            self.connect()
            try:
                mycursor = self.mydb.cursor()
                mycursor.execute(query)
                self.mydb.commit()
                if mycursor.lastrowid == 0:
                    return 1
                return mycursor.lastrowid
            except mysql.connector.IntegrityError as err:
                print(err)
                return None
            finally:
                self.closeConnect()