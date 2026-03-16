"""
Capa de acceso a datos (repositories).
Encapsula las operaciones CRUD sobre la base de datos.
"""
from .autor_repository import AutorRepository
from .libro_repository import LibroRepository
from .usuario_repository import UsuarioRepository
from .prestamo_repository import PrestamoRepository

__all__ = ['AutorRepository', 'LibroRepository', 'UsuarioRepository', 'PrestamoRepository']
