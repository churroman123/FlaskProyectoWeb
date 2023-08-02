from .entities.User import User
import psycopg2
class ModelUser():
    def get_connection():
        host = 'localhost'
        port = 5432
        dbname = 'BD_ArtesGraficas'
        user = 'postgres'
        password = '123456789'
        conn = psycopg2.connect(host = host, port = port, dbname = dbname, user = user, password = password)
        return conn
    @classmethod
    def login(self,user):
        try:
            conn = ModelUser.get_connection()
            cursor = conn.cursor()
            sql="Select idus,username,pass_us from us_clientes where username= '{}' and pass_us ='{}'".format(user.username,user.password)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0],row[1],row[2])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_by_id(self,id):
     try:
         conn = ModelUser.get_connection()
         cursor = conn.cursor()
         sql="Select * from us_clientes where idus={}".format(id)
         cursor.execute(sql)
         row = cursor.fetchone()
         if row != None:
             return  User(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10])
         else:
             return None
     except Exception as ex:
         raise Exception(ex)
     