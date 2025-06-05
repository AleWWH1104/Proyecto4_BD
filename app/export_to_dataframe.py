# app/export_to_dataframe.py
import pandas as pd
from typing import List, Dict
from sqlalchemy.orm import Session
from models import Animal, Evento, Habitat, VistaFinancieraMensual, VistaConservacion, VistaControlAnimal
from crud.crud import get_animals, get_eventos, get_habitats
from crud.crudvista import get_vista_financiera_mensual, get_vista_conservacion, get_vista_control_animal

# ==================== FUNCIONES PARA TABLAS PRINCIPALES ====================

def animals_to_dataframe(db: Session, animals: List[Animal]) -> pd.DataFrame:
    """Convierte animales a DataFrame mostrando solo campos relevantes."""
    data = []
    for animal in animals:
        animal = db.merge(animal)
        data.append({
            'id_animal': animal.id_animal,
            'nombre': animal.nombre,
            'especie': animal.especie.nombre_comun if animal.especie else None,
            'habitat': animal.habitat.nombre if animal.habitat else None,
            'fecha_nacimiento': str(animal.fecha_nacimiento),
            'peso_actual': animal.peso_actual,
            'estado_salud': animal.estado_salud
        })
    
    df = pd.DataFrame(data)
    print("\n=== DataFrame de Animales ===")
    print(df.to_string(index=False))
    return df

def eventos_to_dataframe(db: Session, eventos: List[Evento]) -> pd.DataFrame:
    """Convierte eventos a DataFrame mostrando solo campos relevantes."""
    data = []
    for evento in eventos:
        evento = db.merge(evento)
        data.append({
            'id_evento': evento.id_evento,
            'nombre': evento.nombre,
            'fecha_inicio': str(evento.fecha_inicio),
            'fecha_fin': str(evento.fecha_fin),
            'estado': evento.estado,
            'precio_entrada': evento.precio_entrada
        })
    
    df = pd.DataFrame(data)
    print("\n=== DataFrame de Eventos ===")
    print(df.to_string(index=False))
    return df

def habitats_to_dataframe(db: Session, habitats: List[Habitat]) -> pd.DataFrame:
    """Convierte hábitats a DataFrame mostrando solo campos relevantes."""
    data = []
    for habitat in habitats:
        habitat = db.merge(habitat)
        data.append({
            'id_habitat': habitat.id_habitat,
            'nombre': habitat.nombre,
            'tipo_habitat': habitat.tipo_habitat.nombre if habitat.tipo_habitat else None,
            'estado': habitat.estado,
            'capacidad_maxima': habitat.capacidad_maxima
        })
    
    df = pd.DataFrame(data)
    print("\n=== DataFrame de Hábitats ===")
    print(df.to_string(index=False))
    return df

# ==================== FUNCIONES PARA VISTAS ====================

def vista_financiera_to_dataframe(db: Session, registros: List[VistaFinancieraMensual]) -> pd.DataFrame:
    """Convierte VistaFinancieraMensual a DataFrame."""
    data = []
    for registro in registros:
        registro = db.merge(registro)
        row = {
            'mes': registro.mes,
            'total_ingresos': getattr(registro, 'total_ingresos', 0),
            'total_gastos': getattr(registro, 'total_gastos', 0),
            'balance': getattr(registro, 'balance', 0)
        }
        if hasattr(registro, 'eventos_realizados'):
            row['eventos_realizados'] = registro.eventos_realizados
        if hasattr(registro, 'ingreso_promedio_evento'):
            row['ingreso_promedio_evento'] = registro.ingreso_promedio_evento
        data.append(row)
    
    df = pd.DataFrame(data)
    print("\n=== Vista Financiera Mensual ===")
    print(df.to_string(index=False, float_format="%.2f"))
    return df

def vista_conservacion_to_dataframe(db: Session, registros: List[VistaConservacion]) -> pd.DataFrame:
    """Convierte VistaConservacion a DataFrame."""
    data = []
    for registro in registros:
        registro = db.merge(registro)
        row = {
            'id_especie': registro.id_especie,
            'nombre_cientifico': registro.nombre_cientifico,
            'nombre_comun': registro.nombre_comun,
            'estado_conservacion': registro.estado_conservacion
        }
        if hasattr(registro, 'cantidad_animales'):
            row['cantidad_animales'] = registro.cantidad_animales
        if hasattr(registro, 'habitats_disponibles'):
            row['habitats_disponibles'] = registro.habitats_disponibles
        data.append(row)
    
    df = pd.DataFrame(data)
    print("\n=== Vista de Conservación ===")
    print(df.to_string(index=False))
    return df

def vista_control_animal_to_dataframe(db: Session, registros: List[VistaControlAnimal]) -> pd.DataFrame:
    """Convierte VistaControlAnimal a DataFrame."""
    data = []
    for registro in registros:
        registro = db.merge(registro)
        row = {
            'id_animal': registro.id_animal,
            'nombre_animal': registro.nombre_animal,
            'especie': registro.especie,
            'habitat': registro.habitat,
            'estado_salud': registro.estado_salud
        }
        if hasattr(registro, 'ultimo_chequeo'):
            row['ultimo_chequeo'] = str(registro.ultimo_chequeo) if registro.ultimo_chequeo else None
        if hasattr(registro, 'proximo_chequeo'):
            row['proximo_chequeo'] = str(registro.proximo_chequeo) if registro.proximo_chequeo else None
        data.append(row)
    
    df = pd.DataFrame(data)
    print("\n=== Vista de Control Animal ===")
    print(df.to_string(index=False))
    return df

# ==================== FUNCIONES PRINCIPALES DE EXPORTACIÓN ====================

def export_all_to_dataframes(db: Session) -> Dict[str, pd.DataFrame]:
    """Exporta todos los datos de tablas principales a DataFrames."""
    print("\n" + "="*50)
    print("EXPORTANDO DATOS PRINCIPALES A DATAFRAMES")
    print("="*50)
    
    try:
        dataframes = {
            'animals': animals_to_dataframe(db, get_animals(db)),
            'eventos': eventos_to_dataframe(db, get_eventos(db)),
            'habitats': habitats_to_dataframe(db, get_habitats(db))
        }
        return dataframes
    except Exception as e:
        print(f"\nError durante la exportación de tablas principales: {str(e)}")
        raise

def export_vistas_to_dataframes(db: Session) -> Dict[str, pd.DataFrame]:
    """Exporta todas las vistas a DataFrames."""
    print("\n" + "="*50)
    print("EXPORTANDO VISTAS A DATAFRAMES")
    print("="*50)
    
    try:
        dataframes = {
            'vista_financiera': vista_financiera_to_dataframe(db, get_vista_financiera_mensual(db)),
            'vista_conservacion': vista_conservacion_to_dataframe(db, get_vista_conservacion(db)),
            'vista_control_animal': vista_control_animal_to_dataframe(db, get_vista_control_animal(db))
        }
        return dataframes
    except Exception as e:
        print(f"\nError durante la exportación de vistas: {str(e)}")
        raise

def export_full_database(db: Session) -> Dict[str, Dict[str, pd.DataFrame]]:
    """Exporta toda la base de datos (tablas principales y vistas)"""
    return {
        'tablas_principales': export_all_to_dataframes(db),
        'vistas': export_vistas_to_dataframes(db)
    }