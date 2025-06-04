# app/crud/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import func
# Importar los nuevos modelos de vista
from models import VistaFinancieraMensual, VistaConservacion, VistaControlAnimal
from typing import List, Dict, Any, Optional # Importar Optional

### Funciones de Lectura (READ) para Vistas

def get_vista_financiera_mensual(db: Session, mes: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[VistaFinancieraMensual]:
    """
    Obtiene registros de la vista financiera mensual.
    Puede filtrar por un mes específico (ej. '2024-05').
    """
    query = db.query(VistaFinancieraMensual)
    if mes:
        query = query.filter(VistaFinancieraMensual.mes == mes)
    return query.offset(skip).limit(limit).all()

def get_vista_conservacion(db: Session, estado_conservacion: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[VistaConservacion]:
    """
    Obtiene registros de la vista de conservación.
    Puede filtrar por estado de conservación (ej. 'peligro_critico').
    """
    query = db.query(VistaConservacion)
    if estado_conservacion:
        query = query.filter(VistaConservacion.estado_conservacion == estado_conservacion)
    query = query.order_by(VistaConservacion.id_especie) # O el criterio de ordenamiento que desees
    return query.offset(skip).limit(limit).all()

def get_vista_control_animal(db: Session, animal_id: Optional[int] = None, estado_salud: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[VistaControlAnimal]:
    """
    Obtiene registros de la vista de control animal.
    Puede filtrar por ID de animal o estado de salud.
    """
    query = db.query(VistaControlAnimal)
    if animal_id:
        query = query.filter(VistaControlAnimal.id_animal == animal_id)
    if estado_salud:
        query = query.filter(VistaControlAnimal.estado_salud == estado_salud)
    query = query.order_by(VistaControlAnimal.nombre_animal) # O el criterio de ordenamiento que desees
    return query.offset(skip).limit(limit).all()