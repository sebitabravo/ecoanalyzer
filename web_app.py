from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
import os
import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'ecoanalyzer_secret_key_2025'

# Configuración de rutas de base de datos
DB_USUARIOS = os.path.join('database', 'usuario.db')
DB_PRODUCTOS = os.path.join('database', 'productos.db')

def init_databases():
    """Inicializa las bases de datos si no existen"""
    # Base de datos de usuarios
    conn_usuarios = sqlite3.connect(DB_USUARIOS)
    c_usuarios = conn_usuarios.cursor()
    c_usuarios.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL
        )
    ''')
    
    # Crear usuario admin por defecto si no existe
    c_usuarios.execute('SELECT * FROM usuarios WHERE usuario = ?', ('admin',))
    if not c_usuarios.fetchone():
        c_usuarios.execute('INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)', ('admin', '1234'))
    
    conn_usuarios.commit()
    conn_usuarios.close()
    
    # Base de datos de productos (mantener estructura original)
    conn_productos = sqlite3.connect(DB_PRODUCTOS)
    c_productos = conn_productos.cursor()
    c_productos.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            dia TEXT,
            nombre TEXT,
            hora TEXT,
            precio REAL,
            vendido INTEGER,
            ganancia REAL
        )
    ''')
    conn_productos.commit()
    conn_productos.close()

def login_required(f):
    """Decorador para verificar que el usuario esté logueado"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        
        conn = sqlite3.connect(DB_USUARIOS)
        c = conn.cursor()
        c.execute('SELECT * FROM usuarios WHERE usuario = ? AND contrasena = ?', (usuario, contrasena))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['logged_in'] = True
            session['usuario'] = usuario
            flash('Bienvenido al EcoAnalyzer', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales incorrectas', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    conn = sqlite3.connect(DB_PRODUCTOS)
    c = conn.cursor()
    c.execute('SELECT rowid, * FROM productos ORDER BY rowid DESC')
    productos = c.fetchall()
    conn.close()
    
    return render_template('dashboard.html', productos=productos)

@app.route('/agregar_producto', methods=['POST'])
@login_required
def agregar_producto():
    dia = request.form['dia']
    nombre = request.form['nombre']
    precio = float(request.form['precio'])
    vendido = int(request.form['vendido'])
    hora = datetime.datetime.now().strftime("%H:%M:%S")
    ganancia = precio * vendido
    
    conn = sqlite3.connect(DB_PRODUCTOS)
    c = conn.cursor()
    c.execute('''
        INSERT INTO productos (dia, nombre, hora, precio, vendido, ganancia)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (dia, nombre, hora, precio, vendido, ganancia))
    conn.commit()
    conn.close()
    
    flash('Producto agregado correctamente', 'success')
    return redirect(url_for('dashboard'))

@app.route('/editar_producto/<int:producto_id>', methods=['POST'])
@login_required
def editar_producto(producto_id):
    dia = request.form['dia']
    nombre = request.form['nombre']
    precio = float(request.form['precio'])
    vendido = int(request.form['vendido'])
    hora = datetime.datetime.now().strftime("%H:%M:%S")
    ganancia = precio * vendido
    
    conn = sqlite3.connect(DB_PRODUCTOS)
    c = conn.cursor()
    c.execute('''
        UPDATE productos
        SET dia = ?, nombre = ?, hora = ?, precio = ?, vendido = ?, ganancia = ?
        WHERE rowid = ?
    ''', (dia, nombre, hora, precio, vendido, ganancia, producto_id))
    conn.commit()
    conn.close()
    
    flash('Producto editado correctamente', 'success')
    return redirect(url_for('dashboard'))

@app.route('/eliminar_producto/<int:producto_id>', methods=['POST'])
@login_required
def eliminar_producto(producto_id):
    conn = sqlite3.connect(DB_PRODUCTOS)
    c = conn.cursor()
    c.execute('DELETE FROM productos WHERE rowid = ?', (producto_id,))
    conn.commit()
    conn.close()
    
    flash('Producto eliminado correctamente', 'success')
    return redirect(url_for('dashboard'))

@app.route('/api/graficos')
@login_required
def api_graficos():
    conn = sqlite3.connect(DB_PRODUCTOS)
    c = conn.cursor()
    c.execute('SELECT nombre, SUM(ganancia) as total_ganancia FROM productos GROUP BY nombre')
    datos = c.fetchall()
    conn.close()
    
    nombres = [dato[0] for dato in datos]
    ganancias = [dato[1] for dato in datos]
    
    return jsonify({
        'nombres': nombres,
        'ganancias': ganancias
    })

if __name__ == '__main__':
    init_databases()
    app.run(debug=True, host='0.0.0.0', port=8081)