# app/models.py
from sqlalchemy import JSON, Column, DateTime, Integer, String, Date, DECIMAL, Boolean, Time, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from database import Base, CoordenadasType, HorarioEventoType  # Importar CoordenadasType

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
# ... (Especie y TipoHabitat sin cambios) ...

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
    # Ubicación usa el tipo de dato personalizado CoordenadasType
    ubicacion = Column(CoordenadasType) 
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
    # ¡Usa el nuevo tipo de dato personalizado!
    horario_complejo = Column(HorarioEventoType) 

    def __repr__(self):
        return f"<Evento(nombre='{self.nombre}', fecha_inicio='{self.fecha_inicio}')>"
    
    # --- NUEVOS MODELOS PARA VISTAS ---

class VistaFinancieraMensual(Base):
    __tablename__ = 'vista_financiera_mensual'
    # Las vistas no suelen tener una PK explícita para SQLAlchemy
    # Pero puedes usar 'mes' como un identificador único si lo deseas para consulta
    mes = Column(Text, primary_key=True) # Usamos mes como PK para poder filtrar y ordenar
    ingresos_eventos = Column(DECIMAL(10, 2))
    ingresos_ventas = Column(DECIMAL(10, 2))
    costos_mantenimiento = Column(DECIMAL(10, 2))
    gastos_tratamientos = Column(DECIMAL(10, 2))
    costos_alimentos = Column(DECIMAL(10, 2))
    costos_salarios = Column(DECIMAL(10, 2))
    ingresos_totales = Column(DECIMAL(10, 2))
    gastos_totales = Column(DECIMAL(10, 2))
    balance_mensual = Column(DECIMAL(10, 2))

    def __repr__(self):
        return (f"<VistaFinancieraMensual(mes='{self.mes}', "
                f"ingresos_totales={self.ingresos_totales}, "
                f"gastos_totales={self.gastos_totales}, "
                f"balance_mensual={self.balance_mensual})>")


class VistaConservacion(Base):
    __tablename__ = 'vista_conservacion'
    # id_especie es una buena candidata para PK aquí
    id_especie = Column(Integer, primary_key=True) 
    nombre_cientifico = Column(Text)
    nombre_comun = Column(Text)
    estado_conservacion = Column(EstadoConservacionEnum)
    cantidad_en_zoo = Column(Integer)
    esperanza_vida = Column(Integer)
    habitat_principal = Column(Text)
    rango_temperatura = Column(Text) # Almacenado como texto en la vista
    rango_humedad = Column(Text)     # Almacenado como texto en la vista
    cuidadores_asignados = Column(Integer)
    veterinarios_especializados = Column(Integer)

    def __repr__(self):
        return (f"<VistaConservacion(nombre_comun='{self.nombre_comun}', "
                f"estado_conservacion='{self.estado_conservacion}', "
                f"cantidad_en_zoo={self.cantidad_en_zoo})>")


class VistaControlAnimal(Base):
    __tablename__ = 'vista_control_animal'
    # id_animal es una buena candidata para PK aquí
    id_animal = Column(Integer, primary_key=True)
    nombre_animal = Column(Text)
    especie = Column(Text)
    estado_conservacion = Column(EstadoConservacionEnum)
    habitat = Column(Text)
    tipo_habitat = Column(Text)
    estado_salud = Column(EstadoSaludEnum)
    peso_actual = Column(DECIMAL(8, 2))
    fecha_nacimiento = Column(Date)
    edad_aproximada = Column(Integer)
    cuidador_principal = Column(Text)
    total_cuidadores_asignados = Column(Integer)
    ultima_alimentacion_fecha = Column(Date)
    total_alimento_kg = Column(DECIMAL(10, 2)) # Ajusta la precisión si es necesario

    def __repr__(self):
        return (f"<VistaControlAnimal(nombre_animal='{self.nombre_animal}', "
                f"especie='{self.especie}', estado_salud='{self.estado_salud}')>")
    
    # Nuevos tipos ENUM
TipoVisitanteEnum = ENUM(
    'adulto', 'niño', 'estudiante', 'adulto_mayor',
    name='tipo_visitante_enum', create_type=False
)
TipoProveedorEnum = ENUM(
    'alimentos', 'medicamentos', 'equipos', 'construccion',
    name='tipo_proveedor_enum', create_type=False
)
TipoAlimentoEnum = ENUM(
    'carnivoro', 'herbivoro', 'omnivoro', 'suplemento',
    name='tipo_alimento_enum', create_type=False
)
MetodoPagoEnum = ENUM(
    'efectivo', 'tarjeta', 'transferencia',
    name='metodo_pago_enum', create_type=False
)

# Modelo para visitantes
class Visitante(Base):
    __tablename__ = 'visitantes'
    id_visitante = Column(Integer, primary_key=True)
    nombre = Column(Text, nullable=False)
    apellido = Column(Text, nullable=False)
    email = Column(Text, unique=True)
    telefono = Column(Text)
    fecha_nacimiento = Column(Date)
    nacionalidad = Column(Text)
    tipo_visitante = Column(TipoVisitanteEnum, nullable=False)
    
    eventos = relationship("VisitanteEvento", back_populates="visitante")

# Modelo para relación visitante-evento
class VisitanteEvento(Base):
    __tablename__ = 'visitante_evento'
    id = Column(Integer, primary_key=True)
    id_visitante = Column(Integer, ForeignKey('visitantes.id_visitante'), nullable=False)
    id_evento = Column(Integer, ForeignKey('eventos.id_evento'), nullable=False)
    fecha_registro = Column(DateTime, nullable=False, default=func.now())
    precio_pagado = Column(DECIMAL(8,2), nullable=False)
    asistio = Column(Boolean, nullable=False, default=False)
    
    visitante = relationship("Visitante", back_populates="eventos")
    evento = relationship("Evento", back_populates="asistentes")

# Actualizar modelo Evento para relación
Evento.asistentes = relationship("VisitanteEvento", back_populates="evento")

# Modelo para alimentación animal
class AnimalAlimentacion(Base):
    __tablename__ = 'animal_alimentacion'
    id = Column(Integer, primary_key=True)
    id_animal = Column(Integer, ForeignKey('animales.id_animal'), nullable=False)
    fecha_alimentacion = Column(Date, nullable=False)
    cantidad_kg = Column(DECIMAL(8,2), nullable=False)
    
    animal = relationship("Animal", back_populates="alimentaciones")

# Actualizar modelo Animal para relación
Animal.alimentaciones = relationship("AnimalAlimentacion", back_populates="animal")