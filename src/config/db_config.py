# src/config/db_config.py

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from .settings import settings


# 1. Construir la URL de la base de datos
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"

# 2. Crear el engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

with engine.connect() as con:
    statement = text("CREATE EXTENSION IF NOT EXISTS unaccent;COMMIT;")
    con.execute(statement)

# 4. Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Declarative Base para tus modelos
Base = declarative_base()


# 6. Función para obtener la sesión en cada request (FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
