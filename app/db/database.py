import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Leer las variables del archivo .env
load_dotenv()

# Obtener la URL de PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("No se encontró DATABASE_URL")

# Configurar el motor de conexión
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# Preparar sesiones para operar con la BD
SessionLocal = sessionmaker(bind=engine)