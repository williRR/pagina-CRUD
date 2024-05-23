from flask import Flask, render_template, request,url_for,redirect,flash,send_from_directory
from flask_mysqldb import MySQL
from datetime import datetime
import os

app = Flask(__name__)

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

import os

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


if __name__ == '__main__':
    app.run(debug=True)