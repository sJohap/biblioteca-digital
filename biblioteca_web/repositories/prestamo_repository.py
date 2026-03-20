"""
Repository para la entidad Prestamo.
Gestiona préstamos, historial y disponibilidad de libros.
"""
from database import obtener_conexion
from models.prestamo import Prestamo


class PrestamoRepository:
    """Acceso a datos de préstamos."""

    def listar_todos(self):
        """Obtiene todos los préstamos con datos de libro y usuario."""
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT p.id, p.libro_id, p.usuario_id, p.fecha_prestamo,
                           p.fecha_devolucion_esperada, p.fecha_devolucion_real, p.estado,
                           l.titulo as libro_titulo, u.nombre as usuario_nombre
                    FROM prestamos p
                    JOIN libros l ON p.libro_id = l.id
                    JOIN usuarios u ON p.usuario_id = u.id
                    ORDER BY p.fecha_prestamo DESC
                """)
                return [self._fila_a_prestamo(row) for row in cur.fetchall()]
        except Exception as e:
            raise RuntimeError(f"Error al listar préstamos: {e}")

    def listar_activos(self):
        """Obtiene solo los préstamos activos."""
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT p.id, p.libro_id, p.usuario_id, p.fecha_prestamo,
                           p.fecha_devolucion_esperada, p.fecha_devolucion_real, p.estado,
                           l.titulo as libro_titulo, u.nombre as usuario_nombre
                    FROM prestamos p
                    JOIN libros l ON p.libro_id = l.id
                    JOIN usuarios u ON p.usuario_id = u.id
                    WHERE p.estado = 'activo'
                    ORDER BY p.fecha_prestamo DESC
                """)
                return [self._fila_a_prestamo(row) for row in cur.fetchall()]
        except Exception as e:
            raise RuntimeError(f"Error al listar préstamos activos: {e}")

    def historial_por_libro(self, id_libro):
        """Historial de préstamos de un libro."""
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT p.id, p.libro_id, p.usuario_id, p.fecha_prestamo,
                           p.fecha_devolucion_esperada, p.fecha_devolucion_real, p.estado,
                           l.titulo as libro_titulo, u.nombre as usuario_nombre
                    FROM prestamos p
                    JOIN libros l ON p.libro_id = l.id
                    JOIN usuarios u ON p.usuario_id = u.id
                    WHERE p.libro_id = ?
                    ORDER BY p.fecha_prestamo DESC
                """, (id_libro,))
                return [self._fila_a_prestamo(row) for row in cur.fetchall()]
        except Exception as e:
            raise RuntimeError(f"Error al obtener historial: {e}")

    def historial_por_usuario(self, id_usuario):
        """Historial de préstamos de un usuario."""
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT p.id, p.libro_id, p.usuario_id, p.fecha_prestamo,
                           p.fecha_devolucion_esperada, p.fecha_devolucion_real, p.estado,
                           l.titulo as libro_titulo, u.nombre as usuario_nombre
                    FROM prestamos p
                    JOIN libros l ON p.libro_id = l.id
                    JOIN usuarios u ON p.usuario_id = u.id
                    WHERE p.usuario_id = ?
                    ORDER BY p.fecha_prestamo DESC
                """, (id_usuario,))
                return [self._fila_a_prestamo(row) for row in cur.fetchall()]
        except Exception as e:
            raise RuntimeError(f"Error al obtener historial: {e}")

    def obtener_por_id(self, id_prestamo):
        """Obtiene un préstamo por id."""
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT p.id, p.libro_id, p.usuario_id, p.fecha_prestamo,
                           p.fecha_devolucion_esperada, p.fecha_devolucion_real, p.estado,
                           l.titulo as libro_titulo, u.nombre as usuario_nombre
                    FROM prestamos p
                    JOIN libros l ON p.libro_id = l.id
                    JOIN usuarios u ON p.usuario_id = u.id
                    WHERE p.id = ?
                """, (id_prestamo,))
                row = cur.fetchone()
                return self._fila_a_prestamo(row) if row else None
        except Exception as e:
            raise RuntimeError(f"Error al obtener préstamo: {e}")

    def insertar(self, prestamo):
        """Registra un nuevo préstamo y marca el libro como no disponible."""
        if not prestamo.es_valido():
            raise ValueError("Préstamo inválido: libro, usuario y fechas requeridos")
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute(
                    """INSERT INTO prestamos (libro_id, usuario_id, fecha_prestamo,
                       fecha_devolucion_esperada, fecha_devolucion_real, estado)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (prestamo.libro_id, prestamo.usuario_id, prestamo.fecha_prestamo,
                     prestamo.fecha_devolucion_esperada, prestamo.fecha_devolucion_real or None,
                     prestamo.estado)
                )
                prestamo_id = cur.lastrowid
                cur.execute("UPDATE libros SET disponible = 0 WHERE id = ?", (prestamo.libro_id,))
                return prestamo_id
        except Exception as e:
            raise RuntimeError(f"Error al registrar préstamo: {e}")

    def registrar_devolucion(self, id_prestamo, fecha_devolucion):
        """Marca el préstamo como devuelto y libera el libro."""
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT libro_id FROM prestamos WHERE id = ? AND estado = 'activo'",
                    (id_prestamo,)
                )
                row = cur.fetchone()
                if not row:
                    return False
                cur.execute(
                    """UPDATE prestamos SET estado='devuelto', fecha_devolucion_real=?
                       WHERE id=?""",
                    (fecha_devolucion, id_prestamo)
                )
                cur.execute("UPDATE libros SET disponible = 1 WHERE id = ?", (row['libro_id'],))
                return True
        except Exception as e:
            raise RuntimeError(f"Error al registrar devolución: {e}")

    def contar_activos(self):
        """Cuenta cuántos préstamos están activos."""
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM prestamos WHERE estado = 'activo'")
                return cur.fetchone()[0]
        except Exception as e:
            raise RuntimeError(f"Error al contar préstamos activos: {e}")

    @staticmethod
    def _fila_a_prestamo(row):
        """Convierte una fila en objeto Prestamo con datos extra."""
        p = Prestamo(id_=row['id'], libro_id=row['libro_id'], usuario_id=row['usuario_id'],
                     fecha_prestamo=row['fecha_prestamo'],
                     fecha_devolucion_esperada=row['fecha_devolucion_esperada'],
                     fecha_devolucion_real=row['fecha_devolucion_real'],
                     estado=row['estado'])
        # sqlite3.Row no tiene método .get(); usamos keys() para evitar errores
        p.libro_titulo = row['libro_titulo'] if 'libro_titulo' in row.keys() else ''
        p.usuario_nombre = row['usuario_nombre'] if 'usuario_nombre' in row.keys() else ''
        return p
