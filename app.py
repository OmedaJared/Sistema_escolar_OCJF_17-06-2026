from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_db
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "clave_secreta_institucional_desarrollo"

# Conexión única y limpia usando database.py
db = get_db()

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/alumnos', methods=['GET', 'POST'])
def alumnos():
    if request.method == 'POST':
        matricula = request.form.get('matricula', '').strip()
        nombres = request.form.get('nombres', '').strip()
        apellidos = request.form.get('apellidos', '').strip()
        correo = request.form.get('correo', '').strip()
        fecha_nacimiento = request.form.get('fecha_nacimiento', '').strip()

        # Validación del lado del Servidor
        if not (matricula and nombres and apellidos and correo and fecha_nacimiento):
            flash("Todos los campos son obligatorios para registrar al alumno.", "danger")
            return redirect(url_for('alumnos'))

        # Validar índice único (Matrícula)
        if db.alumnos.find_one({"matricula": matricula}):
            flash(f"La matrícula '{matricula}' ya se encuentra registrada.", "danger")
            return redirect(url_for('alumnos'))

        # Inserción limpia
        db.alumnos.insert_one({
            "matricula": matricula,
            "nombres": nombres,
            "apellidos": apellidos,
            "correo": correo,
            "fecha_nacimiento": fecha_nacimiento
        })
        flash("Alumno matriculado exitosamente.", "success")
        return redirect(url_for('alumnos'))

    lista_alumnos = list(db.alumnos.find({}))
    return render_template('alumnos.html', alumnos=lista_alumnos)


@app.route('/alumnos/editar/<id>', methods=['POST'])
def editar_alumno(id):
    nombres = request.form.get('nombres', '').strip()
    apellidos = request.form.get('apellidos', '').strip()
    correo = request.form.get('correo', '').strip()
    fecha_nacimiento = request.form.get('fecha_nacimiento', '').strip()

    if not (nombres and apellidos and correo and fecha_nacimiento):
        flash("Campos incompletos. No se pudo actualizar al alumno.", "danger")
        return redirect(url_for('alumnos'))

    db.alumnos.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "nombres": nombres,
            "apellidos": apellidos,
            "correo": correo,
            "fecha_nacimiento": fecha_nacimiento
        }}
    )
    flash("Información del alumno actualizada con éxito.", "success")
    return redirect(url_for('alumnos'))


@app.route('/alumnos/eliminar/<id>')
def eliminar_alumno(id):
    db.alumnos.delete_one({"_id": ObjectId(id)})
    flash("Registro del alumno eliminado correctamente.", "success")
    return redirect(url_for('alumnos'))

@app.route('/maestros', methods=['GET', 'POST'])
def maestros():
    if request.method == 'POST':
        num_empleado = request.form.get('num_empleado', '').strip()
        nombre_completo = request.form.get('nombre_completo', '').strip()
        especialidad = request.form.get('especialidad', '').strip()
        telefono = request.form.get('telefono', '').strip()
        turno = request.form.get('turno', '').strip()

        if not (num_empleado and nombre_completo and especialidad and telefono and turno):
            flash("Todos los campos son obligatorios para dar de alta al docente.", "danger")
            return redirect(url_for('maestros'))

        # Validar índice único (No. de Empleado)
        if db.maestros.find_one({"num_empleado": num_empleado}):
            flash(f"El número de empleado '{num_empleado}' ya existe.", "danger")
            return redirect(url_for('maestros'))

        db.maestros.insert_one({
            "num_empleado": num_empleado,
            "nombre_completo": nombre_completo,
            "especialidad": especialidad,
            "telefono": telefono,
            "turno": turno
        })
        flash("Docente registrado exitosamente en la plantilla.", "success")
        return redirect(url_for('maestros'))

    lista_maestros = list(db.maestros.find({}))
    return render_template('maestros.html', maestros=lista_maestros)


@app.route('/maestros/editar/<id>', methods=['POST'])
def editar_maestro(id):
    nombre_completo = request.form.get('nombre_completo', '').strip()
    especialidad = request.form.get('especialidad', '').strip()
    telefono = request.form.get('telefono', '').strip()
    turno = request.form.get('turno', '').strip()

    if not (nombre_completo and especialidad and telefono and turno):
        flash("Campos incompletos para actualizar al maestro.", "danger")
        return redirect(url_for('maestros'))

    db.maestros.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "nombre_completo": nombre_completo,
            "especialidad": specialty if 'specialty' in locals() else especialidad,
            "telefono": telefono,
            "turno": turno
        }}
    )
    flash("Datos del docente modificados correctamente.", "success")
    return redirect(url_for('maestros'))


@app.route('/maestros/eliminar/<id>')
def eliminar_maestro(id):
    db.maestros.delete_one({"_id": ObjectId(id)})
    flash("Docente dado de baja del sistema.", "success")
    return redirect(url_for('maestros'))



@app.route('/materias', methods=['GET', 'POST'])
def materias():
    if request.method == 'POST':
        codigo_materia = request.form.get('codigo_materia', '').strip()
        nombre_asignatura = request.form.get('nombre_asignatura', '').strip()
        horas_semanales = request.form.get('horas_semanales', '').strip()
        creditos = request.form.get('creditos', '').strip()

        if not (codigo_materia and nombre_asignatura and horas_semanales and creditos):
            flash("Todos los campos son obligatorios para el plan de estudios.", "danger")
            return redirect(url_for('materias'))

        # Validar índice único (Código de Materia)
        if db.materias.find_one({"codigo_materia": codigo_materia}):
            flash(f"El código de materia '{codigo_materia}' ya se encuentra asignado.", "danger")
            return redirect(url_for('materias'))

        try:
            db.materias.insert_one({
                "codigo_materia": codigo_materia,
                "nombre_asignatura": nombre_asignatura,
                "horas_semanales": int(horas_semanales),
                "creditos": int(creditos)
            })
            flash("Nueva asignatura añadida al plan curricular.", "success")
        except ValueError:
            flash("Las horas y los créditos deben ser valores numéricos enteros.", "danger")

        return redirect(url_for('materias'))

    lista_materias = list(db.materias.find({}))
    return render_template('materias.html', materias=lista_materias)


@app.route('/materias/editar/<id>', methods=['POST'])
def editar_materia(id):
    nombre_asignatura = request.form.get('nombre_asignatura', '').strip()
    horas_semanales = request.form.get('horas_semanales', '').strip()
    creditos = request.form.get('creditos', '').strip()

    if not (nombre_asignatura and horas_semanales and creditos):
        flash("Campos incompletos para actualizar la materia.", "danger")
        return redirect(url_for('materias'))

    try:
        db.materias.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "nombre_asignatura": nombre_asignatura,
                "horas_semanales": int(horas_semanales),
                "creditos": int(creditos)
            }}
        )
        flash("Detalles de la asignatura modificados.", "success")
    except ValueError:
        flash("Error: Horas y créditos deben ser numéricos.", "danger")

    return redirect(url_for('materias'))


@app.route('/materias/eliminar/<id>')
def eliminar_materia(id):
    db.materias.delete_one({"_id": ObjectId(id)})
    flash("Asignatura eliminada del plan de estudios.", "success")
    return redirect(url_for('materias'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
