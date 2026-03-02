import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener credenciales de la base de datos
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', 'TU_PASSWORD_REAL')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'pyside_mascotas_db')

# Construir URL de conexión para MySQL con PyMySQL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear el motor de base de datos
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Muestra las consultas SQL en consola (útil para desarrollo)
    pool_pre_ping=True  # Verifica la conexión antes de usarla
)

# Crear fábrica de sesiones
Session = sessionmaker(bind=engine)

# Clase base para modelos SQLAlchemy
Base = declarative_base()


def probar_conexion():
    """
    Función para probar la conexión a la base de datos.
    Intenta conectar y muestra el resultado.
    """
    print("🔌 Probando conexión a MySQL...")
    print(f"📊 Base de datos: {DB_NAME}")
    print(f"🔗 URL: {DATABASE_URL.replace(DB_PASS, '******')}")  # Ocultamos la contraseña

    try:
        # Intentar conectar
        with engine.connect() as conn:
            print("✅ ¡Conexión exitosa!")
            print(f"   Objeto de conexión: {conn}")
            print(f"   Motor: {engine}")
            return True
    except Exception as e:
        print("❌ Error de conexión:")
        print(f"   {type(e).__name__}: {e}")
        return False


if __name__ == "__main__":
    """
    Si ejecutamos este script directamente, probamos la conexión.
    """
    probar_conexion()