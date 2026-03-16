"""
Repository para la entidad Autor.
Gestiona el acceso y manipulación de autores en SQLite.
"""
from database import obtener_conexion
from models.autor import Autor


class AutorRepository:
    """Acceso a datos de autores."""

    def listar_todos(self):
        """Obtiene todos los autores ordenados por nombre."""
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute("SELECT id, nombre, nacionalidad, biografia FROM autores ORDER BY nombre")
                return [self._fila_a_autor(row) for row in cur.fetchall()]
        except Exception as e:
            raise RuntimeError(f"Error al listar autores: {e}")

    def obtener_por_id(self, id_autor):
        """Obtiene un autor por su id o None si no existe."""
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT id, nombre, nacionalidad, biografia FROM autores WHERE id = ?",
                    (id_autor,)
                )
                row = cur.fetchone()
                return self._fila_a_autor(row) if row else None
        except Exception as e:
            raise RuntimeError(f"Error al obtener autor: {e}")

    def insertar(self, autor):
        """Inserta un nuevo autor. Retorna el id asignado."""
        if not autor.es_valido():
            raise ValueError("Autor inválido: nombre requerido")
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO autores (nombre, nacionalidad, biografia) VALUES (?, ?, ?)",
                    (autor.nombre.strip(), autor.nacionalidad or '', autor.biografia or '')
                )
                return cur.lastrowid
        except Exception as e:
            raise RuntimeError(f"Error al insertar autor: {e}")

    def actualizar(self, autor):
        """Actualiza un autor existente."""
        if not autor.es_valido() or autor.id is None:
            raise ValueError("Autor inválido o sin id")
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute(
                    """UPDATE autores SET nombre=?, nacionalidad=?, biografia=? WHERE id=?""",
                    (autor.nombre.strip(), autor.nacionalidad or '', autor.biografia or '', autor.id)
                )
                return cur.rowcount > 0
        except Exception as e:
            raise RuntimeError(f"Error al actualizar autor: {e}")

    def eliminar(self, id_autor):
        """Elimina un autor por id."""
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM autores WHERE id = ?", (id_autor,))
                return cur.rowcount > 0
        except Exception as e:
            raise RuntimeError(f"Error al eliminar autor: {e}")

    @staticmethod
    def _fila_a_autor(row):
        """Convierte una fila de BD en instancia de Autor."""
        return Autor(id_=row['id'], nombre=row['nombre'],
                     nacionalidad=row['nacionalidad'] or '',
                     biografia=row['biografia'] or '')
