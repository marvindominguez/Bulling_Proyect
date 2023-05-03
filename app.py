
from functools import wraps
from flask import Flask, redirect, render_template, session, request, url_for, session, make_response, flash
from flask_mysqldb import MySQL
from flask.wrappers import Request
from MySQLdb.cursors import Cursor
# from flask_login import LoginManager


app = Flask(__name__)
# login_manager = LoginManager()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'reportes'


mysql = MySQL(app)
app.secret_key = 'ghjklñ'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/index_user')
def index_user():
    return render_template('index.html')


@app.route('/base')
def base():
    return render_template('admin/home.html')


@app.route('/index')  # login Psicologo
def index():
    return render_template('admin/login.html')


@app.route('/index_admin')
def index_admin():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT r.id_caso, r.semaforo, r.observacion, r.id_estudiante, r.nombre, r.apellido, r.curso, r.edad, r.fecha_caso, r.genero, l.nombre FROM r_caso r INNER JOIN login_profesor l ON r.id_profesor = l.id_profesor")
    casos = cursor.fetchall()
    print(casos)
    return render_template('admin/index.html', casos=casos)


@app.route('/login_profe')
def login_profe():
    return render_template('profesor/login.html')


@app.route('/index_profe')
def index_profe():
    return render_template('profesor/index.html')


@app.route('/register')  # Registrar profesor
def register():
    datos = ['', '', '', '', '', '', '', '', '', '']
    return render_template('admin/register.html', datos=datos)


@app.route('/register_caso')  # Redireccionar Caso
def register_caso():
    return render_template('profesor/register.html')



@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        identificacion = request.form['documento']
        contraseña = request.form['contraseña']
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM login WHERE documento = %s AND contraseña = %s', (identificacion, contraseña))
        user = cursor.fetchone()
        # print(user)
        if user:

            return redirect(url_for('index_admin'))
        else:
            msg = 'Los datos ingresados son incorrectos'
            return render_template('admin/login.html', msg=msg)


@app.route('/login_p', methods=['POST'])
def login_p():
    msg = ''
    if request.method == 'POST':
        documentop = request.form['documento']
        contraseñap = request.form['contraseña']
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM login_profesor WHERE documento = %s AND contraseña = %s', (documentop, contraseñap))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['id_profesor'] = user[0]
            session['nombre'] = user[1]
            session['apellido'] = user[2]
            session['correo'] = user[3]
            session['celular'] = user[4]
            session['documento'] = user[5]
            return redirect(url_for('register_caso'))
        else:
            msg = 'Los datos ingresados son incorrectos'
            return render_template('profesor/login.html', msg=msg)
        
@app.route('/ver_casos')
def ver_casos():
    user = session['id_profesor']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT r.id_caso, r.semaforo, r.observacion, r.id_estudiante, r.nombre, r.apellido, r.curso, r.edad, r.fecha_caso, r.genero, l.nombre FROM r_caso r INNER JOIN login_profesor l ON r.id_profesor = l.id_profesor WHERE l.id_profesor=%s",(user,))
    v_casos = cursor.fetchall()
    return render_template('profesor/ver_casos.html', v_casos=v_casos)



# Cerrar sesion
@app.route('/logout')
def logout():
    # removemos los datos de la sesión para cerrar sesión
    session.pop('loggedin', None)
    session.pop('documento', None)
    session.pop('contraseña', None)
    session.clear()
    return redirect(url_for('index'))


@app.route('/res_profe', methods=['GET', 'POST'])  # Registrar Profe
def res_profe():
    msg = ''
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        cedula = request.form['documento']
        contra = request.form['contraseña']
        datos = [nombre, apellido, correo, cedula, contra]
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM login_profesor WHERE documento =%s', [str(cedula)])
        doc = cursor.fetchone()
        cursor.close()
        if doc:
            msg = 'El documento ya se encuentra registrado'
            return render_template('admin/register.html', msg=msg)
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO login_profesor (nombre, apellido, correo, documento, contraseña) VALUES (%s, %s, %s, %s, %s)',
                       (nombre, apellido, correo, cedula, contra))
        mysql.connection.commit()
        msg = 'El profesor ha sido registrado Correctamente'
    return render_template('admin/register.html', msg=msg)


@app.route('/registe_caso', methods=['POST'])
def registe_caso():
    if request.method == 'POST':
        search = request.form['buscar']
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM estudiante WHERE identificacion = %s', (search,))
        estudiante = cursor.fetchone()
        print(estudiante)
        return render_template('profesor/estudent_caso.html', estudiante=estudiante)


@app.route('/res_caso', methods=['POST'])
def res_caso():  # registe_caso
    id_profesor = request.form['id_profesor']
    semaforo = request.form['semaforo']
    nombre = request.form['nombre']
    observacion = request.form['observacion']
    curso_est = request.form['curse']
    apellido_est = request.form['apellido']
    edad = request.form['edad']
    fecha = request.form['hora']
    genero = request.form['genero']
    doc_est = request.form['identificacion']
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO r_caso (semaforo, observacion, id_estudiante, nombre, apellido, curso, edad, fecha_caso, genero, id_profesor) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                   (semaforo, observacion, doc_est, nombre, apellido_est, curso_est, edad, fecha, genero, id_profesor))
    mysql.connection.commit()
    msg = 'El caso ha sido registrado Correctamente'
    return render_template('profesor/register.html', msg=msg)


@app.route('/b_casos', methods=['POST'])  # Buscar Casos por Piscologo
def b_casos():
    if request.method == "POST":
        if request.method == "POST":
            search = request.form['buscar']
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT r.id_caso, r.semaforo, r.observacion, r.id_estudiante, r.nombre, r.apellido, r.curso, r.edad, r.fecha_caso, r.genero, l.nombre FROM r_caso r INNER JOIN login_profesor l ON r.id_profesor = l.id_profesor WHERE r.id_estudiante = %s", (search,))
            reporte = cursor.fetchall()
            print("los datos son", reporte)
            return render_template('admin/ver.html', reporte=reporte, busqueda=search)
    return redirect(url_for('index_admin'))


# Editar caso
@app.route('/editar_caso/<int:id>', methods=['POST', 'GET'])
def editar_caso(id):
    cursor = mysql.connection.cursor()
    query = " SELECT * FROM r_caso WHERE id_caso = %s"
    value = (id,)
    cursor.execute(query, value)
    datos = cursor.fetchone()
    if datos is None:
        msg = 'El caso no existe'
        return render_template('admin/index.html', msg=msg)
    if request.method == 'POST':
        semaforo = request.form['semaforo']
        observacion = request.form['observacion']
        curso_est = request.form['curse']
        edad = request.form['edad']
        fecha = request.form['hora']
        genero = request.form['genero']
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE r_caso SET semaforo = %s, observacion = %s, curso = %s, edad = %s, fecha_caso = %s, genero = %s WHERE id_caso = %s",
                       (semaforo, observacion, curso_est, edad, fecha, genero, id))
        mysql.connection.commit()
        msg = 'El caso ha sido actualizado Correctamente'
        return redirect(url_for('index_admin', msg=msg))
    # Actualizar caso
    return render_template('admin/update.html', datos=datos)


@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        query = 'DELETE FROM r_caso WHERE id_caso = %s'
        cursor.execute(query,(id,))
        mysql.connection.commit()
        cursor.close()
        msg = 'El caso ha sido eliminado Correctamente'
        return redirect(url_for('index_admin', msg=msg))


def status_401(error):
    return render_template('login')


def status_404(error):
    return '<h1>Página no encontrada</h1>', 404


if __name__ == '__main__':
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    # login_manager.init_app(app)
    app.run(port=5000, debug=True)
