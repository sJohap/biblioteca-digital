import sqlite3
import os

# Definición de la ruta del archivo de base de datos.
# Se creará en la misma carpeta del archivo actual con el nombre "libros.db".
DB_PATH = os.path.join(os.path.dirname(__file__), "libros.db")

def get_connection():
    """
    Establece una conexión con la base de datos SQLite.
    Retorna un objeto de conexión si es exitosa, o None en caso de error.
    """
    try:
        conn = sqlite3.connect(DB_PATH)     # Intenta abrir/crear la BD en la ruta indicada
        return conn
    except Exception as e:
        # Manejo básico de errores: muestra el mensaje en consola.
        print(f"❌ Error al conectar a la BD: {e}")
        return None

def init_db():
    """
    Inicializa la base de datos.
    Crea la tabla "libros" si no existe previamente.
    Define las columnas necesarias para almacenar la información de cada libro.
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Sentencia SQL para crear la tabla de libros.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS libros (
                    referencia TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    anio INTEGER NOT NULL,
                    genero TEXT,
                    estado TEXT CHECK(estado IN ('leído','pendiente')) NOT NULL DEFAULT 'pendiente',
                    fecha_inicio TEXT,
                    fecha_final TEXT
                )
            """)
            conn.commit()   # Guarda los cambios en la BD
        finally:
            conn.close()    # Cierra la conexión para liberar recursos
