from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Cambia esto por una clave secreta segura

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    conexion = conectar_base_datos()
    if conexion is None:
        return None

    cursor = conexion.cursor(dictionary=True)
    cursor.execute('SELECT * FROM usuarios WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conexion.close()

    if user:
        return User(id=user['id'], username=user['username'], password=user['password'])
    return None

def conectar_base_datos():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='root',
            database='portfolio_db',
            ssl_disabled=True
        )
        if conexion.is_connected():
            print('Conexión exitosa a la base de datos')
            return conexion
    except Exception as error:
        print('Error de conexión:', error)
        return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conexion = conectar_base_datos()
        if conexion is None:
            flash('Error al conectar a la base de datos.')
            return redirect(url_for('login'))

        cursor = conexion.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        cursor.close()
        conexion.close()

        if user:
            user_obj = User(id=user['id'], username=user['username'], password=user['password'])
            login_user(user_obj)
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos.')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
def index():
    conexion = conectar_base_datos()
    if conexion is None:
        return "Error al conectar a la base de datos."

    cursor = conexion.cursor(dictionary=True)

    # Obtener información personal
    cursor.execute('SELECT * FROM informacion_personal LIMIT 1')
    info_personal = cursor.fetchone()

    # Obtener experiencia
    cursor.execute('SELECT * FROM experiencia')
    experiencia = cursor.fetchall()

    # Obtener educación
    cursor.execute('SELECT * FROM educacion')
    educacion = cursor.fetchall()

    # Obtener habilidades duras
    cursor.execute('SELECT * FROM habilidades WHERE tipo = "dura"')
    habilidades_duras = cursor.fetchall()

    # Obtener habilidades blandas
    cursor.execute('SELECT * FROM habilidades WHERE tipo = "blanda"')
    habilidades_blandas = cursor.fetchall()

    # Obtener proyectos
    cursor.execute('SELECT * FROM proyectos')
    proyectos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template('index.html',
                           info_personal=info_personal,
                           experiencia=experiencia,
                           educacion=educacion,
                           habilidades_duras=habilidades_duras,
                           habilidades_blandas=habilidades_blandas,
                           proyectos=proyectos)

# Rutas para "Acerca de mí"
@app.route('/editar_acerca_de/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_acerca_de(id):
    conexion = conectar_base_datos()
    if conexion is None:
        return "Error al conectar a la base de datos."
    cursor = conexion.cursor(dictionary=True)
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        cursor.execute('UPDATE informacion_personal SET nombre = %s, apellido = %s, titulo = %s, descripcion = %s WHERE id = %s', (nombre, apellido, titulo, descripcion, id))
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect(url_for('index'))
    cursor.execute('SELECT * FROM informacion_personal WHERE id = %s', (id,))
    info_personal = cursor.fetchone()
    cursor.close()
    conexion.close()
    return render_template('editar_acerca_de.html', info_personal=info_personal)

# Rutas para habilidades
@app.route('/agregar_habilidad', methods=['GET', 'POST'])
@login_required
def agregar_habilidad():
    if request.method == 'POST':
        nombre = request.form['nombre']
        nivel = int(request.form['nivel'])
        tipo = request.form['tipo']
        conexion = conectar_base_datos()
        if conexion is None:
            return "Error al conectar a la base de datos."
        cursor = conexion.cursor()
        cursor.execute('INSERT INTO habilidades (nombre, nivel, tipo) VALUES (%s, %s, %s)', (nombre, nivel, tipo))
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect(url_for('index'))
    return render_template('agregar_habilidad.html')

@app.route('/editar_habilidad/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_habilidad(id):
    conexion = conectar_base_datos()
    if conexion is None:
        return "Error al conectar a la base de datos."
    cursor = conexion.cursor(dictionary=True)
    if request.method == 'POST':
        nombre = request.form['nombre']
        nivel = int(request.form['nivel'])
        tipo = request.form['tipo']
        cursor.execute('UPDATE habilidades SET nombre = %s, nivel = %s, tipo = %s WHERE id = %s', (nombre, nivel, tipo, id))
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect(url_for('index'))
    cursor.execute('SELECT * FROM habilidades WHERE id = %s', (id,))
    habilidad = cursor.fetchone()
    cursor.close()
    conexion.close()
    return render_template('editar_habilidad.html', habilidad=habilidad)

@app.route('/borrar_habilidad/<int:id>')
@login_required
def borrar_habilidad(id):
    conexion = conectar_base_datos()
    if conexion is None:
        return "Error al conectar a la base de datos."
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM habilidades WHERE id = %s', (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect(url_for('index'))

# Rutas para proyectos
@app.route('/agregar_proyecto', methods=['GET', 'POST'])
@login_required
def agregar_proyecto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']
        enlace = request.form['enlace']
        conexion = conectar_base_datos()
        if conexion is None:
            return "Error al conectar a la base de datos."
        cursor = conexion.cursor()
        cursor.execute('INSERT INTO proyectos (nombre, descripcion, fecha, enlace) VALUES (%s, %s, %s, %s)', (nombre, descripcion, fecha, enlace))
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect(url_for('index'))
    return render_template('agregar_proyecto.html')

@app.route('/editar_proyecto/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_proyecto(id):
    conexion = conectar_base_datos()
    if conexion is None:
        return "Error al conectar a la base de datos."
    cursor = conexion.cursor(dictionary=True)
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']
        enlace = request.form['enlace']
        cursor.execute('UPDATE proyectos SET nombre = %s, descripcion = %s, fecha = %s, enlace = %s WHERE id = %s', (nombre, descripcion, fecha, enlace, id))
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect(url_for('index'))
    cursor.execute('SELECT * FROM proyectos WHERE id = %s', (id,))
    proyecto = cursor.fetchone()
    cursor.close()
    conexion.close()
    return render_template('editar_proyecto.html', proyecto=proyecto)

@app.route('/borrar_proyecto/<int:id>')
@login_required
def borrar_proyecto(id):
    conexion = conectar_base_datos()
    if conexion is None:
        return "Error al conectar a la base de datos."
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM proyectos WHERE id = %s', (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect(url_for('index'))

# Rutas para educación
@app.route('/agregar_educacion', methods=['GET', 'POST'])
@login_required
def agregar_educacion():
    if request.method == 'POST':
        titulo = request.form['titulo']
        institucion = request.form['institucion']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        conexion = conectar_base_datos()
        if conexion is None:
            return "Error al conectar a la base de datos."
        cursor = conexion.cursor()
        cursor.execute('INSERT INTO educacion (titulo, institucion, fecha_inicio, fecha_fin) VALUES (%s, %s, %s, %s)', (titulo, institucion, fecha_inicio, fecha_fin))
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect(url_for('index'))
    return render_template('agregar_educacion.html')

@app.route('/editar_educacion/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_educacion(id):
    conexion = conectar_base_datos()
    if conexion is None:
        return "Error al conectar a la base de datos."
    cursor = conexion.cursor(dictionary=True)
    if request.method == 'POST':
        titulo = request.form['titulo']
        institucion = request.form['institucion']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        cursor.execute('UPDATE educacion SET titulo = %s, institucion = %s, fecha_inicio = %s, fecha_fin = %s WHERE id = %s', (titulo, institucion, fecha_inicio, fecha_fin, id))
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect(url_for('index'))
    cursor.execute('SELECT * FROM educacion WHERE id = %s', (id,))
    educacion_item = cursor.fetchone()
    cursor.close()
    conexion.close()
    return render_template('editar_educacion.html', educacion=educacion_item)

@app.route('/borrar_educacion/<int:id>')
@login_required
def borrar_educacion(id):
    conexion = conectar_base_datos()
    if conexion is None:
        return "Error al conectar a la base de datos."
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM educacion WHERE id = %s', (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect(url_for('index'))

# Rutas para experiencia
@app.route('/agregar_experiencia', methods=['GET', 'POST'])
@login_required
def agregar_experiencia():
    if request.method == 'POST':
        puesto = request.form['puesto']
        empresa = request.form['empresa']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        descripcion = request.form['descripcion']
        conexion = conectar_base_datos()
        if conexion is None:
            return "Error al conectar a la base de datos."
        cursor = conexion.cursor()
        cursor.execute('INSERT INTO experiencia (puesto, empresa, fecha_inicio, fecha_fin, descripcion) VALUES (%s, %s, %s, %s, %s)', (puesto, empresa, fecha_inicio, fecha_fin, descripcion))
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect(url_for('index'))
    return render_template('agregar_experiencia.html')

@app.route('/editar_experiencia/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_experiencia(id):
    conexion = conectar_base_datos()
    if conexion is None:
        return "Error al conectar a la base de datos."
    cursor = conexion.cursor(dictionary=True)
    if request.method == 'POST':
        puesto = request.form['puesto']
        empresa = request.form['empresa']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        descripcion = request.form['descripcion']
        cursor.execute('UPDATE experiencia SET puesto = %s, empresa = %s, fecha_inicio = %s, fecha_fin = %s, descripcion = %s WHERE id = %s', (puesto, empresa, fecha_inicio, fecha_fin, descripcion, id))
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect(url_for('index'))
    cursor.execute('SELECT * FROM experiencia WHERE id = %s', (id,))
    experiencia_item = cursor.fetchone()
    cursor.close()
    conexion.close()
    return render_template('editar_experiencia.html', experiencia=experiencia_item)

@app.route('/borrar_experiencia/<int:id>')
@login_required
def borrar_experiencia(id):
    conexion = conectar_base_datos()
    if conexion is None:
        return "Error al conectar a la base de datos."
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM experiencia WHERE id = %s', (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
