class Libros:
    #Constructor de la clase
    def __init__(self, anio=None, referencia=None, autor=None, nombre=None,
                 genero=None, estado=None, fecha_inicio=None, fecha_fin=None):
        #definicion de atributos
        self.anio = anio
        self.referencia = referencia
        self.autor = autor
        self.nombre = nombre
        self.genero = genero
        self.estado = estado
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
    
    #metodo str para mostrar los atributos del libro
    def __str__(self):
        return (f"Libro(referencia='{self.referencia}', nombre='{self.nombre}', autor='{self.autor}', "
                f"anio={self.anio}, genero='{self.genero}', estado='{self.estado}', "
                f"fecha_inicio={self.fecha_inicio}, fecha_fin={self.fecha_fin})")

    '''
    Metodo eq para comparar dos libros por su referencia
    Define la igualdad entre dos instancias de Libros.

        Dos libros se consideran iguales si:
        - 'other' es una instancia de Libros, y
        - Tienen la misma 'referencia' (clave única).
    '''
    def __eq__(self, other):
        if not isinstance(other, Libros):
            return False
        return self.referencia == other.referencia
