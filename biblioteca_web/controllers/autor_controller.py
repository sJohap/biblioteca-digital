"""
Módulo de control de escritores (autores).
Expone rutas para listar, crear, editar y eliminar.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.autor import Autor
from repositories.autor_repository import AutorRepository

blueprint_escritores = Blueprint('escritores', __name__, url_prefix='/escritores')
almacen_escritores = AutorRepository()


@blueprint_escritores.route('/')
def indice():
    try:
        lista = almacen_escritores.listar_todos()
        return render_template('autor/indice.html', escritores=lista)
    except Exception as ex:
        flash(f'Error al cargar la lista: {str(ex)}', 'fallo')
        return render_template('autor/indice.html', escritores=[])


@blueprint_escritores.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'GET':
        return render_template('autor/formulario.html', escritor=None)
    try:
        nombre = request.form.get('nombre', '').strip()
        nacionalidad = request.form.get('nacionalidad', '').strip()
        biografia = request.form.get('biografia', '').strip()
        if not nombre:
            flash('El campo nombre es obligatorio.', 'fallo')
            return render_template('autor/formulario.html', escritor=None)
        escritor = Autor(nombre=nombre, nacionalidad=nacionalidad, biografia=biografia)
        almacen_escritores.insertar(escritor)
        flash('Escritor agregado correctamente.', 'ok')
        return redirect(url_for('escritores.indice'))
    except ValueError as ex:
        flash(str(ex), 'fallo')
        return render_template('autor/formulario.html', escritor=None)
    except Exception as ex:
        flash(f'No se pudo guardar: {str(ex)}', 'fallo')
        return render_template('autor/formulario.html', escritor=None)


@blueprint_escritores.route('/<int:identificador>/modificar', methods=['GET', 'POST'])
def modificar(identificador):
    escritor = almacen_escritores.obtener_por_id(identificador)
    if not escritor:
        flash('Escritor no localizado.', 'fallo')
        return redirect(url_for('escritores.indice'))
    if request.method == 'GET':
        return render_template('autor/formulario.html', escritor=escritor)
    try:
        escritor.nombre = request.form.get('nombre', '').strip()
        escritor.nacionalidad = request.form.get('nacionalidad', '').strip()
        escritor.biografia = request.form.get('biografia', '').strip()
        if not escritor.nombre:
            flash('El campo nombre es obligatorio.', 'fallo')
            return render_template('autor/formulario.html', escritor=escritor)
        almacen_escritores.actualizar(escritor)
        flash('Cambios aplicados correctamente.', 'ok')
        return redirect(url_for('escritores.indice'))
    except (ValueError, Exception) as ex:
        flash(str(ex), 'fallo')
        return render_template('autor/formulario.html', escritor=escritor)


@blueprint_escritores.route('/<int:identificador>/borrar', methods=['POST'])
def borrar(identificador):
    try:
        if almacen_escritores.eliminar(identificador):
            flash('Registro eliminado.', 'ok')
        else:
            flash('No fue posible eliminar.', 'fallo')
    except Exception as ex:
        flash(f'Error: {str(ex)}', 'fallo')
    return redirect(url_for('escritores.indice'))
