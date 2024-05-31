from flask import Flask, render_template, request,url_for,redirect,flash,send_from_directory,session,Response
from flask_mysqldb import MySQL
from datetime import datetime
#importando mi archivo de configuracion para login
from config import config
import os

app = Flask(__name__,template_folder='templates')

#CONEXION A LA BASE DE DATOS    
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DATABASE'] = 'tienda'

mysql = MySQL(app)

#sesiom
app.secret_key = 'mysecretkey'


# MENU CON EL CATALOGO DE PRODUCTOS
@app.route('/')
def index():
    cursor=mysql.connection.cursor()
    cursor.execute('USE tienda')
    cursor.execute('SELECT * FROM producto')
    productos=cursor.fetchall()
    mysql.connection.commit()
    
    return render_template ('admin/menu.html',productos=productos)


# PAGINA PARA ADMINISTRADORES DE PRODUCTOS
@app.route('/administrar_productos')
def administar():
    cursor=mysql.connection.cursor()
    cursor.execute('USE tienda')
    cursor.execute('SELECT * FROM producto')
    data=cursor.fetchall()
    mysql.connection.commit()
    return render_template ('admin/admin.html', productos=data)

# mostrar la imagen de los productos en la pagina de administracion
@app.route('/img/<imagen>')
def imagenes(imagen):
    return send_from_directory(os.path.join('static/img'), imagen)


# AGREGAR PRODUCTOS 
@app.route('/agregar_producto', methods=['GET','POST'])
def agregar_p():
    if request.method == 'POST':
        producto=request.form['producto']
        imagen=request.files['imagen']
        precio=request.form['precio']
        cantidad=request.form['cantidad'] 
        descripcion=request.form['descripcion']
        
        tiempo=datetime.now()
        horaActual=tiempo.strftime('%Y%H%M%S')
        nuevoNombre = None

        if imagen.filename != "":
            nuevoNombre=horaActual+"_"+imagen.filename
            imagen.save('app/static/img/'+nuevoNombre)

        # creamos la conexion
        cursor=mysql.connection.cursor()
        # damos los valores a insertar
        sql=('INSERT INTO producto (nombre,imagen,precio,cantidad,descripcion) VALUES ( %s,%s,%s,%s,%s);' )    
        datos=(producto,nuevoNombre,precio,cantidad,descripcion)  # Guarda el nombre de la imagen, no el objeto de archivo
        cursor.execute('USE tienda')
        cursor.execute(sql,datos)
        # realizamos la insercion
        mysql.connection.commit()
        flash('Producto agregado correctamente')
        return redirect(url_for('administar'))  # Redirige al usuario a la página de administración
    else:
        return render_template('admin/nuevo.html')



#EDITAR PRODUCTOS
@app.route('/editar_producto/<string:codigo>')
def editar(codigo):
    cursor=mysql.connection.cursor()
    cursor.execute('USE tienda')
    cursor.execute('SELECT * FROM producto WHERE codigo={0}'.format(codigo))
    datos=cursor.fetchall()
    print(datos)
    mysql.connection.commit()
    
    return render_template('admin/editar.html',producto=datos[0])

# ACTUALIZAR PRODUCTOS

@app.route('/update/<codigo>',methods=['POST'])
def update(codigo):
    if request.method == 'POST':
        producto=request.form['producto']
        imagen=request.files['imagen']
        precio=request.form['precio']
        cantidad=request.form['cantidad']
        descripcion=request.form['descripcion']
        
        tiempo=datetime.now()
        horaActual=tiempo.strftime('%Y%H%M%S')
        nuevoNombre = None

        cursor=mysql.connection.cursor()
        cursor.execute('USE tienda')

        # Obtén la imagen actual del producto
        cursor.execute('SELECT imagen FROM producto WHERE codigo={0}'.format(codigo,))
        imagen_actual = cursor.fetchone()[0]

        if imagen.filename != "":
            nuevoNombre=horaActual+"_"+imagen.filename
            imagen.save('app/static/img/'+nuevoNombre)

            # Si se ha subido una nueva imagen, borra la imagen anterior
            if imagen_actual is not None and os.path.exists('app/static/img/'+imagen_actual):
                os.unlink('app/static/img/'+imagen_actual)
        else:
            # Si no se ha subido ninguna imagen, usa la imagen actual
            nuevoNombre = imagen_actual

        sql=""" 
            UPDATE producto
            set 
            nombre=%s,
            imagen=%s,
            precio=%s,
            cantidad=%s,
            descripcion=%s
            WHERE codigo=%s
            """
        datos=(producto,nuevoNombre,precio,cantidad,descripcion, codigo)
        cursor.execute(sql,datos)
        mysql.connection.commit()
        flash('Producto actualizado correctamente')
        return redirect(url_for('administar'))


# ELIMINAR PRODUCTOS
@app.route('/eliminar_producto/<string:codigo>')
def eliminar(codigo):
    cursor=mysql.connection.cursor()
    cursor.execute('USE tienda')
    
    # Obtén la información del producto antes de eliminarlo
    cursor.execute('SELECT * FROM producto WHERE codigo={0}'.format(codigo,))
    producto = cursor.fetchone()
    
    # Verifica si el producto existe
    if producto is not None:
        # Verifica si la imagen del producto existe
        if os.path.exists('app/static/img/'+str(producto[2])):
            os.unlink('app/static/img/'+str(producto[2]))
        
        # Ahora puedes eliminar el producto de la base de datos
        cursor.execute('DELETE FROM producto WHERE codigo={0}'.format(codigo,))
        mysql.connection.commit()
    
    return redirect(url_for('administar'))


# mostrando la descripcion del producto
@app.route('/descripcion/<codigo>',methods=['GET'])
def descripcion(codigo):
    
    # #creando conexion a base de datos
    cursor=mysql.connection.cursor() 
    cursor.execute('USE tienda')
    
    cursor.execute('SELECT * FROM producto WHERE codigo={0}'.format(codigo))
    datos=cursor.fetchall()
    
    mysql.connection.commit()
    return render_template('admin/descripcionP.html',producto=datos[0])


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST' and 'correo' in request.form and 'password' :
        correo = request.form['correo']
        password = request.form['password']
        
        cursor=mysql.connection.cursor()
        cursor.execute('USE tienda')
        cursor.execute('SELECT * FROM usuarios WHERE correo=%s AND password=%s',(correo,password,))
        account=cursor.fetchone()
        
        if account:
            # Si se encuentra un usuario, redirige a la página de menú
            if account[3] ==1:
                return redirect(url_for('index'))
            elif account[3] ==2:
                return redirect(url_for('administar'))
        else:
            # Si no se encuentra un usuario, redirige a la página de inicio de sesión con un mensaje de error
            return render_template('admin/login.html', error='Invalid credentials')
    else:
        # Si la solicitud no es un POST o los campos necesarios no están en el formulario, redirige a la página de inicio de sesión
        return render_template('admin/login.html')

if __name__ == '__main__':
    
    app.config.from_object(config['development'])
    app.run(debug=True)