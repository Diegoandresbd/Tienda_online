import os

from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
app.secret_key = "clave_secreta_para_mensajes" # Necesario para mostrar mensajes de éxito/error

# Función para conectarse a la base de datos MySQL
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "db"), # 'db' es el nombre del servicio en docker-compose
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

# 1. Ruta de Inicio (Index)
@app.route('/')
def index():
    return render_template('index.html')

# 2. Ruta para ver el Catálogo de Productos (Inventario)
@app.route('/productos-rotos')
def productos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) # dictionary=True nos devuelve los datos como diccionarios
        cursor.execute("SELECT * FROM productos")
        lista_productos = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('productos.html', productos=lista_productos)
    except Exception as e:
        return f"Error al conectar con la base de datos: {e}"

# 3. Ruta para el Registro de Nuevos Clientes
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Insertar el nuevo cliente en la base de datos
            cursor.execute("INSERT INTO clientes (nombre, email) VALUES (%s, %s)", (nombre, email))
            conn.commit() # Guardar los cambios
            cursor.close()
            conn.close()
            flash('¡Cliente registrado con éxito!', 'success')
            return redirect(url_for('registro'))
        except mysql.connector.Error as err:
            flash(f'Error al registrar (¿correo duplicado?): {err}', 'danger')
            
    return render_template('registro.html')

# 4. Ruta para el Historial de Compras y Clientes
@app.route('/historial')
def historial():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Consulta para ver las compras junto con el nombre del cliente y el producto
        query = """
            SELECT c.fecha_compra, cl.nombre AS cliente, p.nombre AS producto, c.cantidad, c.total 
            FROM compras c
            JOIN clientes cl ON c.cliente_id = cl.id
            JOIN productos p ON c.producto_id = p.id
            ORDER BY c.fecha_compra DESC
        """
        cursor.execute(query)
        lista_compras = cursor.fetchall()
        
        # También traemos la lista de clientes registrados
        cursor.execute("SELECT * FROM clientes ORDER BY fecha_registro DESC")
        lista_clientes = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return render_template('historial.html', compras=lista_compras, clientes=lista_clientes)
    except Exception as e:
        return f"Error al cargar el historial: {e}"

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)