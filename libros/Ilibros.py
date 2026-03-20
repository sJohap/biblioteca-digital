"""
Interfaz ILibros para la gestión de libros.

Esta clase abstracta define las operaciones que cualquier implementación
debe cumplir para manejar libros en el sistema.

Métodos principales:
- libros(): devuelve una lista de objetos Libros.
- agregar_libro(l): agrega un nuevo libro.
- modificar_libro(l): modifica los datos de un libro existente.
- eliminar_libro(l): elimina un libro del sistema.
- busca_libro(l): busca un libro específico.

Métodos adicionales:
- contar_por_estado(): devuelve un diccionario con la cantidad de libros por estado.
- libros_por_genero(genero): devuelve una lista de libros filtrados por género.
"""
from abc import ABC, abstractmethod
from typing import List
from Libros import Libros

class ILibros(ABC):
    @abstractmethod
    def libros(self) -> List[Libros]:
        pass

    @abstractmethod
    def agregar_libro(self, l: Libros) -> bool:
        pass

    @abstractmethod
    def modificar_libro(self, l: Libros) -> bool:
        pass

    @abstractmethod
    def eliminar_libro(self, l: Libros) -> bool:
        pass

    @abstractmethod
    def busca_libro(self, l: Libros) -> bool:
        pass

    # Nuevos métodos
    @abstractmethod
    def contar_por_estado(self) -> dict:
        pass

    @abstractmethod
    def libros_por_genero(self, genero: str) -> List[Libros]:
        pass