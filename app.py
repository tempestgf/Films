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

@app.route('/serie')
def serie():
    return render_template('daredevil.html')

@app.route('/serieuser')
def serieuser():
    return render_template('daredeviluser.html')

@app.route('/resenas')
def resenas():
    series = [
        {
            'nombre': 'Narcos',
            'temporadas': ['Temporada 1', 'Temporada 2', 'Temporada 3'],
            'reseñas': {
                'Temporada 1': 'Narcos nos introduce en el mundo del narcotráfico colombiano de manera magistral. Las actuaciones son excelentes y la trama es emocionante.',
                'Temporada 2': 'La segunda temporada de Narcos mantiene la calidad de la primera. La historia se vuelve aún más intensa y llena de giros inesperados.',
                'Temporada 3': 'Aunque la tercera temporada de Narcos sigue siendo interesante, algunos fans consideran que no alcanza el nivel de las anteriores. Aún así, es una serie que merece la pena ver.'
            }
        },
        {
            'nombre': 'Stranger Things',
            'temporadas': ['Temporada 1', 'Temporada 2', 'Temporada 3'],
            'reseñas': {
                'Temporada 1': 'Stranger Things nos transporta a la década de los 80 con su atmósfera nostálgica y su emocionante historia. Los personajes son carismáticos y la trama es intrigante desde el primer episodio.',
                'Temporada 2': 'La segunda temporada de Stranger Things expande el universo de la serie y profundiza en la mitología establecida en la primera temporada. Los nuevos personajes y los giros argumentales mantienen el interés del espectador.',
                'Temporada 3': 'Aunque la tercera temporada de Stranger Things es visualmente impresionante y llena de momentos emocionantes, algunos críticos consideran que la trama se vuelve un poco predecible en comparación con las temporadas anteriores.'
            }
        }
    ]
    return render_template('resenas.html', series=series)

@app.route('/ver_resena', methods=['POST'])
def ver_resena():
    serie = request.form['serie']
    temporada = request.form['temporada']
    series = [
        {
            'nombre': 'Narcos',
            'temporadas': ['Temporada 1', 'Temporada 2', 'Temporada 3'],
            'reseñas': {
                'Temporada 1': 'Excelente serie',
                'Temporada 2': 'Muy recomendada',
                'Temporada 3': 'Aún no hay reseña'
            }
        },
        {
            'nombre': 'Stranger Things',
            'temporadas': ['Temporada 1', 'Temporada 2', 'Temporada 3'],
            'reseñas': {
                'Temporada 1': 'Muy entretenida',
                'Temporada 2': 'Gran elenco de actores',
                'Temporada 3': 'Esperando reseñas'
            }
        }
    ]
    reseña = series[0]['reseñas'][temporada] if serie == 'Narcos' else series[1]['reseñas'][temporada]
    return render_template('resenas.html', serie=serie, temporada=temporada, reseña=reseña)



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
            return render_template('indexuser.html')
        else:
            flash('Nom d\'usuari o contrasenya incorrecta', 'error')
            return render_template('login.html')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
