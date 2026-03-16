"""
Control de socios (usuarios) de la biblioteca.
Gestiona el registro y modificación de personas que solicitan préstamos.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository

blueprint_socios = Blueprint('socios', __name__, url_prefix='/socios')
almacen_socios = UsuarioRepository()


@blueprint_socios.route('/')
def indice():
    try:
        lista = almacen_socios.listar_todos()
        return render_template('usuario/indice.html', socios=lista)
    except Exception as ex:
        flash(f'Error al cargar: {str(ex)}', 'fallo')
        return render_template('usuario/indice.html', socios=[])


@blueprint_socios.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'GET':
        return render_template('usuario/formulario.html', socio=None)
    try:
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        telefono = request.form.get('telefono', '').strip()
        if not nombre or not email:
            flash('Nombre y correo son obligatorios.', 'fallo')
            return render_template('usuario/formulario.html', socio=None)
        socio = Usuario(nombre=nombre, email=email, telefono=telefono)
        almacen_socios.insertar(socio)
        flash('Socio registrado.', 'ok')
        return redirect(url_for('socios.indice'))
    except ValueError as ex:
        flash(str(ex), 'fallo')
        return render_template('usuario/formulario.html', socio=None)
    except Exception as ex:
        flash(f'Error al guardar: {str(ex)}', 'fallo')
        return render_template('usuario/formulario.html', socio=None)


@blueprint_socios.route('/<int:identificador>/modificar', methods=['GET', 'POST'])
def modificar(identificador):
    socio = almacen_socios.obtener_por_id(identificador)
    if not socio:
        flash('Socio no localizado.', 'fallo')
        return redirect(url_for('socios.indice'))
    if request.method == 'GET':
        return render_template('usuario/formulario.html', socio=socio)
    try:
        socio.nombre = request.form.get('nombre', '').strip()
        socio.email = request.form.get('email', '').strip()
        socio.telefono = request.form.get('telefono', '').strip()
        if not socio.nombre or not socio.email:
            flash('Nombre y correo son obligatorios.', 'fallo')
            return render_template('usuario/formulario.html', socio=socio)
        almacen_socios.actualizar(socio)
        flash('Datos actualizados.', 'ok')
        return redirect(url_for('socios.indice'))
    except (ValueError, Exception) as ex:
        flash(str(ex), 'fallo')
        return render_template('usuario/formulario.html', socio=socio)


@blueprint_socios.route('/<int:identificador>/borrar', methods=['POST'])
def borrar(identificador):
    try:
        if almacen_socios.eliminar(identificador):
            flash('Registro eliminado.', 'ok')
        else:
            flash('No fue posible eliminar.', 'fallo')
    except Exception as ex:
        flash(f'Error: {str(ex)}', 'fallo')
    return redirect(url_for('socios.indice'))
