"""
Repository para la entidad Libro.
Gestiona el acceso y manipulación de libros en SQLite.
"""
from database import obtener_conexion
from models.libro import Libro


class LibroRepository:
    """Acceso a datos de libros."""

    def listar_todos(self):
        """Obtiene todos los libros con nombre del autor."""
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT l.id, l.titulo, l.isbn, l.autor_id, l.anio, l.genero, l.disponible,
                           a.nombre as autor_nombre
                    FROM libros l LEFT JOIN autores a ON l.autor_id = a.id
                    ORDER BY l.titulo
                """)
                return [self._fila_a_libro(row) for row in cur.fetchall()]
        except Exception as e:
            raise RuntimeError(f"Error al listar libros: {e}")

    def obtener_por_id(self, id_libro):
        """Obtiene un libro por id, con nombre de autor."""
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT l.id, l.titulo, l.isbn, l.autor_id, l.anio, l.genero, l.disponible,
                           a.nombre as autor_nombre
                    FROM libros l LEFT JOIN autores a ON l.autor_id = a.id
                    WHERE l.id = ?
                """, (id_libro,))
                row = cur.fetchone()
                return self._fila_a_libro(row) if row else None
        except Exception as e:
            raise RuntimeError(f"Error al obtener libro: {e}")

    def listar_disponibles(self):
        """Lista solo los libros disponibles para préstamo."""
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT l.id, l.titulo, l.isbn, l.autor_id, l.anio, l.genero, l.disponible,
                           a.nombre as autor_nombre
                    FROM libros l LEFT JOIN autores a ON l.autor_id = a.id
                    WHERE l.disponible = 1 ORDER BY l.titulo
                """)
                return [self._fila_a_libro(row) for row in cur.fetchall()]
        except Exception as e:
            raise RuntimeError(f"Error al listar libros disponibles: {e}")

    def buscar_por_titulo(self, texto):
        """Busca libros cuyo título contenga el texto (case insensitive)."""
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT l.id, l.titulo, l.isbn, l.autor_id, l.anio, l.genero, l.disponible,
                           a.nombre as autor_nombre
                    FROM libros l LEFT JOIN autores a ON l.autor_id = a.id
                    WHERE LOWER(l.titulo) LIKE LOWER(?)
                    ORDER BY l.titulo
                """, (f'%{texto}%',))
                return [self._fila_a_libro(row) for row in cur.fetchall()]
        except Exception as e:
            raise RuntimeError(f"Error al buscar libros: {e}")

    def filtrar_por_genero(self, genero):
        """Obtiene libros filtrados por género."""
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT l.id, l.titulo, l.isbn, l.autor_id, l.anio, l.genero, l.disponible,
                           a.nombre as autor_nombre
                    FROM libros l LEFT JOIN autores a ON l.autor_id = a.id
                    WHERE LOWER(l.genero) = LOWER(?)
                    ORDER BY l.titulo
                """, (genero or '',))
                return [self._fila_a_libro(row) for row in cur.fetchall()]
        except Exception as e:
            raise RuntimeError(f"Error al filtrar por género: {e}")

    def insertar(self, libro):
        """Inserta un nuevo libro."""
        if not libro.es_valido():
            raise ValueError("Libro inválido: título y autor requeridos")
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute(
                    """INSERT INTO libros (titulo, isbn, autor_id, anio, genero, disponible)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (libro.titulo.strip(), libro.isbn or None, libro.autor_id,
                     libro.anio, libro.genero or '', 1 if libro.disponible else 0)
                )
                return cur.lastrowid
        except Exception as e:
            raise RuntimeError(f"Error al insertar libro: {e}")

    def actualizar(self, libro):
        """Actualiza un libro existente."""
        if not libro.es_valido() or libro.id is None:
            raise ValueError("Libro inválido o sin id")
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute(
                    """UPDATE libros SET titulo=?, isbn=?, autor_id=?, anio=?, genero=?, disponible=?
                       WHERE id=?""",
                    (libro.titulo.strip(), libro.isbn or None, libro.autor_id,
                     libro.anio, libro.genero or '', 1 if libro.disponible else 0, libro.id)
                )
                return cur.rowcount > 0
        except Exception as e:
            raise RuntimeError(f"Error al actualizar libro: {e}")

    def marcar_disponibilidad(self, id_libro, disponible):
        """Actualiza únicamente el campo disponible de un libro."""
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute(
                    "UPDATE libros SET disponible = ? WHERE id = ?",
                    (1 if disponible else 0, id_libro)
                )
                return cur.rowcount > 0
        except Exception as e:
            raise RuntimeError(f"Error al actualizar disponibilidad: {e}")

    def eliminar(self, id_libro):
        """Elimina un libro por id."""
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM libros WHERE id = ?", (id_libro,))
                return cur.rowcount > 0
        except Exception as e:
            raise RuntimeError(f"Error al eliminar libro: {e}")

    @staticmethod
    def _fila_a_libro(row):
        """Convierte una fila de BD en diccionario con libro y nombre de autor."""
        lib = Libro(id_=row['id'], titulo=row['titulo'], isbn=row['isbn'] or '',
                    autor_id=row['autor_id'], anio=row['anio'], genero=row['genero'] or '',
                    disponible=bool(row['disponible']))
        lib.autor_nombre = row.get('autor_nombre', '')
        return lib
