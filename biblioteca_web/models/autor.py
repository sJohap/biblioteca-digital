"""
Modelo de dominio para la entidad Autor.
Representa a un escritor vinculado a uno o más libros.
"""


class Autor:
    """Entidad que describe a un autor de libros."""

    def __init__(self, id_=None, nombre=None, nacionalidad=None, biografia=None):
        self.id = id_
        self.nombre = nombre or ''
        self.nacionalidad = nacionalidad or ''
        self.biografia = biografia or ''

    def __str__(self):
        return f"Autor(id={self.id}, nombre='{self.nombre}')"

    def __repr__(self):
        return self.__str__()

    def es_valido(self):
        """Comprueba si el autor tiene nombre no vacío."""
        return bool(self.nombre and self.nombre.strip())
