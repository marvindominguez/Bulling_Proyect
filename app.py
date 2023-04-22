from flask import Flask, redirect, render_template, session, request, url_for, session, make_response
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'reporte'
app.secret_key = 'ghjklñ'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index_user')
def index_user():
    return render_template('index.html')


@app.route('/base')
def base():
    return render_template('admin/home.html')


@app.route('/index')
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
    return render_template('admin/register.html')


@app.route('/register_caso')  # Registrar Caso
def register_caso():
    return render_template('profesor/register.html')


@app.route('/login', methods=['Get', 'POST'])
def login():
    if request.method == 'POST':
        identificacion = request.form['documento']
        contraseña = request.form['contraseña']
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM login WHERE documento = %s AND contraseña = %s', (identificacion, contraseña))
        admin = cursor.fetchall()
        print(admin)
        if admin:
            return redirect(url_for('index_admin'))
        else:
            msg = 'Los datos ingresados son incorrectos'
            return render_template('admin/login.html')


@app.route('/login_p', methods=['POST'])
def login_p():
    msg = ''
    if request.method == 'POST':
        documento = request.form['documento']
        contraseña = request.form['contraseña']
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM login_profesor WHERE documento = %s AND contraseña = %s', (documento, contraseña))
        profe = cursor.fetchone()
        if profe:
            session['loggedin'] = True
            session['id_profesor'] = profe[0]
            session['nombre'] = profe[1]
            session['apellido'] = profe[2]
            session['correo'] = profe[3]
            session['celular'] = profe[4]
            session['documento'] = profe[5]
            return redirect(url_for('register_caso'))
        else:
            msg = 'Los datos ingresados son incorrectos'
            return render_template('profesor/login.html', msg=msg)


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
        cursor= mysql.connection.cursor()
        cursor.execute('INSERT INTO login_profesor (nombre, apellido, correo, documento, contraseña) VALUES (%s, %s, %s, %s, %s)',
                       (nombre, apellido, correo, cedula, contra))
        mysql.connection.commit()
        msg = 'El profesor ha sido registrado Correctamente'
    return render_template('admin/register.html', msg=msg)


@app.route('/registe_caso', methods=['POST', 'GET'])
def registe_caso():
    msg = ''
    if request.method == 'POST':
        id_profesor = request.form['id_profesor']
        semaforo = request.form['semaforo']
        observacion = request.form['observacion']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        curso_est = request.form['curso']
        edad = request.form['edad']
        fecha = request.form['hora']
        genero = request.form['genero']
        doc_est = request.form['doc_estudiante']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO r_caso (semaforo, observacion, id_estudiante, nombre, apellido, curso, edad, fecha_caso, genero, id_profesor) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                       (semaforo, observacion, doc_est, nombre, apellido, curso_est, edad, fecha, genero, id_profesor))
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


# Cerrar sesion
@app.route('/logout')
def logout():
    # removemos los datos de la sesión para cerrar sesión
    session.pop('loggedin', None)
    session.pop('id_profesor', None)
    session.pop('id_psicologo', None)
    session.pop('nombre', None)
    session.pop('apellido', None)
    session.pop('correo', None)
    session.pop('celular', None)
    session.pop('documento', None)
    session.pop('contraseña', None)
    session.clear()
    # Redirige a la pagina de login
    return redirect(url_for('index'))

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


if __name__ == '__main__':
    app.run(port=3000, debug=True)
