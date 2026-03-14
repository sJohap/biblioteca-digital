"""
Gestión de la conexión a SQLite y creación del esquema.
Provee la inicialización de tablas y utilidades de acceso a datos.
"""
import sqlite3
from contextlib import contextmanager
from config import RUTA_BD


@contextmanager
def obtener_conexion():
    """
    Context manager para obtener una conexión a la base de datos.
    Garantiza el cierre correcto de la conexión al finalizar el bloque.
    """
    conn = sqlite3.connect(RUTA_BD)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def preparar_almacenamiento():
    """
    Crea todas las tablas necesarias si no existen.
    Incluye: autores, libros, usuarios, prestamos.
    """
    with obtener_conexion() as conn:
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS autores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                nacionalidad TEXT,
                biografia TEXT
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS libros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                isbn TEXT UNIQUE,
                autor_id INTEGER NOT NULL,
                anio INTEGER,
                genero TEXT,
                disponible INTEGER DEFAULT 1,
                FOREIGN KEY (autor_id) REFERENCES autores(id)
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                telefono TEXT
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS prestamos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                libro_id INTEGER NOT NULL,
                usuario_id INTEGER NOT NULL,
                fecha_prestamo TEXT NOT NULL,
                fecha_devolucion_esperada TEXT NOT NULL,
                fecha_devolucion_real TEXT,
                estado TEXT DEFAULT 'activo' CHECK(estado IN ('activo', 'devuelto')),
                FOREIGN KEY (libro_id) REFERENCES libros(id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)
