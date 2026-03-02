"""
Modelo Mascota para la base de datos.
Define la estructura de la tabla 'mascotas' usando SQLAlchemy ORM.
"""

from sqlalchemy import Column, Integer, String, Numeric
from database import Base


class Mascota(Base):
    """
    Clase que representa una mascota en el refugio.
    Mapea a la tabla 'mascotas' en la base de datos.
    """

    __tablename__ = 'mascotas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    """Identificador único de la mascota (autoincremental)"""

    nombre = Column(String(100), nullable=False)
    """Nombre de la mascota - no puede ser nulo"""

    especie = Column(String(50), nullable=False)
    """Especie de la mascota (perro, gato, ave, etc.) - no puede ser nulo"""

    peso = Column(Numeric(10, 2), nullable=False)
    """Peso en kilogramos con 2 decimales - no puede ser nulo"""

    def __repr__(self):
        """
        Representación del objeto para depuración.
        """
        return f"<Mascota(id={self.id}, nombre='{self.nombre}', especie='{self.especie}', peso={self.peso})>"

    def to_dict(self):
        """
        Convierte el objeto a diccionario para facilitar su uso en la UI.
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'especie': self.especie,
            'peso': float(self.peso) if self.peso else None
        }