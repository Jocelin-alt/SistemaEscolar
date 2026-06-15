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
    return "Modulo Alumnos"

# PAGINA MATERIAS
@app.route('/materias')
def materias():
    return "Modulo Materias"

if __name__ == '__main__':
    app.run(debug=True)