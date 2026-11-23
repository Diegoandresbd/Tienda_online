import os
from contextlib import contextmanager
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

@contextmanager
def get_db_cursor(dictionary=False):
    conn = get_db_connection()
    cursor = None
    try:
        cursor = conn.cursor(dictionary=dictionary)
        yield conn, cursor
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()

# 1. Ruta de Inicio (Index)
@app.route('/')
def index():
    return render_template('index.html')

# 2. Ruta para ver el Catálogo de Productos (Inventario)
@app.route('/productos')
def productos():
    try:
        with get_db_cursor(dictionary=True) as (_, cursor):
            cursor.execute("SELECT * FROM productos")
            lista_productos = cursor.fetchall()
        return render_template('productos.html', productos=lista_productos)
    except Exception as e:
        return f"Error al conectar con la base de datos: {e}"

# 3. Ruta para el Registro de Nuevos Clientes
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        email = request.form['email'].strip()

        if not nombre or not email:
            flash('Nombre y correo electrónico son obligatorios.', 'danger')
            return redirect(url_for('registro'))

        try:
            with get_db_cursor() as (conn, cursor):
                cursor.execute("INSERT INTO clientes (nombre, email) VALUES (%s, %s)", (nombre, email))
                conn.commit()
            flash('¡Cliente registrado con éxito!', 'success')
            return redirect(url_for('registro'))
        except mysql.connector.Error as err:
            flash(f'Error al registrar (¿correo duplicado?): {err}', 'danger')
            
    return render_template('registro.html')

# 4. Ruta para el Historial de Compras y Clientes
@app.route('/historial')
def historial():
    try:
        with get_db_cursor(dictionary=True) as (_, cursor):
            query = """
                SELECT c.fecha_compra, cl.nombre AS cliente, p.nombre AS producto, c.cantidad, c.total 
                FROM compras c
                JOIN clientes cl ON c.cliente_id = cl.id
                JOIN productos p ON c.producto_id = p.id
                ORDER BY c.fecha_compra DESC
            """
            cursor.execute(query)
            lista_compras = cursor.fetchall()

            cursor.execute("SELECT * FROM clientes ORDER BY fecha_registro DESC")
            lista_clientes = cursor.fetchall()

        return render_template('historial.html', compras=lista_compras, clientes=lista_clientes)
    except Exception as e:
        return f"Error al cargar el historial: {e}"

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)