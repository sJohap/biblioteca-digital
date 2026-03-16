"""
Control de movimientos de préstamo.
Registra préstamos, devoluciones y muestra el historial.
Incluye contador de préstamos en curso.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from models.prestamo import Prestamo
from repositories.prestamo_repository import PrestamoRepository
from repositories.libro_repository import LibroRepository
from repositories.usuario_repository import UsuarioRepository

blueprint_movimientos = Blueprint('movimientos', __name__, url_prefix='/movimientos')
almacen_prestamos = PrestamoRepository()
almacen_libros = LibroRepository()
almacen_socios = UsuarioRepository()


@blueprint_movimientos.route('/')
def indice():
    try:
        lista = almacen_prestamos.listar_todos()
        cantidad_activos = almacen_prestamos.contar_activos()
        return render_template('prestamo/indice.html', prestamos=lista,
                               total_activos=cantidad_activos)
    except Exception as ex:
        flash(f'Error al cargar: {str(ex)}', 'fallo')
        return render_template('prestamo/indice.html', prestamos=[],
                               total_activos=0)


@blueprint_movimientos.route('/registro-completo')
def registro_completo():
    try:
        lista = almacen_prestamos.listar_todos()
        return render_template('prestamo/registro.html', prestamos=lista)
    except Exception as ex:
        flash(f'Error al cargar el registro: {str(ex)}', 'fallo')
        return render_template('prestamo/registro.html', prestamos=[])


@blueprint_movimientos.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'GET':
        try:
            disponibles = almacen_libros.listar_disponibles()
            socios = almacen_socios.listar_todos()
            return render_template('prestamo/formulario.html',
                                   libros=disponibles, socios=socios)
        except Exception as ex:
            flash(str(ex), 'fallo')
            return redirect(url_for('movimientos.indice'))
    try:
        id_libro = request.form.get('libro_id')
        id_socio = request.form.get('usuario_id')
        fecha_inicio = request.form.get('fecha_prestamo')
        fecha_fin_prevista = request.form.get('fecha_devolucion_esperada')
        if not all([id_libro, id_socio, fecha_inicio, fecha_fin_prevista]):
            flash('Todos los campos son requeridos.', 'fallo')
            disponibles = almacen_libros.listar_disponibles()
            socios = almacen_socios.listar_todos()
            return render_template('prestamo/formulario.html',
                                   libros=disponibles, socios=socios)
        movimiento = Prestamo(libro_id=int(id_libro), usuario_id=int(id_socio),
                             fecha_prestamo=fecha_inicio,
                             fecha_devolucion_esperada=fecha_fin_prevista)
        almacen_prestamos.insertar(movimiento)
        flash('Préstamo registrado. El volumen queda asignado.', 'ok')
        return redirect(url_for('movimientos.indice'))
    except (ValueError, Exception) as ex:
        flash(str(ex), 'fallo')
        return redirect(url_for('movimientos.crear'))


@blueprint_movimientos.route('/<int:identificador>/devolver', methods=['POST'])
def registrar_devolucion(identificador):
    try:
        fecha = request.form.get('fecha_devolucion') or datetime.now().strftime('%Y-%m-%d')
        if almacen_prestamos.registrar_devolucion(identificador, fecha):
            flash('Devolución registrada. El volumen vuelve a estar disponible.', 'ok')
        else:
            flash('Movimiento no localizado o ya finalizado.', 'fallo')
    except Exception as ex:
        flash(f'Error: {str(ex)}', 'fallo')
    return redirect(url_for('movimientos.indice'))
