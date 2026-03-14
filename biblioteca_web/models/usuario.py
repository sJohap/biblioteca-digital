"""
Modelo de dominio para la entidad Usuario.
Representa a una persona que puede solicitar préstamos.
"""


class Usuario:
    """Entidad que identifica a un usuario de la biblioteca."""

    def __init__(self, id_=None, nombre=None, email=None, telefono=None):
        self.id = id_
        self.nombre = nombre or ''
        self.email = email or ''
        self.telefono = telefono or ''

    def __str__(self):
        return f"Usuario(id={self.id}, nombre='{self.nombre}', email='{self.email}')"

    def __repr__(self):
        return self.__str__()

    def es_valido(self):
        """Comprueba que nombre y email no estén vacíos."""
        return bool(
            self.nombre and self.nombre.strip() and
            self.email and self.email.strip()
        )
