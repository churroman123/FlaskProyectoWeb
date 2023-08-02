from entities.Tarjeta import Tarjeta;
import psycopg2

class ModelTarjeta():
    def get_connection():
        host = 'localhost'
        port = 5432
        dbname = 'BD_ArtesGraficas'
        user = 'postgres'
        password = '123456789'
        conn = psycopg2.connect(host = host, port = port, dbname = dbname, user = user, password = password)
        return conn

    def registrarTarjeta(self,Tarjeta):
        try:        
            conn = ModelTarjeta.get_connection()
            cursor = conn.cursor()
            sql = "insert into tarjeta(titular,numtar,ccv,fechafin,idus) values (%s,%s,%s,%s,%s)".format(Tarjeta.titular,Tarjeta.numtar,Tarjeta.ccv,Tarjeta.fechafin,Tarjeta.idus)
            cursor.execute(sql)
            conn.commit()
            return 
        except Exception as ex:
            raise Exception(ex)
