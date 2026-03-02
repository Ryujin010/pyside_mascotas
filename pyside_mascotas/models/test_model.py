# test_model.py (archivo temporal, no incluido en el proyecto final)
from database import Base
from models.mascota import Mascota

print("✅ Modelo Mascota importado correctamente")
print(f"📋 Nombre de la tabla: {Mascota.__tablename__}")
print(f"📊 Columnas: {[col.name for col in Mascota.__table__.columns]}")
print(f"🔑 Primary key: {Mascota.__table__.primary_key.columns.keys()}")