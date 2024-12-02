from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Cargar las variables del archivo .env
load_dotenv()

# Configura la URL de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

# Motor de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para definir los modelos
Base = declarative_base()

# Función para obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()