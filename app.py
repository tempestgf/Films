from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración de la conexión a la base de datos MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="films",
    password="films",
    database="resenas_series"
)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file, filename, platform):
    directory = os.path.join(app.config['UPLOAD_FOLDER'], platform)
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, filename)
    file.save(file_path)
    return filename

@app.route('/')
def index():
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT s.SerieID, s.NomSerie, s.Plataforma, t.Descripcio, s.AnyInici, s.Premis, s.Repartiment, s.Regio, t.TrailerTemporada, t.ImatgeTemporada, s.Tematica FROM series s JOIN temporades t ON s.SerieID = t.SerieID WHERE s.Plataforma = 'Netflix'")
    netflix_series = cursor.fetchall()

    cursor.execute("SELECT s.SerieID, s.NomSerie, s.Plataforma, t.Descripcio, s.AnyInici, s.Premis, s.Repartiment, s.Regio, t.TrailerTemporada, t.ImatgeTemporada, s.Tematica FROM series s JOIN temporades t ON s.SerieID = t.SerieID WHERE s.Plataforma = 'HBO'")
    hbo_series = cursor.fetchall()

    cursor.execute("SELECT s.SerieID, s.NomSerie, s.Plataforma, t.Descripcio, s.AnyInici, s.Premis, s.Repartiment, s.Regio, t.TrailerTemporada, t.ImatgeTemporada, s.Tematica FROM series s JOIN temporades t ON s.SerieID = t.SerieID WHERE s.Plataforma = 'Disney Plus'")
    disneyplus_series = cursor.fetchall()

    
    print("Netflix Series:", netflix_series)
    print("HBO Series:", hbo_series)
    print("Disney Plus Series:", disneyplus_series)
    
    # Asegúrate de que cada serie tenga las claves 'ImatgeTemporada' y 'Tematica' antes de pasarlas a la plantilla
    for serie in netflix_series:
        if 'ImatgeTemporada' not in serie:
            serie['ImatgeTemporada'] = ''  # O proporciona un valor predeterminado
        if 'Tematica' not in serie:
            serie['Tematica'] = ''  # O proporciona un valor predeterminado

    for serie in hbo_series:
        if 'ImatgeTemporada' not in serie:
            serie['ImatgeTemporada'] = ''  # O proporciona un valor predeterminado
        if 'Tematica' not in serie:
            serie['Tematica'] = ''  # O proporciona un valor predeterminado

    for serie in disneyplus_series:
        if 'ImatgeTemporada' not in serie:
            serie['ImatgeTemporada'] = ''  # O proporciona un valor predeterminado
        if 'Tematica' not in serie:
            serie['Tematica'] = ''  # O proporciona un valor predeterminado

    # Dividir las series en lotes de 3 para mostrarlas en el carrusel
    netflix_batches = [netflix_series[i:i+3] for i in range(0, len(netflix_series), 3)]
    hbo_batches = [hbo_series[i:i+3] for i in range(0, len(hbo_series), 3)]
    disneyplus_batches = [disneyplus_series[i:i+3] for i in range(0, len(disneyplus_series), 3)]

    return render_template('index.html', netflix_batches=netflix_batches, hbo_batches=hbo_batches, disneyplus_batches=disneyplus_batches)



@app.route('/resenas')
def resenas():
    if 'username' not in session:
        flash('Debes iniciar sesión para ver tus reseñas.', 'error')
        return redirect(url_for('login'))

    cursor = mydb.cursor(dictionary=True)
    username = session['username']
    cursor.execute("SELECT s.NomSerie, t.NumTemporada, r.Critica FROM resenyes r JOIN temporades t ON r.TemporadaID = t.TemporadaID JOIN series s ON t.SerieID = s.SerieID WHERE r.NomUsuari = %s", (username,))
    user_reviews = cursor.fetchall()
    cursor.close()

    return render_template('resenas.html', user_reviews=user_reviews)

@app.route('/editar_usuario', methods=['GET', 'POST'])
def editar_usuario():
    if 'username' not in session:
        flash('Debes iniciar sesión para editar tus detalles.', 'error')
        return redirect(url_for('login'))

    if request.method == 'GET':
        # Obtener los detalles actuales del usuario
        cursor = mydb.cursor(dictionary=True)
        username = session['username']
        cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        return render_template('editar_usuario.html', user=user)
    elif request.method == 'POST':
        # Actualizar los detalles del usuario en la base de datos
        username = request.form['username']
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']

        cursor = mydb.cursor()
        cursor.execute("UPDATE usuarios SET name = %s, surname = %s, email = %s WHERE username = %s", (name, surname, email, username))
        mydb.commit()
        cursor.close()

        flash('Tus detalles han sido actualizados correctamente.', 'success')
        return redirect(url_for('editar_usuario'))
    
@app.route('/buscar_series', methods=['GET'])
def buscar_series():
    if request.method == 'GET':
        query = request.args.get('query')  # Obtener el término de búsqueda del parámetro 'query' en la URL
        cursor = mydb.cursor(dictionary=True)
        # Consulta SQL para buscar series que coincidan con el término de búsqueda en el nombre de la serie o en la descripción
        sql = "SELECT s.SerieID, s.NomSerie, s.Plataforma, t.Descripcio, s.Tematica, s.AnyInici, s.Premis, s.Repartiment, s.Regio, t.TrailerTemporada, t.ImatgeTemporada FROM series s JOIN temporades t ON s.SerieID = t.SerieID WHERE s.NomSerie LIKE %s OR t.Descripcio LIKE %s"
        # Utilizamos % para permitir búsquedas parciales
        cursor.execute(sql, ('%' + query + '%', '%' + query + '%'))
        search_results = cursor.fetchall()
        cursor.close()
        return render_template('search_results.html', search_results=search_results, query=query)


@app.route('/serie/<int:serie_id>', methods=['GET', 'POST'])
def serie(serie_id):
    if request.method == 'GET':
        # Obtener los detalles de la serie de la base de datos
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.NomSerie, s.Plataforma, t.Descripcio, s.AnyInici, s.Premis, s.Repartiment, s.Regio, t.TrailerTemporada, t.NumTemporada, t.ImatgeTemporada, t.TemporadaID, s.SerieID, s.Tematica
            FROM series s
            JOIN temporades t ON s.SerieID = t.SerieID
            WHERE s.SerieID = %s
        """, (serie_id,))
        serie = cursor.fetchone()

        # Asegúrate de que el diccionario serie tenga la clave 'ImatgeTemporada' antes de pasarla a la plantilla
        if 'ImatgeTemporada' not in serie:
            serie['ImatgeTemporada'] = ''  # O proporciona un valor predeterminado

        # Recuperar las reseñas para esta temporada de la base de datos
        cursor.execute("SELECT * FROM resenyes WHERE TemporadaID = %s", (serie['TemporadaID'],))  # Usar serie['TemporadaID'] aquí
        reviews = cursor.fetchall()

        cursor.close()

        # Aquí asegúrate de que cada reseña tenga las propiedades adecuadas
        reviews_with_properties = []
        for review in reviews:
            review_with_properties = {
                'NomUsuari': review['NomUsuari'],
                'Critica': review['Critica'],
                'DataResenya': review['DataResenya'],
                'Puntuacio': review['Puntuacio']
            }
            reviews_with_properties.append(review_with_properties)

        # Calcular la media de las puntuaciones de las reseñas
        total_puntuacion = 0
        num_resenyes = len(reviews)
        for review in reviews:
            total_puntuacion += review['Puntuacio']

        if num_resenyes > 0:
            media_puntuacion = total_puntuacion / num_resenyes
        else:
            media_puntuacion = 0

        # Redondear la media de puntuación a un solo decimal
        media_puntuacion = round(media_puntuacion, 1)

        return render_template('serie.html', serie=serie, reviews=reviews_with_properties, media_puntuacion=media_puntuacion)

    elif request.method == 'POST':
        if 'username' not in session:
            flash('Debes iniciar sesión para dejar una reseña.', 'error')
            return redirect(url_for('login'))

        # Obtener los datos del formulario
        review = request.form['review']
        
        # Verificar si la clave 'rating' está presente en request.form
        if 'rating' not in request.form:
            flash('La puntuación es obligatoria.', 'error')
            return redirect(url_for('serie', serie_id=serie_id))
            
        rating = request.form['rating']
        username = session['username']

        # Validar los datos del formulario
        if not review or not rating:
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('serie', serie_id=serie_id))

        # Verificar si el comentario está vacío
        if not review.strip():  # strip() elimina los espacios en blanco al principio y al final
            flash('Debes dejar un comentario para enviar una reseña.', 'error')
            return redirect(url_for('serie', serie_id=serie_id))

        # Obtener los detalles de la serie de la base de datos
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.NomSerie, t.TemporadaID
            FROM series s
            JOIN temporades t ON s.SerieID = t.SerieID
            WHERE s.SerieID = %s
        """, (serie_id,))
        serie_details = cursor.fetchone()

        try:
            # Convertir el rating a int
            rating = int(rating)
        except ValueError:
            flash('La puntuación debe ser un número entero.', 'error')
            cursor.close()
            return redirect(url_for('serie', serie_id=serie_id))

        cursor.execute("""
            INSERT INTO resenyes (TemporadaID, NomUsuari, Critica, DataResenya, Puntuacio)
            VALUES (%s, %s, %s, CURDATE(), %s)
        """, (serie_details['TemporadaID'], username, review, rating))

        mydb.commit()
        flash('Tu reseña ha sido enviada con éxito.', 'success')
        cursor.close()

        # Luego, redirigir de vuelta a la página de la serie después de enviar
    return redirect(url_for('serie', serie_id=serie_id))




@app.context_processor
def inject_es_administrador():
    return dict(es_administrador=es_administrador)

ADMIN_USERS = ['admin', 'superadmin']

def es_administrador(username):
    return username in ADMIN_USERS

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    print("Debug: Se alcanzó la ruta '/admin'")
    if 'username' in session:
        username = session['username']
        if es_administrador(username):
            serie_id = 1  # Definir serie_id con un valor por defecto
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

                image = request.files['image']
                trailer = request.files['trailer']
                image_filename = None
                trailer_filename = None

                if image and allowed_file(image.filename):
                    image_filename = save_file(image, secure_filename(image.filename), platform)

                if trailer and allowed_file(trailer.filename) and trailer.filename.endswith('.mp4'):
                    trailer_filename = save_file(trailer, secure_filename(trailer.filename), platform)

                # Validar campos obligatorios
                if not platform or not theme or not series_name or not season or not description or not year:
                    flash('Todos los campos son obligatorios.', 'error')
                    return redirect(url_for('admin'))

                # Validar archivos subidos
                if not image_filename:
                    flash('Formato de archivo de imagen no permitido o no proporcionado.', 'error')
                    return redirect(url_for('admin'))

                if not trailer_filename:
                    flash('Formato de archivo de vídeo no permitido o no proporcionado.', 'error')
                    return redirect(url_for('admin'))

                cursor = mydb.cursor()
                sql = "INSERT INTO series (Plataforma, Tematica, NomSerie, AnyInici, Premis, Repartiment, Regio) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = (platform, theme, series_name, year, awards, cast, region)
                cursor.execute(sql, val)
                mydb.commit()

                serie_id = cursor.lastrowid

                sql = "INSERT INTO temporades (SerieID, NumTemporada, Descripcio, ImatgeTemporada, TrailerTemporada) VALUES (%s, %s, %s, %s, %s)"
                val = (serie_id, season, description, image_filename, trailer_filename)
                cursor.execute(sql, val)
                mydb.commit()

                cursor.close()

                flash('La serie se ha agregado correctamente.', 'success')
                return redirect(url_for('admin'))

            elif request.method == 'GET' and 'delete' in request.args:
                serie_id = request.args['delete']
                cursor = mydb.cursor()
                cursor.execute("SELECT ImatgeTemporada, TrailerTemporada FROM temporades WHERE SerieID = %s", (serie_id,))
                files = cursor.fetchone()
                if files:
                    for file_path in files:
                        if file_path:
                            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file_path))
                cursor.execute("DELETE FROM temporades WHERE SerieID = %s", (serie_id,))
                mydb.commit()
                cursor.execute("DELETE FROM series WHERE SerieID = %s", (serie_id,))
                mydb.commit()
                cursor.close()
                flash('La serie se ha eliminado correctamente.', 'success')
                return redirect(url_for('admin'))

            return render_template('admin.html', serie_id=serie_id)  # Pasar serie_id al renderizar la plantilla
        else:
            flash('Acceso no autorizado. Debes ser un administrador.', 'error')
            return redirect(url_for('index'))
    else:
        flash('Debes iniciar sesión como administrador.', 'error')
        return redirect(url_for('login'))

@app.route('/eliminar_serie', methods=['POST'])
def eliminar_serie():
    if request.method == 'POST':
        serie_id = request.form.get('serie_id')
        if serie_id:
            cursor = mydb.cursor()
            try:
                # Eliminar la serie de la tabla temporadas primero
                sql = "DELETE FROM temporades WHERE SerieID = %s"
                cursor.execute(sql, (serie_id,))
                
                # Luego, eliminar la serie de la tabla series
                sql = "DELETE FROM series WHERE SerieID = %s"
                cursor.execute(sql, (serie_id,))
                
                mydb.commit()
                
                cursor.close()
                
                flash('La serie se ha eliminado correctamente.', 'success')
            except Exception as e:
                print("Error al eliminar la serie:", e)
                mydb.rollback()
                flash('Error al eliminar la serie.', 'error')
                
    return redirect(url_for('admin'))

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
            return redirect(url_for('index'))  # Redirige al usuario a la página principal después del inicio de sesión

        # Verifica si es el inicio de sesión del administrador
        if username == 'admin' and password == 'admin':
            session['admin'] = True
            return redirect(url_for('admin'))  # Redirige al administrador a su panel de control

        flash('Credenciales incorrectas. Inténtalo de nuevo.', 'error')
    
    return render_template('login.html')


import logging

@app.route('/submit_review', methods=['POST'])
def submit_review():
    logging.info(f"Form data: {request.form}")
    
    if 'username' not in session:
        flash('Debes iniciar sesión para dejar una reseña.', 'error')
        return redirect(url_for('login'))

    # Obtener los datos del formulario
    temporada_id = request.form.get('temporada_id')
    serie_id = request.form.get('serie_id')
    review = request.form.get('critica')
    rating = request.form.get('puntuacio')
    username = session['username']

    logging.info(f"Temporada ID: {temporada_id}, Serie ID: {serie_id}, Review: {review}, Rating: {rating}, Username: {username}")

    # Validar los datos del formulario
    if not review or not rating or not serie_id:
        flash('Todos los campos son obligatorios.', 'error')
        return redirect(url_for('serie', serie_id=serie_id))

    try:
        # Convertir el rating y serie_id a int
        rating = int(rating)
        serie_id = int(serie_id)
    except ValueError:
        flash('La puntuación y el ID de la serie deben ser números enteros.', 'error')
        return redirect(url_for('serie', serie_id=serie_id if serie_id else 0))

    cursor = mydb.cursor()
    try:
        cursor.execute("""
            INSERT INTO resenyes (TemporadaID, NomUsuari, Critica, DataResenya, Puntuacio)
            VALUES (%s, %s, %s, CURDATE(), %s)
        """, (temporada_id, username, review, rating))

        mydb.commit()
        flash('Tu reseña ha sido enviada con éxito.', 'success')

    except mysql.connector.Error as error:
        flash('Error al enviar la reseña: {}'.format(error), 'error')
        print(error)
        mydb.rollback()

    cursor.close()

    # Luego, redirigir de vuelta a la página de la serie después de enviar la reseña
    return redirect(url_for('serie', serie_id=serie_id))

@app.route('/logout')
def logout():
    session.pop('username', None)  
    #flash('You have been logged out.', 'success')  
    return redirect(url_for('index'))  






if __name__ == '__main__':
    #app.run(debug=True)
    #app.run(host='192.168.1.40')
    app.run(host='192.168.1.40', port=5000)
