from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# CONEXION A MONGODB
cadena = "mongodb+srv://mruelas036_db_user:JossAngel22@cluster0.lyk7fig.mongodb.net/?appName=Cluster0"

cliente = MongoClient(cadena)

db = cliente["EscuelaDB"]

# PAGINA PRINCIPAL
@app.route('/')
def inicio():
    return render_template('index.html')

# PAGINA MAESTROS
@app.route('/maestros')
def maestros():
    return render_template('maestros.html')

# GUARDAR MAESTRO
@app.route('/guardar_maestro', methods=['POST'])
def guardar_maestro():

    numero_empleado = request.form['numero_empleado']
    nombre = request.form['nombre']
    correo = request.form['correo']
    telefono = request.form['telefono']
    especialidad = request.form['especialidad']

    # VALIDACION
    if (numero_empleado == "" or nombre == "" or
        correo == "" or telefono == "" or
        especialidad == ""):

        return """
        <h2>Todos los campos son obligatorios</h2>

        <a href='/maestros'>
            <button>Regresar</button>
        </a>
        """

    db.maestros.insert_one({
        "numero_empleado": numero_empleado,
        "nombre": nombre,
        "correo": correo,
        "telefono": telefono,
        "especialidad": especialidad
    })

    return """
    <h2>Maestro guardado correctamente</h2>

    <a href='/maestros'>
        <button>Regresar</button>
    </a>
    """

# BUSCAR MAESTRO
@app.route('/buscar_maestro', methods=['POST'])
def buscar_maestro():

    numero_empleado = request.form['numero_empleado']

    maestro = db.maestros.find_one({
        "numero_empleado": numero_empleado
    })

    if maestro:
        return f"""
        <h2>Maestro Encontrado</h2>

        Numero Empleado: {maestro['numero_empleado']} <br><br>
        Nombre: {maestro['nombre']} <br><br>
        Correo: {maestro['correo']} <br><br>
        Telefono: {maestro['telefono']} <br><br>
        Especialidad: {maestro['especialidad']} <br><br>

        <a href='/maestros'>
            <button>Regresar</button>
        </a>
        """
    else:
        return """
        <h2>Maestro no encontrado</h2>

        <a href='/maestros'>
            <button>Regresar</button>
        </a>
        """

# ELIMINAR MAESTRO
@app.route('/eliminar_maestro', methods=['POST'])
def eliminar_maestro():

    numero_empleado = request.form['numero_empleado']

    resultado = db.maestros.delete_one({
        "numero_empleado": numero_empleado
    })

    if resultado.deleted_count > 0:
        return """
        <h2>Maestro eliminado correctamente</h2>

        <a href='/maestros'>
            <button>Regresar</button>
        </a>
        """
    else:
        return """
        <h2>Maestro no encontrado</h2>

        <a href='/maestros'>
            <button>Regresar</button>
        </a>
        """
    
    # MODIFICAR MAESTRO
@app.route('/modificar_maestro', methods=['POST'])
def modificar_maestro():

    numero_empleado = request.form['numero_empleado']
    nombre = request.form['nombre']
    correo = request.form['correo']
    telefono = request.form['telefono']
    especialidad = request.form['especialidad']

    resultado = db.maestros.update_one(
        {"numero_empleado": numero_empleado},
        {
            "$set": {
                "nombre": nombre,
                "correo": correo,
                "telefono": telefono,
                "especialidad": especialidad
            }
        }
    )

    if resultado.modified_count > 0:
        return """
        <h2>Maestro modificado correctamente</h2>

        <a href='/maestros'>
            <button>Regresar</button>
        </a>
        """
    else:
        return """
        <h2>Maestro no encontrado o no hubo cambios</h2>

        <a href='/maestros'>
            <button>Regresar</button>
        </a>
        """
    


# REPORTE DE MAESTROS
@app.route('/reporte_maestros')
def reporte_maestros():

    maestros = db.maestros.find()

    tabla = """
    <h1>Reporte de Maestros</h1>

    <table border="1">
        <tr>
            <th>Numero Empleado</th>
            <th>Nombre</th>
            <th>Correo</th>
            <th>Telefono</th>
            <th>Especialidad</th>
        </tr>
    """

    for maestro in maestros:
        tabla += f"""
        <tr>
            <td>{maestro['numero_empleado']}</td>
            <td>{maestro['nombre']}</td>
            <td>{maestro['correo']}</td>
            <td>{maestro['telefono']}</td>
            <td>{maestro['especialidad']}</td>
        </tr>
        """

    tabla += """
    </table>

    <br><br>

    <a href='/maestros'>
        <button>Regresar</button>
    </a>
    """

    return tabla

# PAGINA ALUMNOS
@app.route('/alumnos')
def alumnos():
    return render_template('alumnos.html')

# GUARDAR ALUMNO
@app.route('/guardar_alumno', methods=['POST'])
def guardar_alumno():

    matricula = request.form['matricula']
    nombre = request.form['nombre']
    carrera = request.form['carrera']
    semestre = request.form['semestre']
    correo = request.form['correo']

    # VALIDACION
    if (matricula == "" or nombre == "" or
        carrera == "" or semestre == "" or
        correo == ""):

        return """
        <h2>Todos los campos son obligatorios</h2>

        <a href='/alumnos'>
            <button>Regresar</button>
        </a>
        """

    db.alumnos.insert_one({
        "matricula": matricula,
        "nombre": nombre,
        "carrera": carrera,
        "semestre": semestre,
        "correo": correo
    })

    return """
    <h2>Alumno guardado correctamente</h2>

    <a href='/alumnos'>
        <button>Regresar</button>
    </a>
    """

# BUSCAR ALUMNO
@app.route('/buscar_alumno', methods=['POST'])
def buscar_alumno():

    matricula = request.form['matricula']

    alumno = db.alumnos.find_one({
        "matricula": matricula
    })

    if alumno:
        return f"""
        <h2>Alumno Encontrado</h2>

        Matricula: {alumno['matricula']} <br><br>
        Nombre: {alumno['nombre']} <br><br>
        Carrera: {alumno['carrera']} <br><br>
        Semestre: {alumno['semestre']} <br><br>
        Correo: {alumno['correo']} <br><br>

        <a href='/alumnos'>
            <button>Regresar</button>
        </a>
        """
    else:
        return """
        <h2>Alumno no encontrado</h2>

        <a href='/alumnos'>
            <button>Regresar</button>
        </a>
        """
    
    
    # ELIMINAR ALUMNO
@app.route('/eliminar_alumno', methods=['POST'])
def eliminar_alumno():

    matricula = request.form['matricula']

    resultado = db.alumnos.delete_one({
        "matricula": matricula
    })

    if resultado.deleted_count > 0:
        return """
        <h2>Alumno eliminado correctamente</h2>

        <a href='/alumnos'>
            <button>Regresar</button>
        </a>
        """
    else:
        return """
        <h2>Alumno no encontrado</h2>

        <a href='/alumnos'>
            <button>Regresar</button>
        </a>
        """
    
    # MODIFICAR ALUMNO
@app.route('/modificar_alumno', methods=['POST'])
def modificar_alumno():

    matricula = request.form['matricula']
    nombre = request.form['nombre']
    carrera = request.form['carrera']
    semestre = request.form['semestre']
    correo = request.form['correo']

    resultado = db.alumnos.update_one(
        {"matricula": matricula},
        {
            "$set": {
                "nombre": nombre,
                "carrera": carrera,
                "semestre": semestre,
                "correo": correo
            }
        }
    )

    if resultado.modified_count > 0:
        return """
        <h2>Alumno modificado correctamente</h2>

        <a href='/alumnos'>
            <button>Regresar</button>
        </a>
        """
    else:
        return """
        <h2>Alumno no encontrado o no hubo cambios</h2>

        <a href='/alumnos'>
            <button>Regresar</button>
        </a>
        """
    
    # REPORTE DE ALUMNOS
@app.route('/reporte_alumnos')
def reporte_alumnos():

    alumnos = db.alumnos.find()

    tabla = """
    <h1>Reporte de Alumnos</h1>

    <table border="1">
        <tr>
            <th>Matricula</th>
            <th>Nombre</th>
            <th>Carrera</th>
            <th>Semestre</th>
            <th>Correo</th>
        </tr>
    """

    for alumno in alumnos:
        tabla += f"""
        <tr>
            <td>{alumno['matricula']}</td>
            <td>{alumno['nombre']}</td>
            <td>{alumno['carrera']}</td>
            <td>{alumno['semestre']}</td>
            <td>{alumno['correo']}</td>
        </tr>
        """

    tabla += """
    </table>

    <br><br>

    <a href='/alumnos'>
        <button>Regresar</button>
    </a>
    """

    return tabla

# PAGINA MATERIAS
@app.route('/materias')
def materias():
    return render_template('materias.html')

# GUARDAR MATERIA
@app.route('/guardar_materia', methods=['POST'])
def guardar_materia():

    clave = request.form['clave']
    nombre = request.form['nombre']
    creditos = request.form['creditos']
    semestre = request.form['semestre']

    # VALIDACION
    if (clave == "" or nombre == "" or
        creditos == "" or semestre == ""):

        return """
        <h2>Todos los campos son obligatorios</h2>

        <a href='/materias'>
            <button>Regresar</button>
        </a>
        """

    db.materias.insert_one({
        "clave": clave,
        "nombre": nombre,
        "creditos": creditos,
        "semestre": semestre
    })

    return """
    <h2>Materia guardada correctamente</h2>

    <a href='/materias'>
        <button>Regresar</button>
    </a>
    """
    
    # BUSCAR MATERIA
@app.route('/buscar_materia', methods=['POST'])
def buscar_materia():

    clave = request.form['clave']

    materia = db.materias.find_one({
        "clave": clave
    })

    if materia:
        return f"""
        <h2>Materia Encontrada</h2>

        Clave: {materia['clave']} <br><br>
        Nombre: {materia['nombre']} <br><br>
        Creditos: {materia['creditos']} <br><br>
        Semestre: {materia['semestre']} <br><br>

        <a href='/materias'>
            <button>Regresar</button>
        </a>
        """
    else:
        return """
        <h2>Materia no encontrada</h2>

        <a href='/materias'>
            <button>Regresar</button>
        </a>
        """
    
    # ELIMINAR MATERIA
@app.route('/eliminar_materia', methods=['POST'])
def eliminar_materia():

    clave = request.form['clave']

    resultado = db.materias.delete_one({
        "clave": clave
    })

    if resultado.deleted_count > 0:
        return """
        <h2>Materia eliminada correctamente</h2>

        <a href='/materias'>
            <button>Regresar</button>
        </a>
        """
    else:
        return """
        <h2>Materia no encontrada</h2>

        <a href='/materias'>
            <button>Regresar</button>
        </a>
        """
    
    # MODIFICAR MATERIA
@app.route('/modificar_materia', methods=['POST'])
def modificar_materia():

    clave = request.form['clave']
    nombre = request.form['nombre']
    creditos = request.form['creditos']
    semestre = request.form['semestre']

    resultado = db.materias.update_one(
        {"clave": clave},
        {
            "$set": {
                "nombre": nombre,
                "creditos": creditos,
                "semestre": semestre
            }
        }
    )

    if resultado.modified_count > 0:
        return """
        <h2>Materia modificada correctamente</h2>

        <a href='/materias'>
            <button>Regresar</button>
        </a>
        """
    else:
        return """
        <h2>Materia no encontrada o no hubo cambios</h2>

        <a href='/materias'>
            <button>Regresar</button>
        </a>
        """
    
    # REPORTE DE MATERIAS
@app.route('/reporte_materias')
def reporte_materias():

    materias = db.materias.find()

    tabla = """
    <h1>Reporte de Materias</h1>

    <table border="1">
        <tr>
            <th>Clave</th>
            <th>Nombre</th>
            <th>Creditos</th>
            <th>Semestre</th>
        </tr>
    """

    for materia in materias:
        tabla += f"""
        <tr>
            <td>{materia['clave']}</td>
            <td>{materia['nombre']}</td>
            <td>{materia['creditos']}</td>
            <td>{materia['semestre']}</td>
        </tr>
        """

    tabla += """
    </table>

    <br><br>

    <a href='/materias'>
        <button>Regresar</button>
    </a>
    """

    return tabla
    

 
if __name__ == '__main__':
    app.run(debug=True)