# app/crud/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Animal, Evento, Habitat, Especie, TipoHabitat
from datetime import date, time
from typing import List, Dict, Any

# --- CRUD para Animales ---

def create_animal(db: Session, animal_data: Dict[str, Any]) -> Animal:
    """Crea un nuevo animal en la base de datos."""
    db_animal = Animal(**animal_data)
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal

def get_animal(db: Session, animal_id: int) -> Animal | None:
    """Obtiene un animal por su ID."""
    return db.query(Animal).filter(Animal.id_animal == animal_id).first()

def get_animals(db: Session, skip: int = 0, limit: int = 100) -> List[Animal]:
    """Obtiene una lista de animales."""
    return db.query(Animal).offset(skip).limit(limit).all()

def update_animal(db: Session, animal_id: int, animal_data: Dict[str, Any]) -> Animal | None:
    """Actualiza un animal existente."""
    db_animal = db.query(Animal).filter(Animal.id_animal == animal_id).first()
    if db_animal:
        for key, value in animal_data.items():
            setattr(db_animal, key, value)
        db.commit()
        db.refresh(db_animal)
        return db_animal
    return None

def delete_animal(db: Session, animal_id: int) -> Animal | None:
    """Elimina un animal por su ID."""
    db_animal = db.query(Animal).filter(Animal.id_animal == animal_id).first()
    if db_animal:
        db.delete(db_animal)
        db.commit()
        return db_animal
    return None

# --- CRUD para Eventos ---

def create_evento(db: Session, evento_data: Dict[str, Any]) -> Evento:
    """Crea un nuevo evento en la base de datos."""
    db_evento = Evento(**evento_data)
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)
    return db_evento

def get_evento(db: Session, evento_id: int) -> Evento | None:
    """Obtiene un evento por su ID."""
    return db.query(Evento).filter(Evento.id_evento == evento_id).first()

def get_eventos(db: Session, skip: int = 0, limit: int = 100) -> List[Evento]:
    """Obtiene una lista de eventos."""
    return db.query(Evento).offset(skip).limit(limit).all()

def update_evento(db: Session, evento_id: int, evento_data: Dict[str, Any]) -> Evento | None:
    """Actualiza un evento existente."""
    db_evento = db.query(Evento).filter(Evento.id_evento == evento_id).first()
    if db_evento:
        for key, value in evento_data.items():
            setattr(db_evento, key, value)
        db.commit()
        db.refresh(db_evento)
        return db_evento
    return None

def delete_evento(db: Session, evento_id: int) -> Evento | None:
    """Elimina un evento por su ID."""
    db_evento = db.query(Evento).filter(Evento.id_evento == evento_id).first()
    if db_evento:
        db.delete(db_evento)
        db.commit()
        return db_evento
    return None

# --- CRUD para Habitats ---

def create_habitat(db: Session, habitat_data: Dict[str, Any]) -> Habitat:
    """Crea un nuevo hábitat en la base de datos."""
    db_habitat = Habitat(**habitat_data)
    db.add(db_habitat)
    db.commit()
    db.refresh(db_habitat)
    return db_habitat

def get_habitat(db: Session, habitat_id: int) -> Habitat | None:
    """Obtiene un hábitat por su ID."""
    return db.query(Habitat).filter(Habitat.id_habitat == habitat_id).first()

def get_habitats(db: Session, skip: int = 0, limit: int = 100) -> List[Habitat]:
    """Obtiene una lista de hábitats."""
    return db.query(Habitat).offset(skip).limit(limit).all()

def update_habitat(db: Session, habitat_id: int, habitat_data: Dict[str, Any]) -> Habitat | None:
    """Actualiza un hábitat existente."""
    db_habitat = db.query(Habitat).filter(Habitat.id_habitat == habitat_id).first()
    if db_habitat:
        for key, value in habitat_data.items():
            setattr(db_habitat, key, value)
        db.commit()
        db.refresh(db_habitat)
        return db_habitat
    return None

def delete_habitat(db: Session, habitat_id: int) -> Habitat | None:
    """Elimina un hábitat por su ID."""
    db_habitat = db.query(Habitat).filter(Habitat.id_habitat == habitat_id).first()
    if db_habitat:
        db.delete(db_habitat)
        db.commit()
        return db_habitat
    return None