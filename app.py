from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_db
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "clave_secreta_institucional_desarrollo"

db = get_db()

def calcular_rendimiento_alumno(alumno_id, curso_id):
    try:
        tareas_curso = list(db.tareas.find({"curso_id": str(curso_id)}))
        tareas_totales = len(tareas_curso)
        
        if tareas_totales == 0:
            return 100  

        lista_tarea_ids = [str(t["_id"]) for t in tareas_curso]

        tareas_entregadas = db.entregas.count_documents({
            "alumno_id": str(alumno_id),
            "tarea_id": {"$in": lista_tarea_ids},
            "estado": "entregado"
        })

        return int((tareas_entregadas / tareas_totales) * 100)
    except Exception as e:
        print(f"Error al calcular rendimiento: {e}")
        return 0

@app.route('/')
def index():
    return render_template('base.html')


# --- ALUMNOS ---
@app.route('/alumnos', methods=['GET', 'POST'])
def alumnos():
    if request.method == 'POST':
        matricula = request.form.get('matricula', '').strip()
        nombres = request.form.get('nombres', '').strip()
        apellidos = request.form.get('apellidos', '').strip()
        correo = request.form.get('correo', '').strip()
        fecha_nacimiento = request.form.get('fecha_nacimiento', '').strip()
        grupo = request.form.get('grupo', '').strip()

        if not (matricula and nombres and apellidos and correo and fecha_nacimiento and grupo):
            flash("Todos los campos son obligatorios para registrar al alumno.", "danger")
            return redirect(url_for('alumnos'))

        if db.alumnos.find_one({"matricula": matricula}):
            flash(f"La matrícula '{matricula}' ya se encuentra registrada.", "danger")
            return redirect(url_for('alumnos'))

        db.alumnos.insert_one({
            "matricula": matricula,
            "nombres": nombres,
            "apellidos": apellidos,
            "correo": correo,
            "fecha_nacimiento": fecha_nacimiento,
            "grupo": grupo
        })
        flash("Alumno registrado exitosamente.", "success")
        return redirect(url_for('alumnos'))

    lista_alumnos = list(db.alumnos.find({}))
    return render_template('alumnos.html', alumnos=lista_alumnos)


@app.route('/alumnos/editar/<id>', methods=['POST'])
def editar_alumno(id):
    nombres = request.form.get('nombres', '').strip()
    apellidos = request.form.get('apellidos', '').strip()
    correo = request.form.get('correo', '').strip()
    fecha_nacimiento = request.form.get('fecha_nacimiento', '').strip()
    grupo = request.form.get('grupo', '').strip()

    db.alumnos.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "nombres": nombres,
            "apellidos": apellidos,
            "correo": correo,
            "fecha_nacimiento": fecha_nacimiento,
            "grupo": grupo
        }}
    )
    flash("Información del alumno actualizada con éxito.", "success")
    return redirect(url_for('alumnos'))


@app.route('/alumnos/eliminar/<id>')
def eliminar_alumno(id):
    db.alumnos.delete_one({"_id": ObjectId(id)})
    flash("Registro del alumno eliminado correctamente.", "success")
    return redirect(url_for('alumnos'))


# --- MAESTROS ---
@app.route('/maestros', methods=['GET', 'POST'])
def maestros():
    if request.method == 'POST':
        num_empleado = request.form.get('num_empleado', '').strip()
        nombre_completo = request.form.get('nombre_completo', '').strip()
        especialidad = request.form.get('especialidad', '').strip()
        telefono = request.form.get('telefono', '').strip()
        turno = request.form.get('turno', '').strip()
        grupos_seleccionados = request.form.getlist('grupos[]')

        if not (num_empleado and nombre_completo and especialidad and telefono and turno and grupos_seleccionados):
            flash("Todos los campos son obligatorios para registrar al docente.", "danger")
            return redirect(url_for('maestros'))

        if db.maestros.find_one({"num_empleado": num_empleado}):
            flash(f"El número de empleado '{num_empleado}' ya existe.", "danger")
            return redirect(url_for('maestros'))

        db.maestros.insert_one({
            "num_empleado": num_empleado,
            "nombre_completo": nombre_completo,
            "especialidad": especialidad,
            "telefono": telefono,
            "turno": turno,
            "grupos": grupos_seleccionados
        })
        flash("Docente registrado exitosamente.", "success")
        return redirect(url_for('maestros'))

    lista_maestros = list(db.maestros.find({}))
    return render_template('maestros.html', maestros=lista_maestros)


@app.route('/maestros/editar/<id>', methods=['POST'])
def editar_maestro(id):
    nombre_completo = request.form.get('nombre_completo', '').strip()
    especialidad = request.form.get('especialidad', '').strip()
    telefono = request.form.get('telefono', '').strip()
    turno = request.form.get('turno', '').strip()
    grupos_seleccionados = request.form.getlist('grupos[]')

    db.maestros.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "nombre_completo": nombre_completo,
            "especialidad": especialidad,
            "telefono": telefono,
            "turno": turno,
            "grupos": grupos_seleccionados
        }}
    )
    flash("Datos del docente modificados correctamente.", "success")
    return redirect(url_for('maestros'))


@app.route('/maestros/eliminar/<id>')
def eliminar_maestro(id):
    db.maestros.delete_one({"_id": ObjectId(id)})
    flash("Docente dado de baja.", "success")
    return redirect(url_for('maestros'))


# --- MATERIAS ---
@app.route('/materias', methods=['GET', 'POST'])
def materias():
    if request.method == 'POST':
        codigo_materia = request.form.get('codigo_materia', '').strip()
        nombre_asignatura = request.form.get('nombre_asignatura', '').strip()
        horas_semanales = request.form.get('horas_semanales', '').strip()
        creditos = request.form.get('creditos', '').strip()

        if db.materias.find_one({"codigo_materia": codigo_materia}):
            flash(f"El código '{codigo_materia}' ya existe.", "danger")
            return redirect(url_for('materias'))

        db.materias.insert_one({
            "codigo_materia": codigo_materia,
            "nombre_asignatura": nombre_asignatura,
            "horas_semanales": int(horas_semanales),
            "creditos": int(creditos)
        })
        flash("Nueva asignatura añadida.", "success")
        return redirect(url_for('materias'))

    lista_materias = list(db.materias.find({}))
    return render_template('materias.html', materias=lista_materias)


@app.route('/materias/editar/<id>', methods=['POST'])
def editar_materia(id):
    nombre_asignatura = request.form.get('nombre_asignatura', '').strip()
    horas_semanales = request.form.get('horas_semanales', '').strip()
    creditos = request.form.get('creditos', '').strip()

    if not (nombre_asignatura and horas_semanales and creditos):
        flash("Todos los campos son obligatorios para editar la materia.", "danger")
        return redirect(url_for('materias'))

    try:
        horas_int = int(horas_semanales)
        creditos_int = int(creditos)
    except ValueError:
        flash("Las horas semanales y los créditos deben ser números enteros.", "danger")
        return redirect(url_for('materias'))

    db.materias.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "nombre_asignatura": nombre_asignatura,
            "horas_semanales": horas_int,
            "creditos": creditos_int
        }}
    )
    
    flash("Materia actualizada con éxito.", "success")
    return redirect(url_for('materias'))


@app.route('/materias/eliminar/<id>')
def eliminar_materia(id):
    db.materias.delete_one({"_id": ObjectId(id)})
    flash("Asignatura de baja.", "success")
    return redirect(url_for('materias'))


# --- GRUPOS ---
@app.route('/grupos', methods=['GET', 'POST'])
def grupos():
    try:
        cursos_en_db = list(db.inscripciones_cursos.find())
        grupos_disponibles = sorted(list(set([c.get("grupo", "").strip() for c in cursos_en_db if c.get("grupo")])))
    except Exception:
        grupos_disponibles = []

    maestros_disponibles = list(db.maestros.find())
    materias_disponibles = list(db.materias.find())
    todos_los_alumnos = list(db.alumnos.find())

    grupo_seleccionado = request.form.get('grupo_id') or request.args.get('grupo_id') or request.form.get('grupo') or request.args.get('grupo')
    if grupo_seleccionado:
        grupo_seleccionado = grupo_seleccionado.strip()

    curso_seleccionado_id = request.form.get('curso_id') or request.args.get('curso_id') or request.form.get('id_curso') or request.args.get('id_curso')
    
    curso = None
    cursos_del_grupo = []
    alumnos_inscritos = []
    lista_tareas = []
    materia_nombre = ""
    docente_asignado = None

    if request.method == 'POST' and request.form.get('action') == 'crear_curso':
        grupo_destino = request.form.get('grupo', '').strip()
        materia = request.form.get('materia', '').strip()
        maestro_id = request.form.get('maestro_id', '').strip()

        if not (grupo_destino and materia and maestro_id):
            flash("Todos los campos (Nombre de grupo, Materia y Docente) son obligatorios.", "danger")
            return redirect(url_for('grupos'))

        existe = db.inscripciones_cursos.find_one({"grupo": grupo_destino, "materia": materia})
        if existe:
            flash(f"El grupo '{grupo_destino}' ya tiene un curso asignado para la materia de {materia}.", "warning")
            return redirect(url_for('grupos', grupo=grupo_destino))
        
        db.inscripciones_cursos.insert_one({
            "grupo": grupo_destino,
            "materia": materia,
            "maestro_id": maestro_id,
            "alumnos": []
        })
        flash(f"Grupo '{grupo_destino}' creado con éxito para la materia {materia}.", "success")
        return redirect(url_for('grupos', grupo=grupo_destino))

    if grupo_seleccionado:
        cursos_del_grupo = list(db.inscripciones_cursos.find({"grupo": grupo_seleccionado}))
        if curso_seleccionado_id:
            try:
                curso = db.inscripciones_cursos.find_one({"_id": ObjectId(curso_seleccionado_id)})
            except Exception:
                curso = db.inscripciones_cursos.find_one({"_id": str(curso_seleccionado_id)})
        elif cursos_del_grupo:
            curso = cursos_del_grupo[0]
            curso_seleccionado_id = str(curso["_id"])

    if curso:
        curso_seleccionado_id = str(curso["_id"])
        materia_nombre = curso.get("materia", "")
        maestro_id_curso = curso.get("maestro_id", "")
        
        if maestro_id_curso:
            try:
                docente_asignado = db.maestros.find_one({"_id": ObjectId(maestro_id_curso)})
            except Exception:
                pass
            if not docente_asignado:
                docente_asignado = db.maestros.find_one({"_id": str(maestro_id_curso)})

        lista_tareas = list(db.tareas.find({"curso_id": curso_seleccionado_id}))
        
        for al_id in curso.get("alumnos", []):
            al = None
            try:
                al = db.alumnos.find_one({"_id": ObjectId(al_id)})
            except Exception:
                pass
            if not al:
                al = db.alumnos.find_one({"_id": str(al_id)})
            if al:
                rendimiento = calcular_rendimiento_alumno(al["_id"], curso_seleccionado_id)
                alumnos_inscritos.append({
                    "_id": str(al["_id"]),
                    "matricula": al.get("matricula"),
                    "nombres": al.get("nombres"),
                    "apellidos": al.get("apellidos"),
                    "rendimiento": rendimiento
                })

    return render_template(
        'grupos.html',
        grupos=grupos_disponibles,
        grupo_seleccionado=grupo_seleccionado,
        grupo=grupo_seleccionado,
        cursos_del_grupo=cursos_del_grupo,
        maestros=maestros_disponibles,
        materias=materias_disponibles,
        todos_los_alumnos=todos_los_alumnos,
        docente=docente_asignado,
        curso=curso,
        curso_id=curso_seleccionado_id if curso_seleccionado_id else "",
        materia=materia_nombre,
        alumnos=alumnos_inscritos,
        tareas=lista_tareas
    )

@app.route('/grupos/eliminar/<id_curso>', methods=['GET'])
def eliminar_curso(id_curso):
    try:
        curso = db.inscripciones_cursos.find_one({"_id": ObjectId(id_curso)})
        grupo_retorno = curso.get("grupo") if curso else None
        
        resultado = db.inscripciones_cursos.delete_one({"_id": ObjectId(id_curso)})
        if resultado.deleted_count == 0:
            db.inscripciones_cursos.delete_one({"_id": str(id_curso)})
            
        db.tareas.delete_many({"curso_id": str(id_curso)})
        flash("Curso eliminado correctamente junto con sus registros asociados.", "success")
        
        if grupo_retorno:
            return redirect(url_for('grupos', grupo=grupo_retorno))
    except Exception as e:
        flash(f"Error al intentar eliminar el curso: {e}", "danger")
        
    return redirect(url_for('grupos'))

@app.route('/cursos/crear', methods=['POST'])
def crear_curso():
    grupo = request.form.get('grupo', '').strip()
    materia = request.form.get('materia', '').strip()
    maestro_id = request.form.get('maestro_id')

    if not (grupo and materia and maestro_id):
        flash("Todos los campos son obligatorios para abrir un curso.", "danger")
        return redirect(url_for('grupos', grupo=grupo))

    existe = db.inscripciones_cursos.find_one({"grupo": grupo, "materia": materia})
    if existe:
        flash(f"El grupo {grupo} ya tiene un curso asignado para la materia de {materia}.", "warning")
    else:
        db.inscripciones_cursos.insert_one({
            "grupo": grupo,
            "materia": materia,
            "maestro_id": maestro_id,
            "alumnos": []
        })
        flash("Curso creado de manera exitosa para el grupo.", "success")

    return redirect(url_for('grupos', grupo=grupo))


@app.route('/cursos/agregar_alumno', methods=['POST'])
def agregar_alumno_curso():
    curso_id = request.form.get('curso_id')
    alumno_id = request.form.get('alumno_id')

    curso = db.inscripciones_cursos.find_one({"_id": ObjectId(curso_id)})
    if curso:
        if alumno_id not in curso.get("alumnos", []):
            db.inscripciones_cursos.update_one(
                {"_id": ObjectId(curso_id)},
                {"$push": {"alumnos": alumno_id}}
            )
            flash("Alumno inscrito exitosamente en el curso.", "success")
        else:
            flash("El alumno ya está registrado en este curso.", "warning")
        return redirect(url_for('grupos', grupo=curso["grupo"], curso_id=curso_id))
    
    return redirect(url_for('grupos'))


@app.route('/cursos/eliminar_alumno', methods=['POST'])
def eliminar_alumno_curso():
    curso_id = request.form.get('curso_id')
    alumno_id = request.form.get('alumno_id')

    curso = db.inscripciones_cursos.find_one({"_id": ObjectId(curso_id)})
    if curso:
        db.inscripciones_cursos.update_one(
            {"_id": ObjectId(curso_id)},
            {"$pull": {"alumnos": alumno_id}}
        )
        flash("Alumno removido del curso.", "info")
        return redirect(url_for('grupos', grupo=curso["grupo"], curso_id=curso_id))
        
    return redirect(url_for('grupos'))


@app.route('/tareas/crear', methods=['POST'])
def crear_tarea():
    curso_id = request.form.get('curso_id')
    titulo_tarea = request.form.get('titulo_tarea', '').strip()

    curso = db.inscripciones_cursos.find_one({"_id": ObjectId(curso_id)})
    if curso and titulo_tarea:
        db.tareas.insert_one({
            "grupo": curso["grupo"],
            "materia": curso["materia"],
            "curso_id": curso_id,
            "titulo": titulo_tarea
        })
        flash(f"Tarea '{titulo_tarea}' asignada.", "success")
        return redirect(url_for('grupos', grupo=curso["grupo"], curso_id=curso_id))
        
    return redirect(url_for('grupos'))


@app.route('/tareas/eliminar', methods=['POST'])
def eliminar_tarea():
    curso_id = request.form.get('curso_id')
    tarea_id = request.form.get('tarea_id')

    curso = db.inscripciones_cursos.find_one({"_id": ObjectId(curso_id)})
    if tarea_id:
        db.tareas.delete_one({"_id": ObjectId(tarea_id)})
        db.entregas.delete_many({"tarea_id": tarea_id})
        flash("Tarea eliminada correctamente del curso.", "info")
        
    if curso:
        return redirect(url_for('grupos', grupo=curso["grupo"], curso_id=curso_id))
    return redirect(url_for('grupos'))


@app.route('/tareas/evaluar/<curso_id>')
def evaluar_tareas(curso_id):
    curso = None
    try:
        curso = db.inscripciones_cursos.find_one({"_id": ObjectId(curso_id)})
    except Exception:
        pass
    
    if not curso:
        curso = db.inscripciones_cursos.find_one({"_id": str(curso_id)})

    if not curso:
        flash("Curso no encontrado en el sistema.", "danger")
        return redirect(url_for('grupos'))

    lista_tareas = list(db.tareas.find({
        "$or": [
            {"curso_id": str(curso_id)},
            {"curso_id": ObjectId(curso_id) if ObjectId.is_valid(curso_id) else curso_id}
        ]
    }))

    alumnos_curso = []
    for al_id in curso.get("alumnos", []):
        al = None
        try:
            al = db.alumnos.find_one({"_id": ObjectId(al_id)})
        except Exception:
            pass
        if not al:
            al = db.alumnos.find_one({"_id": str(al_id)})
            
        if al:
            alumnos_curso.append({
                "_id": str(al["_id"]),
                "matricula": al.get("matricula"),
                "nombre_completo": f"{al.get('nombres')} {al.get('apellidos')}"
            })
    
    entregas_map = {}
    try:
        todas_entregas = list(db.entregas.find({"materia": curso.get("materia")}))
        for t in todas_entregas:
            key = f"{str(t.get('alumno_id'))}_{str(t.get('tarea_id'))}"
            entregas_map[key] = t.get("estado", "no_entregado")
    except Exception as e:
        print(f"Error cargando entregas: {e}")

    return render_template(
        'evaluar_tareas.html',
        curso_id=str(curso_id),
        grupo=curso.get("grupo", ""),
        materia=curso.get("materia", ""),
        tareas=lista_tareas,
        alumnos=alumnos_curso,
        entregas_map=entregas_map
    )

@app.route('/tareas/guardar_calificaciones', methods=['POST'])
def guardar_calificaciones():
    curso_id = request.form.get('curso_id')
    
    if not curso_id:
        flash("Error: No se proporcionó el identificador del curso en el formulario.", "danger")
        return redirect(url_for('grupos'))

    try:
        curso = db.inscripciones_cursos.find_one({"_id": ObjectId(curso_id)})
    except Exception:
        curso = None
    
    if not curso:
        flash("Error al procesar las calificaciones: Curso no encontrado.", "danger")
        return redirect(url_for('grupos'))
        
    materia = curso.get("materia", "Sin materia")
    grupo_curso = curso.get("grupo", "")
    lista_tareas = list(db.tareas.find({"curso_id": str(curso_id)}))

    for al_id in curso.get("alumnos", []):
        a_id_str = str(al_id)
        for tarea in lista_tareas:
            t_id_str = str(tarea["_id"])
            checkbox_name = f"entrega_{a_id_str}_{t_id_str}"
            ha_entregado = request.form.get(checkbox_name)
            
            estado_actual = "entregado" if ha_entregado else "no_entregado"
            
            db.entregas.update_one(
                {"alumno_id": a_id_str, "tarea_id": t_id_str, "materia": materia},
                {"$set": {
                    "alumno_id": a_id_str,
                    "tarea_id": t_id_str,
                    "materia": materia,
                    "estado": estado_actual
                }},
                upsert=True
            )
            
    flash("Calificaciones guardadas correctamente.", "success")
    return redirect(url_for('grupos', grupo=grupo_curso, curso_id=curso_id))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)