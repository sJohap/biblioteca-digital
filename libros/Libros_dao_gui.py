"""
Implementación de la interfaz ILibros utilizando SQLite.

Esta clase (LibrosDao) se encarga de la comunicación con la base de datos
para realizar operaciones CRUD y consultas adicionales sobre los libros.

Operaciones principales:
- libros(): obtiene todos los libros (implementación de la interfaz).
- agregar_libro(l): inserta un nuevo libro en la base de datos.
- eliminar_libro(l): elimina un libro por referencia.
- modificar_libro(l): actualiza la información de un libro.
- busca_libro(l): busca un libro por referencia y carga sus datos en el objeto.

Consultas adicionales:
- contar_por_estado(): devuelve un diccionario con el conteo de libros por estado.
- libros_por_genero(genero): obtiene todos los libros filtrados por género.
- obtener_libro(referencia): obtiene un libro completo a partir de su referencia.
- listar_libros(): devuelve una lista con todos los libros ordenados por nombre.
"""
from Ilibros import ILibros
from conexion_gui import get_connection
from Libros import Libros
from typing import List, Dict

class LibrosDao(ILibros):

    def libros(self) -> List[Libros]:
        """Obtiene todos los libros (método requerido por la interfaz)"""
        return self.listar_libros()

    def agregar_libro(self, l: Libros) -> bool:
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO libros
                     (referencia, nombre, autor, anio, genero, estado, fecha_inicio, fecha_final)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(sql, (
                l.referencia,
                l.nombre,
                l.autor,
                l.anio,
                l.genero,
                l.estado,
                l.fecha_inicio,
                l.fecha_fin
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"❌ Error en agregar_libro: {e}")
            return False
        finally:
            conn.close()

    def eliminar_libro(self, l: Libros) -> bool:
        """Elimina un libro por referencia (método requerido por la interfaz)"""
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            sql = "DELETE FROM libros WHERE referencia = ?"
            cursor.execute(sql, (l.referencia,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"❌ Error en eliminar_libro: {e}")
            return False
        finally:
            conn.close()

    def modificar_libro(self, l: Libros) -> bool:
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            sql = """UPDATE libros SET nombre=?, autor=?, anio=?, genero=?, estado=?, 
                     fecha_inicio=?, fecha_final=? WHERE referencia=?"""
            cursor.execute(sql, (
                l.nombre,
                l.autor,
                l.anio,
                l.genero,
                l.estado,
                l.fecha_inicio,
                l.fecha_fin,
                l.referencia
            ))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"❌ Error en modificar_libro: {e}")
            return False
        finally:
            conn.close()

    def busca_libro(self, l: Libros) -> bool:
        """Busca un libro por referencia y carga sus datos en el objeto"""
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            sql = """SELECT referencia, nombre, autor, anio, genero, estado, 
                    fecha_inicio, fecha_final FROM libros WHERE referencia = ?"""
            cursor.execute(sql, (l.referencia,))
            row = cursor.fetchone()
            
            if row:
                # Cargar los datos en el objeto Libros
                l.nombre = row[1]
                l.autor = row[2]
                l.anio = row[3]
                l.genero = row[4]
                l.estado = row[5]
                l.fecha_inicio = row[6]
                l.fecha_fin = row[7]
                return True
            return False
        except Exception as e:
            print(f"❌ Error en busca_libro: {e}")
            return False
        finally:
            conn.close()

    def contar_por_estado(self) -> Dict[str, int]:
        """Cuenta libros por estado (método requerido por la interfaz)"""
        conn = get_connection()
        if not conn:
            return {}
        try:
            cursor = conn.cursor()
            sql = "SELECT estado, COUNT(*) FROM libros GROUP BY estado"
            cursor.execute(sql)
            resultados = cursor.fetchall()
            return {estado: cantidad for estado, cantidad in resultados}
        except Exception as e:
            print(f"❌ Error en contar_por_estado: {e}")
            return {}
        finally:
            conn.close()

    def libros_por_genero(self, genero: str) -> List[Libros]:
        """Obtiene libros por género (método requerido por la interfaz)"""
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            sql = "SELECT referencia, nombre, autor, anio, genero, estado, fecha_inicio, fecha_final FROM libros WHERE genero = ?"
            cursor.execute(sql, (genero,))
            rows = cursor.fetchall()
            libros = []
            for row in rows:
                libros.append(Libros(
                    referencia=row[0],
                    nombre=row[1],
                    autor=row[2],
                    anio=row[3],
                    genero=row[4],
                    estado=row[5],
                    fecha_inicio=row[6],
                    fecha_fin=row[7]
                ))
            return libros
        except Exception as e:
            print(f"❌ Error en libros_por_genero: {e}")
            return []
        finally:
            conn.close()

    def obtener_libro(self, referencia: str) -> Libros:
        """Método adicional para obtener un libro completo por referencia"""
        conn = get_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            sql = "SELECT referencia, nombre, autor, anio, genero, estado, fecha_inicio, fecha_final FROM libros WHERE referencia=?"
            cursor.execute(sql, (referencia,))
            row = cursor.fetchone()
            if row:
                return Libros(
                    referencia=row[0],
                    nombre=row[1],
                    autor=row[2],
                    anio=row[3],
                    genero=row[4],
                    estado=row[5],
                    fecha_inicio=row[6],
                    fecha_fin=row[7]
                )
            return None
        except Exception as e:
            print(f"❌ Error en obtener_libro: {e}")
            return None
        finally:
            conn.close()

    def listar_libros(self) -> List[Libros]:
        """Método adicional para listar todos los libros"""
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            sql = "SELECT referencia, nombre, autor, anio, genero, estado, fecha_inicio, fecha_final FROM libros ORDER BY nombre"
            cursor.execute(sql)
            rows = cursor.fetchall()
            libros = []
            for row in rows:
                libros.append(Libros(
                    referencia=row[0],
                    nombre=row[1],
                    autor=row[2],
                    anio=row[3],
                    genero=row[4],
                    estado=row[5],
                    fecha_inicio=row[6],
                    fecha_fin=row[7]
                ))
            return libros
        except Exception as e:
            print(f"❌ Error en listar_libros: {e}")
            return []
        finally:
            conn.close()