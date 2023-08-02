from flask import Flask, render_template, redirect,request,url_for,flash

from config import config
from flask_login import LoginManager, login_user,logout_user,login_required,current_user

import psycopg2

from PIL import Image

from io import BytesIO
##modelos

from models.ModelUser import ModelUser

# entities
from  models.entities.User import User


##metodo de conexión
def get_connection():
    host = 'localhost'
    port = 5432
    dbname = 'BD_ArtesGraficas'
    user = 'postgres'
    password = '123456789'
    conn = psycopg2.connect(host = host, port = port, dbname = dbname, user = user, password = password)
    return conn



##convertir imagen en bytea prueba
def insert_img():
    conn = get_connection()
    imagen_path = "C:/Users/Admin/Desktop/Ing. Software/WEB/src/static/images/principal-productos.jpeg"
    with open(imagen_path,"rb") as f:
        imagen = Image.open(f)
        imagen_bytea = psycopg2.Binary(f.read())
    
    with conn.cursor() as cursor:
        cursor.execute("update almacen set img = %s where cod_prod='PBV231'" ,[imagen_bytea])
        conn.commit()


##principal
app = Flask(__name__)

login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(id)

@app.route('/')
def index():
    ##insert_img()
    return render_template('index.html')

@app.route('/redirectRegistro')
def redirectRegistro():
    return redirect('/registro')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/RegistroPrueba', methods=['POST'])
def RegistroPrueba():
    
    if request.method == 'POST':
    
       print(request.form['prueba'])
       return  redirect('/miCuenta')



## Registro de nuevo Cliente en la pagina WEb
@app.route('/RegistroRespuesta', methods=['POST'])
def RegistroRespuesta():
    if request.method == 'POST':
        conn = get_connection()
        try:
            username = request.form['username']
            password = request.form['password']
            nombre = request.form['nombre']
            ap_p = request.form['apellidoPaterno']
            ap_m = request.form['apellidoMaterno']
            genero = request.form.get('genero')
            estado = request.form['estado']
            cp = request.form['cp']
            calle = request.form['calle']
            numcasa = request.form['numcasa']
            
            with conn.cursor() as cursor:   
                cursor.execute("INSERT INTO us_clientes (username, pass_us, nomus,ap_pu,ap_mu,gen,estad,cp,calle,numcas) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s)",(username,password,nombre,ap_p,ap_m,genero,estado,cp,calle,numcasa))
                conn.commit()
            return redirect('/logeo')
        except Exception as ex:
            print(ex)
            return redirect('/registro')
        finally:
            conn.close()

@app.route('/RegistroTarjeta', methods=['POST','GET'])
def RegistroTarjeta():
    print('estoy aqui')
    if request.method == 'POST':
        conn = get_connection()
        print('estoy en post')
        try:
            titular = request.form['titular']
            numeroTarjeta = request.form['tarjeta']
            ccv = request.form['ccv']
            fechafin = request.form['fechafin']
            idUser = current_user.id

            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO tarjeta (titular, numtar, ccv, idus,fechafin) VALUES (%s, %s, %s, %s,%s)",
                               (titular, numeroTarjeta, ccv, idUser,fechafin))
                conn.commit()
            return redirect('/miCuenta')
        except Exception as ex:
            print(ex)
        finally:
            conn.close()

    # Si la solicitud es GET, renderiza el formulario
    print('no me guarde')
    return render_template('miCuenta.html')

@app.route('/redirecthome')
def redirecthome():
    return redirect('/home')

@app.route('/home')
def home():
    return render_template('index.html')

##redigir a tienda
@app.route('/redirectTienda')
def redirectTienda():
    return redirect('/Tienda')

@app.route('/Tienda')
def Tienda():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("select idalmacen, cod_prod,des,nombreprod,precio from almacen where nomprov = 'Alien T-shirts'")
    rows = cursor.fetchall()

    ##creamos lista para almacenar los datos de los productos
    productos=[]

    for row in rows:

        producto ={
            'id':row[0],
            'codigo':row[1],
            'descripcion':row[2],
            'nombre':row[3],
            'precio':row[4],
        }
        productos.append(producto)
    return render_template('Tienda.html', productos=productos)

##para mostrar la imagen del producto correspondiente
@app.route('/imagen_producto/<int:id>')
def imagen_producto(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('select img from almacen where idalmacen = %s',(id),)
    img_bytes = cursor.fetchone()[0]

    try:
        img_io = BytesIO(img_bytes)
        img_pil = Image.open(img_io)
        return img_pil
    except:
        return "error al cargar la imagen"

##redirigir a log in
@app.route('/inicioSesion')
def inicioSesion():
    return redirect('/logeo') 

@app.route('/respuestalogin')
def respuestalogin():
    return redirect(url_for('login'))

##redirigir a mi cuenta
@app.route('/Cuenta')
def Cuenta():
    return redirect('/miCuenta')

@app.route('/miCuenta')
def miCuenta():
    cliente = current_user.username
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("select idventa,dinven,cod_prod,fecha from ventas where cliente = '{}'".format(cliente))
    rows = cursor.fetchall()
    ##creamos lista para almacenar los datos de los pedidos
    compras=[]
    for row in rows:
        compra ={
            'id':row[0],
            'total':row[1],
            'cod_Productos':row[2],
            'fecha':row[3],   
        }
        compras.append(compra)
        
    return render_template('miCuenta.html',compras = compras)

@app.route('/logeo')
def logeo():
    return render_template('login.html')

##se podra acceder aesta ruta con los metodos post y get
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        user = User(0,request.form['username'],request.form['password'])
        logged_user = ModelUser.login(user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect('/')
            else:
                flash("invalid password..") 
                return redirect('/logeo')  
        else:
            flash("User not found...")  
            return redirect('/logeo')  

@app.route('/logout')
def logout():
    logout_user() 
    return redirect('/logeo')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()