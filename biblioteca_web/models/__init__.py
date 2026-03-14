"""
Módulo de modelos de dominio.
Exporta las entidades del sistema: Autor, Libro, Usuario, Prestamo.
"""
from .autor import Autor
from .libro import Libro
from .usuario import Usuario
from .prestamo import Prestamo

__all__ = ['Autor', 'Libro', 'Usuario', 'Prestamo']
