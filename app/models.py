# app/models.py
from sqlalchemy import Column, Integer, String, Date, DECIMAL, Boolean, Time, ForeignKey, Text
from sqlalchemy.dialects.postgresql import ENUM, JSONB
from sqlalchemy.orm import relationship
from database import Base

# Definición de ENUMS (deben coincidir con los de tu esquema SQL)
EstadoConservacionEnum = ENUM(
    'extinto', 'extinto_naturaleza', 'peligro_critico', 'peligro',
    'vulnerable', 'casi_amenazado', 'preocupacion_menor',
    name='estado_conservacion_enum', create_type=False
)
EstadoHabitatEnum = ENUM(
    'activo', 'mantenimiento', 'cerrado',
    name='estado_habitat_enum', create_type=False
)
SexoAnimalEnum = ENUM(
    'M', 'F', 'indefinido',
    name='sexo_animal_enum', create_type=False
)
OrigenAnimalEnum = ENUM(
    'nacido_zoologico', 'rescate', 'intercambio', 'compra',
    name='origen_animal_enum', create_type=False
)
EstadoSaludEnum = ENUM(
    'excelente', 'bueno', 'regular', 'malo', 'critico',
    name='estado_salud_enum', create_type=False
)
TipoEventoEnum = ENUM(
    'educativo', 'entretenimiento', 'especial', 'temporal',
    name='tipo_evento_enum', create_type=False
)
EstadoEventoEnum = ENUM(
    'programado', 'en_curso', 'finalizado', 'cancelado',
    name='estado_evento_enum', create_type=False
)

# Modelos
class Especie(Base):
    __tablename__ = 'especies'
    id_especie = Column(Integer, primary_key=True)
    nombre_cientifico = Column(Text, nullable=False, unique=True)
    nombre_comun = Column(Text)
    reino = Column(Text)
    filo = Column(Text)
    clase = Column(Text)
    orden = Column(Text)
    familia = Column(Text)
    genero = Column(Text)
    estado_conservacion = Column(EstadoConservacionEnum)
    esperanza_vida = Column(Integer)
    peso_promedio = Column(DECIMAL(5, 2))

    animales = relationship("Animal", back_populates="especie")

    def __repr__(self):
        return f"<Especie(nombre_cientifico='{self.nombre_cientifico}')>"


class TipoHabitat(Base):
    __tablename__ = 'tipos_habitat'
    id_tipo_habitat = Column(Integer, primary_key=True)
    nombre = Column(Text, nullable=False, unique=True)
    descripcion = Column(Text)
    temperatura_min = Column(DECIMAL(5, 2))
    temperatura_max = Column(DECIMAL(5, 2))
    humedad_min = Column(DECIMAL(5, 2))
    humedad_max = Column(DECIMAL(5, 2))

    habitats = relationship("Habitat", back_populates="tipo_habitat")

    def __repr__(self):
        return f"<TipoHabitat(nombre='{self.nombre}')>"


class Habitat(Base):
    __tablename__ = 'habitats'
    id_habitat = Column(Integer, primary_key=True)
    nombre = Column(Text, nullable=False)
    id_tipo_habitat = Column(Integer, ForeignKey('tipos_habitat.id_tipo_habitat'), nullable=False)
    # ubicacion se trata como JSONB para los tipos compuestos
    ubicacion = Column(JSONB)
    capacidad_maxima = Column(Integer, nullable=False)
    area_metros_cuadrados = Column(DECIMAL(8, 2), nullable=False)
    fecha_construccion = Column(Date)
    estado = Column(EstadoHabitatEnum, nullable=False)
    costo_mantenimiento_mensual = Column(DECIMAL(10, 2), nullable=False)

    tipo_habitat = relationship("TipoHabitat", back_populates="habitats")
    animales = relationship("Animal", back_populates="habitat")

    def __repr__(self):
        return f"<Habitat(nombre='{self.nombre}', estado='{self.estado}')>"


class Animal(Base):
    __tablename__ = 'animales'
    id_animal = Column(Integer, primary_key=True)
    nombre = Column(Text)
    id_especie = Column(Integer, ForeignKey('especies.id_especie'), nullable=False)
    id_habitat = Column(Integer, ForeignKey('habitats.id_habitat'), nullable=False)
    fecha_nacimiento = Column(Date)
    sexo = Column(SexoAnimalEnum, nullable=False)
    peso_actual = Column(DECIMAL(8, 2), nullable=False)
    altura = Column(DECIMAL(5, 2))
    numero_identificacion = Column(Text, unique=True, nullable=False)
    origen = Column(OrigenAnimalEnum, nullable=False)
    estado_salud = Column(EstadoSaludEnum, nullable=False)

    especie = relationship("Especie", back_populates="animales")
    habitat = relationship("Habitat", back_populates="animales")

    def __repr__(self):
        return f"<Animal(nombre='{self.nombre}', especie='{self.especie.nombre_comun if self.especie else 'N/A'}')>"


class Evento(Base):
    __tablename__ = 'eventos'
    id_evento = Column(Integer, primary_key=True)
    nombre = Column(Text, nullable=False)
    descripcion = Column(Text)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)
    horario_inicio = Column(Time)
    horario_fin = Column(Time)
    capacidad_maxima = Column(Integer, nullable=False)
    precio_entrada = Column(DECIMAL(8, 2), nullable=False)
    tipo_evento = Column(TipoEventoEnum, nullable=False)
    estado = Column(EstadoEventoEnum, nullable=False)
    # horario_complejo se trata como JSONB para los tipos compuestos
    horario_complejo = Column(JSONB)

    def __repr__(self):
        return f"<Evento(nombre='{self.nombre}', fecha_inicio='{self.fecha_inicio}')>"