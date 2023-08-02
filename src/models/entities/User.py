from flask_login import UserMixin

class User(UserMixin):
    def __init__(self,id,username,password,nombre=None,apPaterno=None,apMaterno=None,genero=None,estado=None,cp=None,calle=None,numcas=None) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.nombre = nombre
        self.apPaterno = apPaterno
        self.apMaterno = apMaterno
        self.genero = genero
        self.estado = estado
        self.cp = cp
        self.calle = calle
        self.numcas = numcas
