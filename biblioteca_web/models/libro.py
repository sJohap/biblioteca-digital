"""
Modelo de dominio para la entidad Libro.
Almacena la información bibliográfica y el estado de disponibilidad.
"""


class Libro:
    """Entidad que representa un ejemplar en el catálogo."""

    def __init__(self, id_=None, titulo=None, isbn=None, autor_id=None,
                 anio=None, genero=None, disponible=True):
        self.id = id_
        self.titulo = titulo or ''
        self.isbn = isbn or ''
        self.autor_id = autor_id
        self.anio = anio
        self.genero = genero or ''
        self.disponible = disponible if isinstance(disponible, bool) else bool(disponible)

    def __str__(self):
        return f"Libro(id={self.id}, titulo='{self.titulo}', disponible={self.disponible})"

    def __repr__(self):
        return self.__str__()

    def es_valido(self):
        """Comprueba que el título no esté vacío y exista autor_id."""
        return bool(self.titulo and self.titulo.strip() and self.autor_id is not None)
