"""
Repository para la entidad Usuario.
Gestiona el acceso y manipulación de usuarios en SQLite.
"""
import sqlite3
from database import obtener_conexion
from models.usuario import Usuario


class UsuarioRepository:
    """Acceso a datos de usuarios."""

    def listar_todos(self):
        """Obtiene todos los usuarios ordenados por nombre."""
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute("SELECT id, nombre, email, telefono FROM usuarios ORDER BY nombre")
                return [self._fila_a_usuario(row) for row in cur.fetchall()]
        except Exception as e:
            raise RuntimeError(f"Error al listar usuarios: {e}")

    def obtener_por_id(self, id_usuario):
        """Obtiene un usuario por id."""
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT id, nombre, email, telefono FROM usuarios WHERE id = ?",
                    (id_usuario,)
                )
                row = cur.fetchone()
                return self._fila_a_usuario(row) if row else None
        except Exception as e:
            raise RuntimeError(f"Error al obtener usuario: {e}")

    def insertar(self, usuario):
        """Inserta un nuevo usuario."""
        if not usuario.es_valido():
            raise ValueError("Usuario inválido: nombre y email requeridos")
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO usuarios (nombre, email, telefono) VALUES (?, ?, ?)",
                    (usuario.nombre.strip(), usuario.email.strip(), usuario.telefono or '')
                )
                return cur.lastrowid
        except sqlite3.IntegrityError as e:
            raise ValueError(f"El email ya está registrado: {e}")
        except Exception as e:
            raise RuntimeError(f"Error al insertar usuario: {e}")

    def actualizar(self, usuario):
        """Actualiza un usuario existente."""
        if not usuario.es_valido() or usuario.id is None:
            raise ValueError("Usuario inválido o sin id")
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute(
                    "UPDATE usuarios SET nombre=?, email=?, telefono=? WHERE id=?",
                    (usuario.nombre.strip(), usuario.email.strip(),
                     usuario.telefono or '', usuario.id)
                )
                return cur.rowcount > 0
        except Exception as e:
            raise RuntimeError(f"Error al actualizar usuario: {e}")

    def eliminar(self, id_usuario):
        """Elimina un usuario por id."""
        try:
            with obtener_conexion() as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
                return cur.rowcount > 0
        except Exception as e:
            raise RuntimeError(f"Error al eliminar usuario: {e}")

    @staticmethod
    def _fila_a_usuario(row):
        """Convierte una fila de BD en instancia de Usuario."""
        return Usuario(id_=row['id'], nombre=row['nombre'],
                       email=row['email'], telefono=row['telefono'] or '')
