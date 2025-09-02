from flask import Flask, render_template, request, redirect, flash, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime  
from flask import jsonify
from flask import Flask, render_template, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.secret_key = '8f7asdhjk2347asdhjkljh23lkj4hkjl34h23kj4h'

db = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345678',
    'database': 'mi_base'
}

def crear_tablas():
    conn = mysql.connector.connect(**db)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS testimonios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            mensaje TEXT NOT NULL,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            aprobado BOOLEAN DEFAULT 0
        );
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS nueva_admision (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre_estudiante VARCHAR(100),
            edad INT,
            dni_estudiante VARCHAR(20),
            grado VARCHAR(50),
            colegio_anterior VARCHAR(100),
            nombre_tutor VARCHAR(100),
            dni_tutor VARCHAR(20),
            direccion TEXT,
            telefono VARCHAR(20),
            email VARCHAR(100),
            condiciones TEXT,
            vacunado VARCHAR(10),
            observaciones TEXT,
            estado VARCHAR(20) DEFAULT 'pendiente',
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS profesores (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100),
            area VARCHAR(100),
            foto VARCHAR(200),
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    ip_usuario = request.remote_addr
    conn = mysql.connector.connect(**db)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO visitas (ip) VALUES (%s)", (ip_usuario,))
    conn.commit()
    conn.close()
    return render_template('index.html')

@app.route('/primaria')
def primaria():
    conn = mysql.connector.connect(**db)
    c = conn.cursor(dictionary=True)

    # Obtener testimonios SOLO de primaria
    c.execute("SELECT * FROM testimonios WHERE nivel = 'Primaria' ORDER BY id DESC")
    testimonios = c.fetchall()

    # Obtener noticias de nivel primaria
    c.execute("SELECT * FROM noticias WHERE nivel = 'primaria' ORDER BY fecha DESC")
    noticias = c.fetchall()

    conn.close()
    return render_template('primaria.html', testimonios=testimonios, noticias=noticias) 

@app.route('/secundaria')
def secundaria():
    conn = mysql.connector.connect(**db)
    c = conn.cursor(dictionary=True)

    # Obtener testimonios SOLO de secundaria
    c.execute("SELECT * FROM testimonios WHERE nivel = 'Secundaria' ORDER BY id DESC")
    testimonios = c.fetchall()

    # Obtener noticias de nivel secundaria
    c.execute("SELECT * FROM noticias WHERE nivel = 'secundaria' ORDER BY fecha DESC")
    noticias = c.fetchall()

    conn.close()
    return render_template('secundaria.html', testimonios=testimonios, noticias=noticias)

@app.route('/submit_testimonio', methods=['POST'])
def submit_testimonio():
    nombre = request.form.get('nombre', '').strip()
    correo = request.form.get('correo', '').strip().lower()
    mensaje = request.form.get('mensaje', '').strip()
    nivel = request.form.get('nivel', '').strip()  # 🔥 nivel desde el formulario

    if not nombre or not mensaje or not correo or not nivel:
        flash('Por favor completa todos los campos.', 'error')
        return redirect(request.referrer or url_for('index'))

    partes_nombre = nombre.split()
    if len(partes_nombre) < 2:
        flash('Debes ingresar al menos dos nombres y apellidos.', 'error')
        return redirect(request.referrer or url_for('index'))

    if partes_nombre[0].lower() not in correo:
        flash('El correo debe incluir tu nombre.', 'error')
        return redirect(request.referrer or url_for('index'))

    prohibidas = ['maldicion', 'fuck', 'shit', 'mierda']
    for palabra in prohibidas:
        if palabra.lower() in mensaje.lower():
            flash('El testimonio contiene palabras no permitidas.', 'error')
            return redirect(request.referrer or url_for('index'))

    conn = mysql.connector.connect(**db)
    c = conn.cursor()
    c.execute('INSERT INTO testimonios (nombre, testimonio, nivel) VALUES (%s, %s, %s)', (nombre, mensaje, nivel))
    conn.commit()
    conn.close()

    flash('Tu testimonio fue enviado y está pendiente de aprobación.', 'success')

    # Redirección según el nivel
    if nivel.lower() == 'primaria':
        return redirect(url_for('primaria'))
    elif nivel.lower() == 'secundaria':
        return redirect(url_for('secundaria'))
    else:
        return redirect(url_for('index'))

@app.route('/submit_admision', methods=['POST'])
def submit_admision():
    nombre = request.form.get('nombre', '').strip()
    dni = request.form.get('dni', '').strip()
    fecha_nac = request.form.get('fecha_nacimiento', '')
    nivel = request.form.get('nivel', '').strip()
    correo = request.form.get('correo', '').strip()
    telefono = request.form.get('telefono', '').strip()
    mensaje = request.form.get('mensaje', '').strip()
    if not nombre or not dni or not nivel:
        flash('Nombre, DNI y nivel son obligatorios.', 'error')
        return redirect('/')

    conn = mysql.connector.connect(**db)
    c = conn.cursor()
    c.execute(
        'INSERT INTO admision (nombre, dni, fecha_nacimiento, nivel, correo, telefono, mensaje) '
        'VALUES (%s, %s, %s, %s, %s, %s, %s)',
        (nombre, dni, fecha_nac, nivel, correo, telefono, mensaje)
    )
    conn.commit()
    conn.close()
    flash('Solicitud de admisión enviada correctamente.', 'success')
    return redirect('/')

@app.route('/matricula', methods=['POST'])
def matricula():
    # Validación de acceso
    if 'rol' not in session or session['rol'] != 'padre':
        flash('Acceso no autorizado.', 'error')
        return redirect('/')

    # Capturar datos del formulario
    nombreAlumno = request.form.get('nombreAlumno', '').strip()
    edadAlumno = request.form.get('edadAlumno', '').strip()
    dniAlumno = request.form.get('dniAlumno', '').strip()
    grado = request.form.get('grado', '').strip()
    colegioAnterior = request.form.get('colegioAnterior', '').strip()
    nombrePadre = request.form.get('nombrePadre', '').strip()
    dniPadre = request.form.get('dniPadre', '').strip()
    direccion = request.form.get('direccion', '').strip()
    telefono = request.form.get('telefono', '').strip()
    email = request.form.get('email', '').strip()
    estadoSalud = request.form.get('estadoSalud', '').strip()
    vacunado = request.form.get('vacunado', '').strip()
    observaciones = request.form.get('observaciones', '').strip()

    # Validar campos obligatorios
    if not (nombreAlumno and edadAlumno and dniAlumno and grado and nombrePadre and dniPadre and direccion and telefono and email):
        flash('Por favor completa todos los campos obligatorios.', 'error')
        return redirect('/')

    conn = mysql.connector.connect(**db)
    c = conn.cursor()

    try:
        c.execute(
            '''INSERT INTO nueva_admision (
                nombre_estudiante, edad, dni_estudiante, grado, colegio_anterior,
                nombre_tutor, dni_tutor, direccion, telefono, email,
                condiciones, vacunado, observaciones, estado
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
            (
                nombreAlumno, edadAlumno, dniAlumno, grado, colegioAnterior,
                nombrePadre, dniPadre, direccion, telefono, email,
                estadoSalud, vacunado, observaciones, 'pendiente'
            )
        )
        conn.commit()
        flash('¡Gracias! Tu matrícula ha sido enviada correctamente. Nos contactaremos pronto.', 'success')
    except Exception as e:
        flash('Error al guardar la matrícula: ' + str(e), 'error')
    finally:
        conn.close()

    return redirect('/') 
    


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombres = request.form.get('nombres', '').strip()
        apellidos = request.form.get('apellidos', '').strip()
        dni = request.form.get('dni', '').strip()
        correo = request.form.get('correo', '').strip()
        celular = request.form.get('celular', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if not all([nombres, apellidos, dni, correo, celular, password, confirm_password]):
            flash('Completa todos los campos.', 'error')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'error')
            return redirect(url_for('register'))

        if not dni.isdigit() or len(dni) != 8:
            flash('El DNI debe tener exactamente 8 dígitos numéricos.', 'error')
            return redirect(url_for('register'))

        if not celular.isdigit() or len(celular) != 9:
            flash('El número de celular debe tener exactamente 9 dígitos numéricos.', 'error')
            return redirect(url_for('register'))

        if not nombres.replace(" ", "").isalpha() or not apellidos.replace(" ", "").isalpha():
            flash('Los nombres y apellidos deben contener solo letras.', 'error')
            return redirect(url_for('register'))

        conn = mysql.connector.connect(**db)
        c = conn.cursor()

        c.execute('SELECT id FROM usuarios WHERE correo = %s', (correo,))
        if c.fetchone():
            flash('Ese correo ya está registrado.', 'error')
            conn.close()
            return redirect(url_for('register'))

        c.execute('SELECT id FROM usuarios WHERE dni = %s', (dni,))
        if c.fetchone():
            flash('Ese DNI ya está registrado.', 'error')
            conn.close()
            return redirect(url_for('register'))

        hash_pass = generate_password_hash(password)
        c.execute('''
            INSERT INTO usuarios (nombres, apellidos, dni, correo, celular, password, creado_por_usuario)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (nombres, apellidos, dni, correo, celular, hash_pass, True))

        conn.commit()
        conn.close()

        flash('Registro exitoso. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']

        conn = mysql.connector.connect(**db)
        c = conn.cursor(dictionary=True)
        c.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        usuario = c.fetchone()
        conn.close()

        if usuario and check_password_hash(usuario['password'], password):
            session['usuario_id'] = usuario['id']
            session['nombre'] = f"{usuario['nombres']} {usuario['apellidos']}"  # ✅ Corregido aquí
            session['rol'] = usuario['rol']

            if usuario['rol'] == 'admin':
                return redirect(url_for('admin_panel'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Correo o contraseña incorrectos.', 'error')
            return render_template('login.html')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('login'))


@app.route('/admin')
def admin_panel():
    if 'usuario_id' not in session:
        flash('Debes iniciar sesión.', 'error')
        return redirect(url_for('admin_login'))

    if session.get('rol') != 'admin':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('index'))

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  

    return render_template('admin.html', nombre=session.get('nombre'), fecha=fecha)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']  # <--- debe ser "password"

        conn = mysql.connector.connect(**db)
        c = conn.cursor(dictionary=True)
        c.execute("SELECT * FROM usuarios WHERE correo = %s AND rol = 'admin'", (correo,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['usuario_id'] = user['id']
            session['nombre'] = user['nombre']
            session['rol'] = user['rol']
            return redirect(url_for('admin_panel'))
        else:
            flash('Acceso restringido o credenciales inválidas.', 'error')

    return render_template('admin_login.html')

@app.route('/api/matriculas')
def obtener_matriculas():
    if 'usuario_id' not in session or session.get('rol') != 'admin':
        return jsonify({'error': 'No autorizado'}), 403

    orden = request.args.get('orden', 'DESC').upper()
    if orden not in ['ASC', 'DESC']:
        orden = 'DESC'

    conn = mysql.connector.connect(**db)
    c = conn.cursor(dictionary=True)
    c.execute(f"SELECT * FROM nueva_admision WHERE estado = 'pendiente' ORDER BY fecha {orden}")
    datos = c.fetchall()
    conn.close()
    return jsonify(datos) 


@app.route('/aprobar_matricula/<int:matricula_id>', methods=['POST'])
def aprobar_matricula(matricula_id):
    if 'usuario_id' not in session or session.get('rol') != 'admin':
        return jsonify({'error': 'No autorizado'}), 403

    conn = mysql.connector.connect(**db)
    c = conn.cursor()
    c.execute("UPDATE nueva_admision SET estado = 'aprobado' WHERE id = %s", (matricula_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


@app.route('/rechazar_matricula/<int:matricula_id>', methods=['POST'])
def rechazar_matricula(matricula_id):
    if 'usuario_id' not in session or session.get('rol') != 'admin':
        return jsonify({'error': 'No autorizado'}), 403

    conn = mysql.connector.connect(**db)
    c = conn.cursor()
    c.execute("UPDATE nueva_admision SET estado = 'rechazado' WHERE id = %s", (matricula_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/exportar_matriculas')
def exportar_matriculas():
    if 'usuario_id' not in session or session.get('rol') != 'admin':
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('admin_panel'))

    import pandas as pd

    conn = mysql.connector.connect(**db)
    df = pd.read_sql("SELECT * FROM nueva_admision ORDER BY fecha DESC", conn)
    conn.close()

    archivo = 'matriculas_exportadas.xlsx'
    df.to_excel(archivo, index=False)

    from flask import send_file
    return send_file(archivo, as_attachment=True)

@app.route('/api/profesores', methods=['GET', 'POST'])
def profesores():
    if 'usuario_id' not in session or session.get('rol') != 'admin':
        return jsonify({'error': 'No autorizado'}), 403

    if request.method == 'GET':
        conn = mysql.connector.connect(**db)
        c = conn.cursor(dictionary=True)
        c.execute("SELECT * FROM profesores ORDER BY fecha DESC")
        profesores = c.fetchall()
        conn.close()
        return jsonify(profesores)

    elif request.method == 'POST':
        data = request.json
        nombre = data.get('nombre')
        area = data.get('area')
        foto = data.get('foto', 'user.jpg')

        conn = mysql.connector.connect(**db)
        c = conn.cursor()
        c.execute("INSERT INTO profesores (nombre, area, foto) VALUES (%s, %s, %s)", (nombre, area, foto))
        conn.commit()
        conn.close()
        return jsonify({'mensaje': 'Profesor agregado exitosamente'})

@app.route('/api/profesores/<int:profesor_id>', methods=['PUT'])
def editar_profesor(profesor_id):
    if 'usuario_id' not in session or session.get('rol') != 'admin':
        return jsonify({'error': 'No autorizado'}), 403

    data = request.json
    nombre = data.get('nombre')
    area = data.get('area')
    foto = data.get('foto', 'user.jpg')

    conn = mysql.connector.connect(**db)
    c = conn.cursor()
    c.execute("UPDATE profesores SET nombre=%s, area=%s, foto=%s WHERE id=%s", (nombre, area, foto, profesor_id))
    conn.commit()
    conn.close()
    return jsonify({'mensaje': 'Profesor actualizado exitosamente'})

@app.route('/api/profesores/<int:profesor_id>', methods=['DELETE'])
def eliminar_profesor(profesor_id):
    if 'usuario_id' not in session or session.get('rol') != 'admin':
        return jsonify({'error': 'No autorizado'}), 403

    conn = mysql.connector.connect(**db)
    c = conn.cursor()
    c.execute("DELETE FROM profesores WHERE id=%s", (profesor_id,))
    conn.commit()
    conn.close()
    return jsonify({'mensaje': 'Profesor eliminado exitosamente'})


    

@app.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    rol = data.get('rol')

    if not username or not password or not rol:
        return jsonify({'error': 'Faltan datos'}), 400

    hashed_password = generate_password_hash(password)

    try:
        conn = mysql.connector.connect(**db)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios_admin (username, password, rol) VALUES (%s, %s, %s)",
            (username, hashed_password, rol)
        )
        conn.commit()
        return jsonify({'message': 'Usuario agregado exitosamente'})
    except mysql.connector.errors.IntegrityError:
        return jsonify({'error': 'El usuario ya existe'}), 400
    finally:
        conn.close()

@app.route('/api/usuarios')
def obtener_usuarios():
    conn = mysql.connector.connect(**db)
    cursor = conn.cursor(dictionary=True)

    
    cursor.execute("SELECT id, username, rol FROM usuarios_admin")
    usuarios = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(usuarios)



@app.route('/agregar_noticia', methods=['POST'])
def agregar_noticia():
    if 'usuario_id' not in session or session.get('rol') != 'admin':
        return jsonify({'error': 'No autorizado'}), 403

    nivel = request.form.get('nivel')
    titulo = request.form.get('titulo')
    contenido = request.form.get('contenido')
    imagen = request.files.get('imagen')

    if not (nivel and titulo and contenido):
        return jsonify({'error': 'Faltan campos'}), 400

    nombre_archivo = None
    if imagen:
        nombre_archivo = secure_filename(imagen.filename)
        ruta = os.path.join('static/img', nombre_archivo)
        imagen.save(ruta)

    conn = mysql.connector.connect(**db)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO noticias (titulo, contenido, nivel, imagen) VALUES (%s, %s, %s, %s)",
        (titulo, contenido, nivel, nombre_archivo)
    )
    conn.commit()
    conn.close()

    return jsonify({'message': 'Noticia publicada exitosamente'})

@app.route('/api/noticias')
def api_noticias():
    if 'usuario_id' not in session or session.get('rol') != 'admin':
        return jsonify({'error': 'No autorizado'}), 403

    conn = mysql.connector.connect(**db)
    c = conn.cursor(dictionary=True)
    c.execute("SELECT * FROM noticias ORDER BY fecha DESC")
    noticias = c.fetchall()
    conn.close()
    return jsonify(noticias)

@app.route('/eliminar_noticia/<int:id>', methods=['DELETE'])
def eliminar_noticia(id):
    if 'usuario_id' not in session or session.get('rol') != 'admin':
        return jsonify({'error': 'No autorizado'}), 403

    conn = mysql.connector.connect(**db)
    c = conn.cursor()
    # Obtener nombre de la imagen antes de eliminar
    c.execute("SELECT imagen FROM noticias WHERE id = %s", (id,))
    img = c.fetchone()
    if img and img[0]:
        try:
            os.remove(os.path.join('static/noticias', img[0]))
        except:
            pass

    c.execute("DELETE FROM noticias WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Noticia eliminada'})

@app.route('/editar_noticia/<int:id>', methods=['POST'])
def editar_noticia(id):
    if 'usuario_id' not in session or session.get('rol') != 'admin':
        return jsonify({'error': 'No autorizado'}), 403

    nivel = request.form.get('nivel')
    titulo = request.form.get('titulo')
    contenido = request.form.get('contenido')
    imagen = request.files.get('imagen')

    conn = mysql.connector.connect(**db)
    c = conn.cursor()

    if imagen:
        nombre_archivo = secure_filename(imagen.filename)
        ruta = os.path.join('static/noticias', nombre_archivo)
        imagen.save(ruta)
        c.execute("UPDATE noticias SET titulo=%s, contenido=%s, nivel=%s, imagen=%s WHERE id=%s",
                  (titulo, contenido, nivel, nombre_archivo, id))
    else:
        c.execute("UPDATE noticias SET titulo=%s, contenido=%s, nivel=%s WHERE id=%s",
                  (titulo, contenido, nivel, id))

    conn.commit()
    conn.close()
    return jsonify({'message': 'Noticia editada'})

@app.route('/api/registrados')
def obtener_registrados():
    conn = mysql.connector.connect(**db)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, correo AS username, rol FROM usuarios WHERE creado_por_usuario = TRUE")
    registros = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(registros)

@app.route('/asignar_rol/<int:user_id>', methods=['POST'])
def asignar_rol(user_id):
    data = request.get_json()
    nuevo_rol = data.get('rol')

    conn = mysql.connector.connect(**db)
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET rol = %s WHERE id = %s", (nuevo_rol, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Rol asignado correctamente'})

@app.route('/api/estadisticas')
def api_estadisticas():
    if 'usuario_id' not in session or session.get('rol') != 'admin':
        return jsonify({'error': 'No autorizado'}), 403

    try:
        conn = mysql.connector.connect(**db)
        cursor = conn.cursor()

        # Total de visitas
        cursor.execute("SELECT COUNT(*) FROM visitas")  # Asegúrate de tener esta tabla
        total_visitas = cursor.fetchone()[0]

        # Total de matrículas
        cursor.execute("SELECT COUNT(*) FROM nueva_admision")
        total_matriculas = cursor.fetchone()[0]

        # Total de profesores
        cursor.execute("SELECT COUNT(*) FROM profesores")
        total_profesores = cursor.fetchone()[0]

        conn.close()

        return jsonify({
            'visitas': total_visitas,
            'matriculas': total_matriculas,
            'profesores': total_profesores
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
    

if __name__ == '__main__':
    crear_tablas()
    app.run(debug=True)








