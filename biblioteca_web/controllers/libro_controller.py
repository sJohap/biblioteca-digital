"""
Control del catálogo de volúmenes.
Incluye búsqueda por título y filtro por categoría (género).
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.libro import Libro
from repositories.libro_repository import LibroRepository
from repositories.autor_repository import AutorRepository

blueprint_catalogo = Blueprint('catalogo', __name__, url_prefix='/catalogo')
almacen_libros = LibroRepository()
almacen_escritores = AutorRepository()


@blueprint_catalogo.route('/')
def indice():
    try:
        criterio = request.args.get('buscar', '').strip()
        categoria = request.args.get('genero', '').strip()
        if criterio:
            elementos = almacen_libros.buscar_por_titulo(criterio)
        elif categoria:
            elementos = almacen_libros.filtrar_por_genero(categoria)
        else:
            elementos = almacen_libros.listar_todos()
        return render_template('libro/indice.html', libros=elementos,
                               criterio=criterio, categoria=categoria)
    except Exception as ex:
        flash(f'Error al obtener el catálogo: {str(ex)}', 'fallo')
        return render_template('libro/indice.html', libros=[])


@blueprint_catalogo.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'GET':
        escritores = almacen_escritores.listar_todos()
        return render_template('libro/formulario.html', libro=None, escritores=escritores)
    try:
        titulo = request.form.get('titulo', '').strip()
        isbn = request.form.get('isbn', '').strip() or None
        id_autor = request.form.get('autor_id')
        id_autor = int(id_autor) if id_autor else None
        anio = request.form.get('anio')
        anio = int(anio) if anio else None
        genero = request.form.get('genero', '').strip()
        if not titulo or not id_autor:
            flash('Título y autor son requeridos.', 'fallo')
            return render_template('libro/formulario.html', libro=None,
                                   escritores=almacen_escritores.listar_todos())
        volumen = Libro(titulo=titulo, isbn=isbn, autor_id=id_autor, anio=anio,
                        genero=genero, disponible=True)
        almacen_libros.insertar(volumen)
        flash('Volumen agregado al catálogo.', 'ok')
        return redirect(url_for('catalogo.indice'))
    except Exception as ex:
        flash(f'Error al guardar: {str(ex)}', 'fallo')
        return render_template('libro/formulario.html', libro=None,
                               escritores=almacen_escritores.listar_todos())


@blueprint_catalogo.route('/<int:identificador>/modificar', methods=['GET', 'POST'])
def modificar(identificador):
    libro = almacen_libros.obtener_por_id(identificador)
    if not libro:
        flash('Volumen no encontrado.', 'fallo')
        return redirect(url_for('catalogo.indice'))
    if request.method == 'GET':
        return render_template('libro/formulario.html', libro=libro,
                               escritores=almacen_escritores.listar_todos())
    try:
        libro.titulo = request.form.get('titulo', '').strip()
        libro.isbn = request.form.get('isbn', '').strip() or None
        id_autor = request.form.get('autor_id')
        libro.autor_id = int(id_autor) if id_autor else None
        anio = request.form.get('anio')
        libro.anio = int(anio) if anio else None
        libro.genero = request.form.get('genero', '').strip()
        if not libro.titulo or not libro.autor_id:
            flash('Título y autor son requeridos.', 'fallo')
            return render_template('libro/formulario.html', libro=libro,
                                   escritores=almacen_escritores.listar_todos())
        almacen_libros.actualizar(libro)
        flash('Datos actualizados.', 'ok')
        return redirect(url_for('catalogo.indice'))
    except Exception as ex:
        flash(f'Error al actualizar: {str(ex)}', 'fallo')
        return render_template('libro/formulario.html', libro=libro,
                               escritores=almacen_escritores.listar_todos())


@blueprint_catalogo.route('/<int:identificador>/borrar', methods=['POST'])
def borrar(identificador):
    try:
        if almacen_libros.eliminar(identificador):
            flash('Volumen eliminado.', 'ok')
        else:
            flash('No se pudo eliminar.', 'fallo')
    except Exception as ex:
        flash(f'Error: {str(ex)}', 'fallo')
    return redirect(url_for('catalogo.indice'))
