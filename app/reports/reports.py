# app/reports/reports.py
import pandas as pd
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_
from datetime import date, time
from typing import Optional, List

from models import (
    Animal, Especie, EstadoHabitatEnum, Habitat, TipoHabitat, Evento, Visitante, VisitanteEvento,
    AnimalAlimentacion, Proveedor, Alimento,
    EstadoConservacionEnum, SexoAnimalEnum, OrigenAnimalEnum, EstadoSaludEnum,
    TipoEventoEnum, EstadoEventoEnum, TipoVisitanteEnum, TipoAlimentoEnum, TipoProveedorEnum,
    CoordenadasType, HorarioEventoType, InfoNutricionalType # Asegúrate de importar tus tipos personalizados si los usas para deserialización
)
from utils import export_dataframe_to_csv # Importar la función de exportación
from database import engine # Importar el engine para consultas directas si es necesario


def get_reporte_animales_por_habitat(
    db: Session,
    nombre_habitat: Optional[str] = None,
    tipo_habitat: Optional[str] = None, # Filtro 1: Tipo de hábitat
    estado_habitat: Optional[str] = None, # Filtro 2: Estado del hábitat
    especie_nombre_comun: Optional[str] = None, # Filtro 3: Nombre común de la especie
    sexo_animal: Optional[str] = None, # Filtro 4: Sexo del animal
    estado_salud_animal: Optional[str] = None, # Filtro 5: Estado de salud del animal
    min_peso: Optional[float] = None,
    max_peso: Optional[float] = None,
    export_csv: bool = False,
    filename: str = "reporte_animales_habitat.csv"
) -> pd.DataFrame:
    """
    Reporte: Lista de animales, filtrados por hábitat y características del animal.
    Incluye 5 filtros significativos: tipo_habitat, estado_habitat, especie_nombre_comun,
    sexo_animal, estado_salud_animal.
    """
    query = db.query(
        Animal.nombre.label('nombre_animal'),
        Animal.numero_identificacion,
        Animal.sexo,
        Animal.peso_actual,
        Animal.estado_salud,
        Especie.nombre_comun.label('especie_comun'),
        Especie.nombre_cientifico,
        Especie.estado_conservacion,
        Habitat.nombre.label('nombre_habitat'),
        Habitat.estado.label('estado_habitat'),
        TipoHabitat.nombre.label('tipo_habitat_nombre')
    ).join(Especie, Animal.id_especie == Especie.id_especie)\
    .join(Habitat, Animal.id_habitat == Habitat.id_habitat)\
    .join(TipoHabitat, Habitat.id_tipo_habitat == TipoHabitat.id_tipo_habitat)

    filters = []
    if nombre_habitat:
        filters.append(Habitat.nombre.ilike(f'%{nombre_habitat}%'))
    if tipo_habitat:
        try:
            filters.append(TipoHabitat.nombre.ilike(f'%{tipo_habitat}%'))
        except ValueError:
            print(f"Advertencia: '{tipo_habitat}' no es un tipo de hábitat válido.")
    if estado_habitat:
        try:
            filters.append(Habitat.estado == estado_habitat)
        except ValueError:
            print(f"Advertencia: '{estado_habitat}' no es un estado de hábitat válido.")
    if especie_nombre_comun:
        filters.append(Especie.nombre_comun.ilike(f'%{especie_nombre_comun}%'))
    if sexo_animal:
        try:
            filters.append(Animal.sexo == sexo_animal)
        except ValueError:
            print(f"Advertencia: '{sexo_animal}' no es un sexo de animal válido.")
    if estado_salud_animal:
        try:
            filters.append(Animal.estado_salud == estado_salud_animal)
        except ValueError:
            print(f"Advertencia: '{estado_salud_animal}' no es un estado de salud válido.")
    if min_peso is not None:
        filters.append(Animal.peso_actual >= min_peso)
    if max_peso is not None:
        filters.append(Animal.peso_actual <= max_peso)

    if filters:
        query = query.filter(and_(*filters))

    results = query.all()
    df = pd.DataFrame([row._asdict() for row in results])

    if export_csv:
        export_dataframe_to_csv(df, filename)
    
    return df

def get_reporte_eventos_y_asistencia(
    db: Session,
    fecha_inicio_desde: Optional[date] = None,
    fecha_inicio_hasta: Optional[date] = None,
    tipo_evento: Optional[str] = None, # Filtro 1: Tipo de evento
    estado_evento: Optional[str] = None, # Filtro 2: Estado del evento
    min_precio_entrada: Optional[float] = None,
    max_precio_entrada: Optional[float] = None,
    tipo_visitante: Optional[str] = None, # Filtro 3: Tipo de visitante
    nacionalidad_visitante: Optional[str] = None, # Filtro 4: Nacionalidad del visitante
    evento_con_asistencia: Optional[bool] = None, # Filtro 5: Eventos con o sin asistencia registrada
    export_csv: bool = False,
    filename: str = "reporte_eventos_asistencia.csv"
) -> pd.DataFrame:
    """
    Reporte: Eventos y su asistencia, con detalles de visitantes.
    Incluye 5 filtros significativos: tipo_evento, estado_evento, tipo_visitante,
    nacionalidad_visitante, evento_con_asistencia.
    """
    # Consulta base para eventos
    query = db.query(
        Evento.nombre.label('nombre_evento'),
        Evento.fecha_inicio,
        Evento.fecha_fin,
        Evento.horario_inicio,
        Evento.horario_fin,
        Evento.precio_entrada,
        Evento.tipo_evento,
        Evento.estado.label('estado_evento'),
        func.count(VisitanteEvento.id).label('total_asistentes'),
        func.sum(VisitanteEvento.precio_pagado).label('ingresos_totales_evento')
    ).outerjoin(VisitanteEvento, Evento.id_evento == VisitanteEvento.id_evento) \
    .group_by(
        Evento.id_evento,
        Evento.nombre,
        Evento.fecha_inicio,
        Evento.fecha_fin,
        Evento.horario_inicio,
        Evento.horario_fin,
        Evento.precio_entrada,
        Evento.tipo_evento,
        Evento.estado
    )

    filters = []
    if fecha_inicio_desde:
        filters.append(Evento.fecha_inicio >= fecha_inicio_desde)
    if fecha_inicio_hasta:
        filters.append(Evento.fecha_inicio <= fecha_inicio_hasta)
    if tipo_evento:
        try:
            filters.append(Evento.tipo_evento == tipo_evento)
        except ValueError:
            print(f"Advertencia: '{tipo_evento}' no es un tipo de evento válido.")
    if estado_evento:
        try:
            filters.append(Evento.estado == estado_evento)
        except ValueError:
            print(f"Advertencia: '{estado_evento}' no es un estado de evento válido.")
    if min_precio_entrada is not None:
        filters.append(Evento.precio_entrada >= min_precio_entrada)
    if max_precio_entrada is not None:
        filters.append(Evento.precio_entrada <= max_precio_entrada)
    
    # Para filtros relacionados con Visitante, necesitamos un subquery o unir después
    if tipo_visitante or nacionalidad_visitante or evento_con_asistencia is not None:
        # Volvemos a la tabla VisitanteEvento para aplicar filtros específicos de visitante
        query_with_visitors = db.query(
            Evento.nombre.label('nombre_evento'),
            Evento.fecha_inicio,
            Evento.fecha_fin,
            Evento.horario_inicio,
            Evento.horario_fin,
            Evento.precio_entrada,
            Evento.tipo_evento,
            Evento.estado.label('estado_evento'),
            Visitante.nombre.label('nombre_visitante'),
            Visitante.apellido.label('apellido_visitante'),
            Visitante.tipo_visitante,
            Visitante.nacionalidad,
            VisitanteEvento.fecha_registro,
            VisitanteEvento.precio_pagado,
            VisitanteEvento.asistio
        ).outerjoin(VisitanteEvento, Evento.id_evento == VisitanteEvento.id_evento) \
        .outerjoin(Visitante, VisitanteEvento.id_visitante == Visitante.id_visitante)

        visitor_filters = []
        if tipo_visitante:
            try:
                visitor_filters.append(Visitante.tipo_visitante == tipo_visitante)
            except ValueError:
                print(f"Advertencia: '{tipo_visitante}' no es un tipo de visitante válido.")
        if nacionalidad_visitante:
            visitor_filters.append(Visitante.nacionalidad.ilike(f'%{nacionalidad_visitante}%'))
        if evento_con_asistencia is not None:
            if evento_con_asistencia:
                visitor_filters.append(VisitanteEvento.id.isnot(None)) # Solo eventos con alguna asistencia
            else:
                visitor_filters.append(VisitanteEvento.id.is_(None)) # Solo eventos sin asistencia

        if visitor_filters:
            query_with_visitors = query_with_visitors.filter(and_(*visitor_filters))
        
        # Combinar los filtros de evento con los de visitante si se especificaron
        if filters:
            query_with_visitors = query_with_visitors.filter(and_(*filters))
        
        results = query_with_visitors.all()
        df = pd.DataFrame([row._asdict() for row in results])

    else: # Si no hay filtros específicos de visitante, se usa la consulta agrupada original
        if filters:
            query = query.filter(and_(*filters))
        
        results = query.all()
        df = pd.DataFrame([row._asdict() for row in results])

    # Si hay eventos sin asistentes, func.count() puede dar 0, func.sum() puede dar None
    if 'total_asistentes' in df.columns:
        df['total_asistentes'] = df['total_asistentes'].fillna(0).astype(int)
    if 'ingresos_totales_evento' in df.columns:
        df['ingresos_totales_evento'] = df['ingresos_totales_evento'].fillna(0.0)

    if export_csv:
        export_dataframe_to_csv(df, filename)
    
    return df

def get_reporte_alimentos_y_proveedores(
    db: Session,
    nombre_alimento: Optional[str] = None,
    tipo_alimento: Optional[str] = None, # Filtro 1: Tipo de alimento
    nombre_proveedor: Optional[str] = None, # Filtro 2: Nombre de la empresa proveedora
    tipo_proveedor: Optional[str] = None, # Filtro 3: Tipo de proveedor
    calificacion_proveedor_min: Optional[int] = None, # Filtro 4: Calificación mínima del proveedor
    stock_actual_min: Optional[int] = None, # Filtro 5: Stock actual mínimo
    fecha_vencimiento_antes: Optional[date] = None,
    costo_por_kg_max: Optional[float] = None,
    export_csv: bool = False,
    filename: str = "reporte_alimentos_proveedores.csv"
) -> pd.DataFrame:
    """
    Reporte: Información sobre alimentos y sus proveedores.
    Incluye 5 filtros significativos: tipo_alimento, nombre_proveedor, tipo_proveedor,
    calificacion_proveedor_min, stock_actual_min.
    """
    query = db.query(
        Alimento.nombre.label('nombre_alimento'),
        Alimento.tipo_alimento,
        Alimento.calorias_por_kg,
        Alimento.costo_por_kg,
        Alimento.fecha_vencimiento,
        Alimento.stock_actual,
        Alimento.stock_minimo,
        Proveedor.nombre_empresa.label('nombre_proveedor'),
        Proveedor.contacto_principal,
        Proveedor.telefono,
        Proveedor.tipo_proveedor,
        Proveedor.calificacion,
        Proveedor.activo.label('proveedor_activo')
    ).join(Proveedor, Alimento.id_proveedor == Proveedor.id_proveedor)

    filters = []
    if nombre_alimento:
        filters.append(Alimento.nombre.ilike(f'%{nombre_alimento}%'))
    if tipo_alimento:
        try:
            filters.append(Alimento.tipo_alimento == tipo_alimento)
        except ValueError:
            print(f"Advertencia: '{tipo_alimento}' no es un tipo de alimento válido.")
    if nombre_proveedor:
        filters.append(Proveedor.nombre_empresa.ilike(f'%{nombre_proveedor}%'))
    if tipo_proveedor:
        try:
           filters.append(Proveedor.tipo_proveedor == tipo_proveedor)
        except ValueError:
            print(f"Advertencia: '{tipo_proveedor}' no es un tipo de proveedor válido.")
    if calificacion_proveedor_min is not None:
        filters.append(Proveedor.calificacion >= calificacion_proveedor_min)
    if stock_actual_min is not None:
        filters.append(Alimento.stock_actual >= stock_actual_min)
    if fecha_vencimiento_antes:
        filters.append(Alimento.fecha_vencimiento <= fecha_vencimiento_antes)
    if costo_por_kg_max is not None:
        filters.append(Alimento.costo_por_kg <= costo_por_kg_max)

    if filters:
        query = query.filter(and_(*filters))

    results = query.all()
    df = pd.DataFrame([row._asdict() for row in results])

    if export_csv:
        export_dataframe_to_csv(df, filename)
    
    return df