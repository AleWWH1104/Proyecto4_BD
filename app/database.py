from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin@localhost:5430/peluzoo")

# Crear el motor de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=5,
    pool_pre_ping=True,
    pool_recycle=3600
)

# Configurar la sesion
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

def get_db():
    """Obtener una sesion de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    """probar la conexion a la base de datos"""
    try:
        # Usar pandas para probar la conexión con una consulta simple
        df = pd.read_sql("SELECT 1 as connection_test", con=engine)
        print("✅ Conexión exitosa a la base de datos")
        print(df)
        return True
    except Exception as e:
        print("❌ Error de conexión a la base de datos:")
        print(str(e))
        return False
    

def execute_query_to_dataframe(query: str, params=None):
    """
    Ejecuta una consulta SQL y devuelve un DataFrame de pandas
    """
    try:
        df = pd.read_sql_query(query, con=engine, params=params)
        return df
    except Exception as e:
        print(f"Error ejecutando consulta: {str(e)}")
        return pd.DataFrame() 