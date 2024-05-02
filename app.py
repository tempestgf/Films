from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración de la conexión a la base de datos MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="films",
    password="films",
    database="resenas_series"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        platform = request.form['platform']
        theme = request.form['theme']
        series_name = request.form['series_name']
        season = request.form['season']
        description = request.form['description']
        year = request.form['year']
        awards = request.form['awards']
        cast = request.form['cast']
        region = request.form['region']

        cursor = mydb.cursor()
        sql = "INSERT INTO Series (Plataforma, Tematica, NomSerie, AnyInici, Premis, Repartiment, Regio) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (platform, theme, series_name, year, awards, cast, region)
        cursor.execute(sql, val)
        mydb.commit()

        serie_id = cursor.lastrowid

        sql = "INSERT INTO Temporades (SerieID, NumTemporada, Descripcio) VALUES (%s, %s, %s)"
        val = (serie_id, season, description)
        cursor.execute(sql, val)
        mydb.commit()

        cursor.close()

        return redirect(url_for('admin'))

    return render_template('admin.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.form['username']
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        # Verificar si hay campos vacíos
        if not all([username, name, surname, email, password, confirm_password]):
            flash('Por favor, completa todos los campos.', 'error')
            return render_template('register.html')

        # Verificar si el usuario ya existe en la base de datos
        cursor = mydb.cursor()
        sql = "SELECT * FROM Usuarios WHERE username = %s OR email = %s"
        val = (username, email)
        cursor.execute(sql, val)
        user = cursor.fetchone()

        if user:
            flash('Ya existe un usuario con este nombre de usuario o correo electrónico.', 'error')
            return render_template('register.html')

        # Verificar si las contraseñas coinciden
        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('register.html')

        # Insertar el nuevo usuario en la base de datos
        sql = "INSERT INTO Usuarios (username, name, surname, email, password) VALUES (%s, %s, %s, %s, %s)"
        val = (username, name, surname, email, password)
        cursor.execute(sql, val)
        mydb.commit()

        return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mydb.cursor()
        sql = "SELECT * FROM Usuarios WHERE username = %s AND password = %s"
        val = (username, password)
        cursor.execute(sql, val)
        user = cursor.fetchone()

        if user:
            session['username'] = user[1]
            return redirect(url_for('index'))
        else:
            flash('Nom d\'usuari o contrasenya incorrecta', 'error')
            return render_template('login.html')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
