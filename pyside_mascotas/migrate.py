#!/usr/bin/env python
"""
Script automatizado para gestionar migraciones con Alembic.
Ejecuta: python migrate.py
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import subprocess

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', 'TU_PASSWORD_REAL')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'pyside_mascotas_db')

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def limpiar_version_huerfana():
    """
    Elimina la tabla alembic_version si existe y está huérfana.
    Esto evita conflictos al iniciar migraciones desde cero.
    """
    print("🔍 Verificando versiones huérfanas de Alembic...")

    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            # Verificar si la tabla alembic_version existe
            result = conn.execute(
                text("SHOW TABLES LIKE 'alembic_version'")
            ).fetchone()

            if result:
                print("⚠️  Tabla 'alembic_version' encontrada. Eliminando...")
                conn.execute(text("DROP TABLE alembic_version"))
                conn.commit()
                print("✅ Tabla 'alembic_version' eliminada.")
            else:
                print("✅ No hay versiones huérfanas de Alembic.")

    except Exception as e:
        print(f"❌ Error al verificar/limpiar versiones: {e}")


def generar_migracion():
    """
    Genera una nueva migración autogenerada basada en los modelos.
    """
    print("\n📝 Generando nueva migración...")
    try:
        # Usar subprocess para ejecutar comandos de alembic
        result = subprocess.run(
            ["alembic", "revision", "--autogenerate", "-m", "crear tabla mascotas"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("✅ Migración generada exitosamente:")
            print(result.stdout)
        else:
            print("❌ Error al generar migración:")
            print(result.stderr)
            return False
        return True
    except Exception as e:
        print(f"❌ Error al ejecutar alembic: {e}")
        return False


def aplicar_migracion():
    """
    Aplica la migración a la base de datos (upgrade head).
    """
    print("\n⬆️  Aplicando migración a la base de datos...")
    try:
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("✅ Migración aplicada exitosamente:")
            print(result.stdout)
        else:
            print("❌ Error al aplicar migración:")
            print(result.stderr)
            return False
        return True
    except Exception as e:
        print(f"❌ Error al ejecutar alembic: {e}")
        return False


def main():
    """
    Función principal que ejecuta todo el proceso de migración.
    """
    print("=" * 50)
    print("🚀 INICIANDO PROCESO DE MIGRACIÓN")
    print("=" * 50)

    # Paso 1: Limpiar versiones huérfanas
    limpiar_version_huerfana()

    # Paso 2: Generar migración
    if not generar_migracion():
        print("❌ Proceso detenido por error en generación de migración.")
        return

    # Paso 3: Aplicar migración
    if not aplicar_migracion():
        print("❌ Proceso detenido por error al aplicar migración.")
        return

    print("\n" + "=" * 50)
    print("✅ PROCESO DE MIGRACIÓN COMPLETADO EXITOSAMENTE")
    print("=" * 50)


if __name__ == "__main__":
    main()