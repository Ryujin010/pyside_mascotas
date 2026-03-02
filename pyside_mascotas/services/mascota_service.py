"""
Servicio de Mascotas - Capa de acceso a datos.
Proporciona métodos para interactuar con la base de datos.
Ahora con soporte para paginación.
"""

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', 'admin')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'pyside_mascotas_db')

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear motor y sesión
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class MascotaService:
    """
    Servicio para gestionar operaciones CRUD de mascotas.
    """

    def __init__(self):
        """Inicializa el servicio sin sesión activa."""
        self.db: Session = None

    def __enter__(self):
        """Método para usar el servicio con context manager (with)."""
        self.db = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra la sesión automáticamente al salir del context manager."""
        if self.db:
            if exc_type:
                self.db.rollback()
            self.db.close()

    # ===== MÉTODOS ORIGINALES =====
    def obtener_todos(self):
        """
        Obtiene todas las mascotas de la base de datos.

        Returns:
            list: Lista de objetos Mascota
        """
        from models.mascota import Mascota
        return self.db.query(Mascota).all()

    def obtener_estadisticas(self):
        """
        Obtiene estadísticas de las mascotas.

        Returns:
            dict: Diccionario con:
                - total: número total de mascotas
                - por_especie: diccionario con conteo por especie
                - peso_promedio: peso promedio de todas las mascotas
        """
        from models.mascota import Mascota

        try:
            # Total de mascotas
            total = self.db.query(Mascota).count()

            # Conteo por especie
            especies_query = self.db.query(
                Mascota.especie,
                func.count(Mascota.id).label('cantidad')
            ).group_by(Mascota.especie).all()

            por_especie = {especie: cantidad for especie, cantidad in especies_query}

            # Peso promedio
            peso_promedio = self.db.query(func.avg(Mascota.peso)).scalar()

            return {
                'total': total,
                'por_especie': por_especie,
                'peso_promedio': float(peso_promedio) if peso_promedio else 0
            }

        except Exception as e:
            raise Exception(f"Error al obtener estadísticas: {str(e)}")

    def obtener_por_id(self, mascota_id):
        """
        Obtiene una mascota por su ID.

        Args:
            mascota_id (int): ID de la mascota a buscar

        Returns:
            Mascota: La mascota encontrada o None si no existe

        Raises:
            ValueError: Si el ID no es válido
            Exception: Si ocurre un error en la base de datos
        """
        from models.mascota import Mascota

        if not mascota_id or mascota_id <= 0:
            raise ValueError("ID de mascota no válido")

        try:
            mascota = self.db.query(Mascota).filter(Mascota.id == mascota_id).first()

            if not mascota:
                raise ValueError(f"No existe una mascota con ID {mascota_id}")

            return mascota

        except Exception as e:
            raise Exception(f"Error al buscar mascota: {str(e)}")

    def actualizar(self, mascota_id, datos):
        """
        Actualiza una mascota existente en la base de datos.

        Args:
            mascota_id (int): ID de la mascota a actualizar
            datos (dict): Diccionario con los campos a actualizar: nombre, especie, peso

        Returns:
            Mascota: La mascota actualizada

        Raises:
            ValueError: Si los datos no son válidos o la mascota no existe
            Exception: Si ocurre un error en la base de datos
        """
        from models.mascota import Mascota

        if not mascota_id or mascota_id <= 0:
            raise ValueError("ID de mascota no válido")

        if not datos.get('nombre'):
            raise ValueError("El nombre es obligatorio")

        if not datos.get('especie'):
            raise ValueError("La especie es obligatoria")

        if not datos.get('peso'):
            raise ValueError("El peso es obligatorio")

        try:
            peso = float(datos['peso'])
            if peso <= 0:
                raise ValueError("El peso debe ser mayor a 0")
            if peso > 1000:
                raise ValueError("El peso no puede ser mayor a 1000 kg")
        except (ValueError, TypeError):
            raise ValueError("El peso debe ser un número válido")

        try:
            mascota = self.db.query(Mascota).filter(Mascota.id == mascota_id).first()

            if not mascota:
                raise ValueError(f"No existe una mascota con ID {mascota_id}")

            mascota.nombre = datos['nombre'].strip()
            mascota.especie = datos['especie'].strip()
            mascota.peso = peso

            self.db.commit()
            self.db.refresh(mascota)

            return mascota

        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al actualizar en base de datos: {str(e)}")

    def eliminar(self, mascota_id):
        """
        Elimina una mascota de la base de datos.

        Args:
            mascota_id (int): ID de la mascota a eliminar

        Returns:
            bool: True si se eliminó correctamente

        Raises:
            ValueError: Si el ID no es válido o la mascota no existe
            Exception: Si ocurre un error en la base de datos
        """
        from models.mascota import Mascota

        if not mascota_id or mascota_id <= 0:
            raise ValueError("ID de mascota no válido")

        try:
            mascota = self.db.query(Mascota).filter(Mascota.id == mascota_id).first()

            if not mascota:
                raise ValueError(f"No existe una mascota con ID {mascota_id}")

            self.db.delete(mascota)
            self.db.commit()

            return True

        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al eliminar en base de datos: {str(e)}")

    def crear(self, datos):
        """
        Crea una nueva mascota en la base de datos.

        Args:
            datos (dict): Diccionario con los campos: nombre, especie, peso

        Returns:
            Mascota: La mascota creada con su ID asignado

        Raises:
            ValueError: Si los datos no son válidos
            Exception: Si ocurre un error en la base de datos
        """
        from models.mascota import Mascota

        if not datos.get('nombre'):
            raise ValueError("El nombre es obligatorio")

        if not datos.get('especie'):
            raise ValueError("La especie es obligatoria")

        if not datos.get('peso'):
            raise ValueError("El peso es obligatorio")

        try:
            peso = float(datos['peso'])
            if peso <= 0:
                raise ValueError("El peso debe ser mayor a 0")
            if peso > 1000:
                raise ValueError("El peso no puede ser mayor a 1000 kg")
        except (ValueError, TypeError):
            raise ValueError("El peso debe ser un número válido")

        nueva_mascota = Mascota(
            nombre=datos['nombre'].strip(),
            especie=datos['especie'].strip(),
            peso=peso
        )

        try:
            self.db.add(nueva_mascota)
            self.db.commit()
            self.db.refresh(nueva_mascota)
            return nueva_mascota
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al guardar en base de datos: {str(e)}")

    # ===== [NUEVO] MÉTODOS DE PAGINACIÓN =====

    def contar_total(self):
        """
        Cuenta el total de mascotas en la base de datos.

        Returns:
            int: Número total de mascotas
        """
        from models.mascota import Mascota
        return self.db.query(Mascota).count()

    def obtener_pagina(self, offset, limit):
        """
        Obtiene una página de mascotas.

        Args:
            offset (int): Número de registros a saltar
            limit (int): Número máximo de registros a obtener

        Returns:
            list: Lista de objetos Mascota de la página solicitada
        """
        from models.mascota import Mascota
        return self.db.query(Mascota).offset(offset).limit(limit).all()

    def obtener_pagina_con_filtro(self, offset, limit, filtro=""):
        """
        Obtiene una página de mascotas aplicando un filtro de búsqueda.

        Args:
            offset (int): Número de registros a saltar
            limit (int): Número máximo de registros a obtener
            filtro (str): Texto para filtrar por nombre o especie

        Returns:
            list: Lista de objetos Mascota filtrados de la página solicitada
        """
        from models.mascota import Mascota

        query = self.db.query(Mascota)

        if filtro:
            filtro_lower = f"%{filtro.lower()}%"
            query = query.filter(
                (Mascota.nombre.ilike(filtro_lower)) |
                (Mascota.especie.ilike(filtro_lower))
            )

        return query.offset(offset).limit(limit).all()

    def contar_con_filtro(self, filtro=""):
        """
        Cuenta el total de mascotas que coinciden con un filtro.

        Args:
            filtro (str): Texto para filtrar por nombre o especie

        Returns:
            int: Número total de mascotas que coinciden con el filtro
        """
        from models.mascota import Mascota

        query = self.db.query(Mascota)

        if filtro:
            filtro_lower = f"%{filtro.lower()}%"
            query = query.filter(
                (Mascota.nombre.ilike(filtro_lower)) |
                (Mascota.especie.ilike(filtro_lower))
            )

        return query.count()