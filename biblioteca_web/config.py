"""
Configuración global del sistema Biblioteca Digital.
Almacena rutas, claves y banderas de ejecución.
"""
import os

DIRECTORIO_BASE = os.path.abspath(os.path.dirname(__file__))
RUTA_BD = os.path.join(DIRECTORIO_BASE, 'biblioteca.db')
CLAVE_SECRETA = os.environ.get('CLAVE_SECRETA', 'clave-desarrollo-biblioteca-2024')
DEBUG = True
