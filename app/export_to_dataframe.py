# app/export_to_dataframe.py
import pandas as pd
from typing import List
from sqlalchemy.orm import Session
from models import Animal, Evento, Habitat
from crud.crud import get_animals, get_eventos, get_habitats

def animals_to_dataframe(db: Session, animals: List[Animal]) -> pd.DataFrame:
    """Convierte animales a DataFrame mostrando solo campos relevantes."""
    data = []
    for animal in animals:
        # Asegurarnos de cargar las relaciones necesarias
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

def export_all_to_dataframes(db: Session) -> dict:
    """Exporta todos los datos a DataFrames."""
    print("\n" + "="*50)
    print("EXPORTANDO DATOS A DATAFRAMES (SOLO CONSOLA)")
    print("="*50)
    
    try:
        dataframes = {
            'animals': animals_to_dataframe(db, get_animals(db)),
            'eventos': eventos_to_dataframe(db, get_eventos(db)),
            'habitats': habitats_to_dataframe(db, get_habitats(db))
        }
        return dataframes
    except Exception as e:
        print(f"\nError durante la exportación: {str(e)}")
        raise