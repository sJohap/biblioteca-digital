"""
Modelo de dominio para la entidad Prestamo.
Vincula un libro con un usuario y registra fechas de préstamo y devolución.
"""


class Prestamo:
    """Entidad que representa un préstamo de un libro a un usuario."""

    def __init__(self, id_=None, libro_id=None, usuario_id=None,
                 fecha_prestamo=None, fecha_devolucion_esperada=None,
                 fecha_devolucion_real=None, estado='activo'):
        self.id = id_
        self.libro_id = libro_id
        self.usuario_id = usuario_id
        self.fecha_prestamo = fecha_prestamo or ''
        self.fecha_devolucion_esperada = fecha_devolucion_esperada or ''
        self.fecha_devolucion_real = fecha_devolucion_real
        self.estado = estado if estado in ('activo', 'devuelto') else 'activo'

    def __str__(self):
        return f"Prestamo(id={self.id}, libro={self.libro_id}, usuario={self.usuario_id}, estado={self.estado})"

    def __repr__(self):
        return self.__str__()

    def es_valido(self):
        """Comprueba que existan libro, usuario y fechas requeridas."""
        return bool(
            self.libro_id is not None and
            self.usuario_id is not None and
            self.fecha_prestamo and self.fecha_devolucion_esperada
        )
