# app/database.py
from sqlalchemy import create_engine, TypeDecorator, String, DECIMAL, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
import os
import json # Importar para serializar/deserializar JSON

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

# --- NUEVO: Tipo de dato personalizado para Coordenadas ---
class CoordenadasType(TypeDecorator):
    """
    Tipo de dato personalizado para mapear el tipo compuesto 'coordenadas' de PostgreSQL.
    Lo almacenaremos como TEXT en la base de datos, serializando/deserializando a JSON.
    """
    impl = String # O String para almacenar como texto si no se soporta JSONB

    cache_ok = True # Para versiones más recientes de SQLAlchemy

    def process_bind_param(self, value, dialect):
        """Convierte el objeto Python (diccionario) a una cadena JSON para la DB."""
        if value is not None:
            # PostgreSQL espera una cadena de texto para el tipo compuesto, no un JSONB literal.
            # Convertimos el diccionario a una cadena de tupla SQL.
            # Ejemplo: (1.23, 4.56, 100)
            if not isinstance(value, dict):
                raise TypeError("Coordenadas must be a dictionary with latitud, longitud, altitud.")
            
            lat = value.get("latitud")
            lon = value.get("longitud")
            alt = value.get("altitud")

            # Aseguramos el formato de decimal para latitud/longitud y entero para altitud
            lat_str = f"{float(lat):.8f}" if lat is not None else "NULL"
            lon_str = f"{float(lon):.8f}" if lon is not None else "NULL"
            alt_str = str(int(alt)) if alt is not None else "NULL"

            return f"({lat_str},{lon_str},{alt_str})"
        return value

    def process_result_value(self, value, dialect):
        """Convierte la cadena de la DB de vuelta a un objeto Python (diccionario)."""
        if value is not None:
            # Parsea la cadena de tupla de PostgreSQL (ej. "(1.23,4.56,100)")
            # y la convierte en un diccionario.
            value = value.strip('()') # Eliminar paréntesis
            parts = value.split(',')
            
            latitud = float(parts[0]) if parts[0] != 'NULL' else None
            longitud = float(parts[1]) if parts[1] != 'NULL' else None
            altitud = int(parts[2]) if parts[2] != 'NULL' else None

            return {"latitud": latitud, "longitud": longitud, "altitud": altitud}
        return value

# Puedes hacer lo mismo para otros tipos compuestos si los necesitas:
# class InfoNutricionalType(TypeDecorator):
#     impl = String # O TEXT
#     cache_ok = True
#     def process_bind_param(self, value, dialect):
#         return json.dumps(value) if value is not None else value
#     def process_result_value(self, value, dialect):
#         return json.loads(value) if value is not None else value

# class HorarioEventoType(TypeDecorator):
#     impl = String # O TEXT
#     cache_ok = True
#     def process_bind_param(self, value, dialect):
#         return json.dumps(value) if value is not None else value
#     def process_result_value(self, value, dialect):
#         return json.loads(value) if value is not None else value
# --- FIN NUEVO ---

# --- NUEVO: Tipo de dato personalizado para HorarioEvento ---
class HorarioEventoType(TypeDecorator):
    impl = String # Usamos String para almacenar la representación textual de la tupla SQL
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """Convierte el diccionario Python a una cadena de tupla SQL para la DB."""
        if value is not None:
            if not isinstance(value, dict):
                raise TypeError("HorarioEvento must be a dictionary.")
            
            # Asegúrate de que los días de la semana sean un array de enteros, y conviértelos a la sintaxis de array de PostgreSQL
            dias_semana_str = "{" + ",".join(map(str, value.get("dias_semana", []))) + "}" if value.get("dias_semana") else "{}"
            hora_inicio_str = f"'{value['hora_inicio']}'" if 'hora_inicio' in value else "NULL"
            hora_fin_str = f"'{value['hora_fin']}'" if 'hora_fin' in value else "NULL"
            duracion_minutos_str = str(int(value['duracion_minutos'])) if 'duracion_minutos' in value else "NULL"
            frecuencia_str = f"'{value['frecuencia']}'" if 'frecuencia' in value else "NULL"

            # Formato de la tupla para PostgreSQL: (dias_semana, hora_inicio, hora_fin, duracion_minutos, frecuencia)
            return f"({dias_semana_str},{hora_inicio_str},{hora_fin_str},{duracion_minutos_str},{frecuencia_str})"
        return value

    def process_result_value(self, value, dialect):
        """Convierte la cadena de tupla de la DB de vuelta a un diccionario Python."""
        if value is not None:
            # Eliminar paréntesis y dividir por comas para obtener los componentes
            # Esto puede ser un poco más complejo debido a los arrays dentro de la tupla.
            # Una solución simple es usar un regex o parser más robusto si la estructura es muy anidada.
            # Para este caso simple, podemos asumir un formato predecible.

            # Ejemplo: "({1,2,3},10:00:00,11:00:00,60,diario)"
            # Necesitamos un parsing más inteligente para manejar el array y los strings con comas.
            
            # Para simplificar, vamos a dividir por la primera y última coma que no estén dentro de {}
            # O mejor, usar un enfoque que reconozca los campos directamente
            
            # Una forma más robusta es usar el módulo `re` para analizar la cadena
            import re
            match = re.match(r"^\({(.*?)},(.+?),(.+?),(.+?),(.+?)\)$", value)
            if match:
                dias_semana_raw = match.group(1).strip()
                hora_inicio_raw = match.group(2).strip().strip("'")
                hora_fin_raw = match.group(3).strip().strip("'")
                duracion_minutos_raw = match.group(4).strip()
                frecuencia_raw = match.group(5).strip().strip("'")

                dias_semana = [int(d) for d in dias_semana_raw.split(',') if d] if dias_semana_raw else []
                
                return {
                    "dias_semana": dias_semana,
                    "hora_inicio": hora_inicio_raw,
                    "hora_fin": hora_fin_raw,
                    "duracion_minutos": int(duracion_minutos_raw),
                    "frecuencia": frecuencia_raw
                }
        return value
# --- FIN NUEVO ---

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