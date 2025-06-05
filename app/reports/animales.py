# app/reports/animales.py

import pandas as pd
from sqlalchemy.orm import Session
from models import Animal, Especie, Habitat, TipoHabitat
from datetime import datetime
from sqlalchemy import and_

def calcular_edad(fecha_nacimiento):
    if not fecha_nacimiento:
        return None
    return datetime.today().year - fecha_nacimiento.year

def generar_reporte_animales(
    db: Session,
    estado_salud: list = None,
    especies: list = None,
    peso_min: float = None,
    peso_max: float = None,
    edad_min: int = None,
    edad_max: int = None,
    tipo_habitat: list = None,
    sexo: list = None,
    export_csv: str = "reporte_animales_cuidados.csv"
):
    query = db.query(Animal).join(Especie).join(Habitat).join(TipoHabitat)

    if estado_salud:
        query = query.filter(Animal.estado_salud.in_(estado_salud))
    
    if especies:
        query = query.filter(Especie.nombre_comun.in_(especies))

    if peso_min is not None:
        query = query.filter(Animal.peso_actual >= peso_min)
    
    if peso_max is not None:
        query = query.filter(Animal.peso_actual <= peso_max)

    if sexo:
        query = query.filter(Animal.sexo.in_(sexo))
    
    animales = query.all()

    # Convertir a DataFrame
    data = []
    for a in animales:
        edad = calcular_edad(a.fecha_nacimiento)
        if edad_min is not None and (edad is None or edad < edad_min):
            continue
        if edad_max is not None and (edad is None or edad > edad_max):
            continue

        data.append({
            "ID": a.id_animal,
            "Nombre": a.nombre,
            "Especie": a.especie.nombre_comun,
            "Hábitat": a.habitat.nombre,
            "Tipo de Hábitat": a.habitat.tipo_habitat.nombre if a.habitat.tipo_habitat else None,
            "Sexo": a.sexo,
            "Peso (kg)": a.peso_actual,
            "Edad (años)": edad,
            "Estado de Salud": a.estado_salud
        })

    df = pd.DataFrame(data)

    # Exportar a CSV
    df.to_csv(export_csv, index=False)
    print(f"\n✅ Reporte de animales exportado a {export_csv}")
    print(df.head(10).to_string(index=False))  # Vista previa

    return df
