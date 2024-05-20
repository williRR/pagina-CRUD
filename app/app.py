from flask import Flask, render_template, request,url_for,redirect,flash
from flask_mysqldb import MySQL
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
    return render_template ('admin/menu.html')


# PAGINA PARA ADMINISTRADORES DE PRODUCTOS
@app.route('/administrar_productos')
def administar():
    cursor=mysql.connection.cursor()
    cursor.execute('USE tienda')
    cursor.execute('SELECT * FROM producto')
    data=cursor.fetchall()
    mysql.connection.commit()
    return render_template ('admin/admin.html', productos=data)



#AGREGAR PRODUTOS 
@app.route('/agregar_producto', methods=['GET','POST'])
def agregar_p():
    if request.method == 'POST':
   
     producto=request.form['producto']
     #imagen=request.form['imagen']
     precio=request.form['precio']
     cantidad=request.form['cantidad']  
     
    
     #creamaos la conexion
     cursor=mysql.connection.cursor()
     # damos los valores a insertar
     
     
     sql=('INSERT INTO producto (nombre,precio,cantidad) VALUES ( %s,%s,%s);' )    
     datos=(producto,precio,cantidad)
     cursor.execute('USE tienda')
     cursor.execute(sql,datos)
    #realizamos la insercion
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


@app.route('/update/<codigo>',methods=['POST'])
def update(codigo):
    if request.method == 'POST':
        producto=request.form['producto']
        #imagen=request.form['imagen']
        precio=request.form['precio']
        cantidad=request.form['cantidad']
        
        #conexion a la base de datos
        cursor=mysql.connection.cursor()  
        
        cursor.execute('USE tienda')
        sql=""" 
            UPDATE producto
            set 
            nombre=%s,
            precio=%s,
            cantidad=%s
            WHERE codigo=%s
            """
        datos=(producto,precio,cantidad, codigo)
        cursor.execute(sql,datos)
        mysql.connection.commit()
    flash('Producto actualizado correctamente')
    return redirect(url_for('administar'))
         
        



# #ELIMINAR PRODUCTOS
@app.route('/eliminar_producto/<string:codigo>')
def eliminar(codigo):
    
    cursor=mysql.connection.cursor()
    cursor.execute('USE tienda')
    cursor.execute('DELETE FROM producto WHERE codigo={0}'.format(codigo,))
    mysql.connection.commit()
    return redirect(url_for('administar'))



if __name__ == '__main__':
    app.run(debug=True)