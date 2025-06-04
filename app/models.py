from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Time, Boolean, CheckConstraint, UniqueConstraint, Table, Text
from sqlalchemy.orm import relationship, composite
from sqlalchemy.dialects.postgresql import ENUM, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from database import Base
from sqlalchemy.types import TypeDecorator
import enum

# --------------------------
# Tipos ENUM personalizados
# --------------------------

class EstadoConservacionEnum(enum.Enum):
    extinto = "extinto"
    extinto_naturaleza = "extinto_naturaleza"
    peligro_critico = "peligro_critico"
    peligro = "peligro"
    vulnerable = "vulnerable"
    casi_amenazado = "casi_amenazado"
    preocupacion_menor = "preocupacion_menor"

class EstadoHabitatEnum(enum.Enum):
    activo = "activo"
    mantenimiento = "mantenimiento"
    cerrado = "cerrado"

class SexoAnimalEnum(enum.Enum):
    M = "M"
    F = "F"
    indefinido = "indefinido"

class OrigenAnimalEnum(enum.Enum):
    nacido_zoologico = "nacido_zoologico"
    rescate = "rescate"
    intercambio = "intercambio"
    compra = "compra"

class EstadoSaludEnum(enum.Enum):
    excelente = "excelente"
    bueno = "bueno"
    regular = "regular"
    malo = "malo"
    critico = "critico"

class TipoVisitanteEnum(enum.Enum):
    adulto = "adulto"
    niño = "niño"
    estudiante = "estudiante"
    adulto_mayor = "adulto_mayor"

class TipoProveedorEnum(enum.Enum):
    alimentos = "alimentos"
    medicamentos = "medicamentos"
    equipos = "equipos"
    construccion = "construccion"

class TipoAlimentoEnum(enum.Enum):
    carnivoro = "carnivoro"
    herbivoro = "herbivoro"
    omnivoro = "omnivoro"
    suplemento = "suplemento"

class TipoTratamientoEnum(enum.Enum):
    preventivo = "preventivo"
    curativo = "curativo"
    emergencia = "emergencia"
    rutina = "rutina"

class TipoEventoEnum(enum.Enum):
    educativo = "educativo"
    entretenimiento = "entretenimiento"
    especial = "especial"
    temporal = "temporal"

class EstadoEventoEnum(enum.Enum):
    programado = "programado"
    en_curso = "en_curso"
    finalizado = "finalizado"
    cancelado = "cancelado"

class DiaSemanaEnum(enum.Enum):
    lunes = "lunes"
    martes = "martes"
    miercoles = "miercoles"
    jueves = "jueves"
    viernes = "viernes"
    sabado = "sabado"
    domingo = "domingo"

class MetodoPagoEnum(enum.Enum):
    efectivo = "efectivo"
    tarjeta = "tarjeta"
    transferencia = "transferencia"

class TipoEmpleadoEnum(enum.Enum):
    administrativo = "administrativo"
    operativo = "operativo"
    especialista = "especialista"

class TipoMantenimientoEnum(enum.Enum):
    limpieza = "limpieza"
    reparacion = "reparacion"
    mejora = "mejora"
    inspeccion = "inspeccion"

class CategoriaProductoEnum(enum.Enum):
    souvenir = "souvenir"
    alimentacion = "alimentacion"
    juguetes = "juguetes"
    ropa = "ropa"
    educativo = "educativo"

# --------------------------
# Tipos compuestos personalizados
# --------------------------

class Coordenadas:
    def __init__(self, latitud, longitud, altitud):
        self.latitud = latitud
        self.longitud = longitud
        self.altitud = altitud

    def __composite_values__(self):
        return (self.latitud, self.longitud, self.altitud)

class InfoNutricional:
    def __init__(self, calorias_por_100g, proteinas, grasas, carbohidratos, fibra, vitaminas):
        self.calorias_por_100g = calorias_por_100g
        self.proteinas = proteinas
        self.grasas = grasas
        self.carbohidratos = carbohidratos
        self.fibra = fibra
        self.vitaminas = vitaminas

    def __composite_values__(self):
        return (
            self.calorias_por_100g,
            self.proteinas,
            self.grasas,
            self.carbohidratos,
            self.fibra,
            self.vitaminas
        )

class SignosVitales:
    def __init__(self, temperatura, frecuencia_cardiaca, frecuencia_respiratoria, presion_arterial, peso):
        self.temperatura = temperatura
        self.frecuencia_cardiaca = frecuencia_cardiaca
        self.frecuencia_respiratoria = frecuencia_respiratoria
        self.presion_arterial = presion_arterial
        self.peso = peso

    def __composite_values__(self):
        return (
            self.temperatura,
            self.frecuencia_cardiaca,
            self.frecuencia_respiratoria,
            self.presion_arterial,
            self.peso
        )

class HorarioEvento:
    def __init__(self, dias_semana, hora_inicio, hora_fin, duracion_minutos, frecuencia):
        self.dias_semana = dias_semana
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.duracion_minutos = duracion_minutos
        self.frecuencia = frecuencia

    def __composite_values__(self):
        return (
            self.dias_semana,
            self.hora_inicio,
            self.hora_fin,
            self.duracion_minutos,
            self.frecuencia
        )

# --------------------------
# Modelos de tablas
# --------------------------

class Especie(Base):
    __tablename__ = 'especies'
    
    id_especie = Column(Integer, primary_key=True)
    nombre_cientifico = Column(String, unique=True, nullable=False)
    nombre_comun = Column(String)
    reino = Column(String)
    filo = Column(String)
    clase = Column(String)
    orden = Column(String)
    familia = Column(String)
    genero = Column(String)
    estado_conservacion = Column(ENUM(EstadoConservacionEnum))
    esperanza_vida = Column(Integer)
    peso_promedio = Column(Float)
    
    animales = relationship("Animal", back_populates="especie")

class TipoHabitat(Base):
    __tablename__ = 'tipos_habitat'
    
    id_tipo_habitat = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)
    descripcion = Column(Text)
    temperatura_min = Column(Float)
    temperatura_max = Column(Float)
    humedad_min = Column(Float)
    humedad_max = Column(Float)
    
    habitats = relationship("Habitat", back_populates="tipo_habitat")

class Habitat(Base):
    __tablename__ = 'habitats'
    
    id_habitat = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    id_tipo_habitat = Column(Integer, ForeignKey('tipos_habitat.id_tipo_habitat'), nullable=False)
    
    ubicacion_lat = Column(Float)
    ubicacion_lon = Column(Float)
    ubicacion_alt = Column(Integer)
    ubicacion = composite(Coordenadas, ubicacion_lat, ubicacion_lon, ubicacion_alt)
    
    capacidad_maxima = Column(Integer, nullable=False)
    area_metros_cuadrados = Column(Float, nullable=False)
    fecha_construccion = Column(Date)
    estado = Column(ENUM(EstadoHabitatEnum), nullable=False)
    costo_mantenimiento_mensual = Column(Float, nullable=False)
    
    tipo_habitat = relationship("TipoHabitat", back_populates="habitats")
    animales = relationship("Animal", back_populates="habitat")
    mantenimientos = relationship("HabitatMantenimiento", back_populates="habitat")
    
    __table_args__ = (
        CheckConstraint('capacidad_maxima > 0', name='chk_capacidad_maxima'),
        CheckConstraint('area_metros_cuadrados > 0', name='chk_area_metros'),
        CheckConstraint('costo_mantenimiento_mensual >= 0', name='chk_costo_mantenimiento'),
    )

class Departamento(Base):
    __tablename__ = 'departamentos'
    
    id_departamento = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)
    presupuesto_anual = Column(Float, nullable=False)
    descripcion = Column(Text)
    jefe_departamento_id = Column(Integer, ForeignKey('empleados.id_empleado'))
    
    empleados = relationship("Empleado", back_populates="departamento")
    jefe = relationship("Empleado", foreign_keys=[jefe_departamento_id])
    
    __table_args__ = (
        CheckConstraint('presupuesto_anual >= 0', name='chk_presupuesto'),
    )

class Empleado(Base):
    __tablename__ = 'empleados'
    
    id_empleado = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    email = Column(String, unique=True)
    telefono = Column(String)
    id_departamento = Column(Integer, ForeignKey('departamentos.id_departamento'))
    cargo = Column(String)
    fecha_contratacion = Column(Date)
    salario = Column(Float, nullable=False)
    tipo_empleado = Column(ENUM(TipoEmpleadoEnum), nullable=False)
    activo = Column(Boolean, nullable=False, default=True)
    
    departamento = relationship("Departamento", back_populates="empleados", foreign_keys=[id_departamento])
    cuidador = relationship("Cuidador", back_populates="empleado", uselist=False)
    veterinario = relationship("Veterinario", back_populates="empleado", uselist=False)
    mantenimientos = relationship("HabitatMantenimiento", back_populates="empleado")
    horarios = relationship("Horario", back_populates="empleado")
    
    __table_args__ = (
        CheckConstraint('salario >= 0', name='chk_salario'),
    )

class Cuidador(Base):
    __tablename__ = 'cuidadores'
    
    id_cuidador = Column(Integer, ForeignKey('empleados.id_empleado'), primary_key=True)
    especialidad = Column(Text)
    años_experiencia = Column(Integer)
    certificaciones = Column(Text)
    nivel_autoridad = Column(Integer, nullable=False)
    
    empleado = relationship("Empleado", back_populates="cuidador")
    animales = relationship("AnimalCuidador", back_populates="cuidador")
    alimentaciones = relationship("AnimalAlimentacion", back_populates="cuidador")
    
    __table_args__ = (
        CheckConstraint('años_experiencia >= 0', name='chk_experiencia_cuidador'),
        CheckConstraint('nivel_autoridad BETWEEN 1 AND 5', name='chk_nivel_autoridad'),
    )

class Veterinario(Base):
    __tablename__ = 'veterinarios'
    
    id_veterinario = Column(Integer, ForeignKey('empleados.id_empleado'), primary_key=True)
    numero_colegiado = Column(String, unique=True, nullable=False)
    especialidad_veterinaria = Column(Text)
    universidad_titulo = Column(Text)
    años_experiencia = Column(Integer)
    
    empleado = relationship("Empleado", back_populates="veterinario")
    
    __table_args__ = (
        CheckConstraint('años_experiencia >= 0', name='chk_experiencia_veterinario'),
    )

class Animal(Base):
    __tablename__ = 'animales'
    
    id_animal = Column(Integer, primary_key=True)
    nombre = Column(String)
    id_especie = Column(Integer, ForeignKey('especies.id_especie'), nullable=False)
    id_habitat = Column(Integer, ForeignKey('habitats.id_habitat'), nullable=False)
    fecha_nacimiento = Column(Date)
    sexo = Column(ENUM(SexoAnimalEnum), nullable=False)
    peso_actual = Column(Float, nullable=False)
    altura = Column(Float)
    numero_identificacion = Column(String, unique=True, nullable=False)
    origen = Column(ENUM(OrigenAnimalEnum), nullable=False)
    estado_salud = Column(ENUM(EstadoSaludEnum), nullable=False)
    
    especie = relationship("Especie", back_populates="animales")
    habitat = relationship("Habitat", back_populates="animales")
    cuidadores = relationship("AnimalCuidador", back_populates="animal")
    alimentaciones = relationship("AnimalAlimentacion", back_populates="animal")
    
    __table_args__ = (
        CheckConstraint('peso_actual > 0', name='chk_peso_animal'),
    )

class Visitante(Base):
    __tablename__ = 'visitantes'
    
    id_visitante = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    email = Column(String, unique=True)
    telefono = Column(String)
    fecha_nacimiento = Column(Date)
    nacionalidad = Column(String)
    tipo_visitante = Column(ENUM(TipoVisitanteEnum), nullable=False)
    
    eventos = relationship("VisitanteEvento", back_populates="visitante")
    ventas = relationship("VentaProducto", back_populates="visitante")

class Proveedor(Base):
    __tablename__ = 'proveedores'
    
    id_proveedor = Column(Integer, primary_key=True)
    nombre_empresa = Column(String, nullable=False)
    contacto_principal = Column(String)
    email = Column(String, unique=True)
    telefono = Column(String)
    direccion = Column(Text)
    tipo_proveedor = Column(ENUM(TipoProveedorEnum), nullable=False)
    calificacion = Column(Integer, nullable=False)
    activo = Column(Boolean, nullable=False, default=True)
    
    alimentos = relationship("Alimento", back_populates="proveedor")
    productos = relationship("Producto", back_populates="proveedor")
    
    __table_args__ = (
        CheckConstraint('calificacion BETWEEN 1 AND 5', name='chk_calificacion_proveedor'),
    )

class Alimento(Base):
    __tablename__ = 'alimentos'
    
    id_alimento = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    id_proveedor = Column(Integer, ForeignKey('proveedores.id_proveedor'), nullable=False)
    tipo_alimento = Column(ENUM(TipoAlimentoEnum), nullable=False)
    
    # Campos para el tipo compuesto info_nutricional
    calorias_por_100g = Column(Integer)
    proteinas = Column(Float)
    grasas = Column(Float)
    carbohidratos = Column(Float)
    fibra = Column(Float)
    vitaminas = Column(ARRAY(Text))
    info_nutricional = composite(
        InfoNutricional,
        calorias_por_100g,
        proteinas,
        grasas,
        carbohidratos,
        fibra,
        vitaminas
    )
    
    calorias_por_kg = Column(Integer)
    proteinas_porcentaje = Column(Float)
    grasas_porcentaje = Column(Float)
    carbohidratos_porcentaje = Column(Float)
    costo_por_kg = Column(Float, nullable=False)
    fecha_vencimiento = Column(Date)
    stock_actual = Column(Integer, nullable=False)
    stock_minimo = Column(Integer, nullable=False)
    
    proveedor = relationship("Proveedor", back_populates="alimentos")
    alimentaciones = relationship("AnimalAlimentacion", back_populates="alimento")
    
    __table_args__ = (
        CheckConstraint('costo_por_kg >= 0', name='chk_costo_alimento'),
        CheckConstraint('stock_actual >= 0', name='chk_stock_actual'),
        CheckConstraint('stock_minimo >= 0', name='chk_stock_minimo'),
    )

class TratamientoMedico(Base):
    __tablename__ = 'tratamientos_medicos'
    
    id_tratamiento = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(Text)
    costo_base = Column(Float, nullable=False)
    duracion_estimada_dias = Column(Integer, nullable=False)
    tipo_tratamiento = Column(ENUM(TipoTratamientoEnum), nullable=False)
    requiere_sedacion = Column(Boolean, nullable=False, default=False)
    
    __table_args__ = (
        CheckConstraint('costo_base >= 0', name='chk_costo_tratamiento'),
        CheckConstraint('duracion_estimada_dias >= 0', name='chk_duracion_tratamiento'),
    )

class Evento(Base):
    __tablename__ = 'eventos'
    
    id_evento = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(Text)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)
    horario_inicio = Column(Time)
    horario_fin = Column(Time)
    capacidad_maxima = Column(Integer, nullable=False)
    precio_entrada = Column(Float, nullable=False)
    tipo_evento = Column(ENUM(TipoEventoEnum), nullable=False)
    estado = Column(ENUM(EstadoEventoEnum), nullable=False)
    
    # Campos para el tipo compuesto horario_evento
    dias_semana = Column(ARRAY(Integer))
    hora_inicio_complejo = Column(Time)
    hora_fin_complejo = Column(Time)
    duracion_minutos = Column(Integer)
    frecuencia = Column(String(20))
    horario_complejo = composite(
        HorarioEvento,
        dias_semana,
        hora_inicio_complejo,
        hora_fin_complejo,
        duracion_minutos,
        frecuencia
    )
    
    visitantes = relationship("VisitanteEvento", back_populates="evento")
    horarios = relationship("Horario", back_populates="evento")
    
    __table_args__ = (
        CheckConstraint('capacidad_maxima > 0', name='chk_capacidad_evento'),
        CheckConstraint('precio_entrada >= 0', name='chk_precio_evento'),
    )

class Producto(Base):
    __tablename__ = 'productos'
    
    id_producto = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(Text)
    precio = Column(Float, nullable=False)
    stock_actual = Column(Integer, nullable=False)
    stock_minimo = Column(Integer, nullable=False)
    categoria = Column(ENUM(CategoriaProductoEnum), nullable=False)
    id_proveedor = Column(Integer, ForeignKey('proveedores.id_proveedor'), nullable=False)
    activo = Column(Boolean, nullable=False, default=True)
    
    proveedor = relationship("Proveedor", back_populates="productos")
    ventas = relationship("VentaProducto", back_populates="producto")
    
    __table_args__ = (
        CheckConstraint('precio >= 0', name='chk_precio_producto'),
        CheckConstraint('stock_actual >= 0', name='chk_stock_actual_producto'),
        CheckConstraint('stock_minimo >= 0', name='chk_stock_minimo_producto'),
    )

class Horario(Base):
    __tablename__ = 'horarios'
    
    id_horario = Column(Integer, primary_key=True)
    dia_semana = Column(ENUM(DiaSemanaEnum), nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    tipo_actividad = Column(Text)
    descripcion = Column(Text)
    id_empleado = Column(Integer, ForeignKey('empleados.id_empleado'))
    id_evento = Column(Integer, ForeignKey('eventos.id_evento'))
    
    empleado = relationship("Empleado", back_populates="horarios")
    evento = relationship("Evento", back_populates="horarios")

# --------------------------
# Tablas de relación (N:M)
# --------------------------

class AnimalCuidador(Base):
    __tablename__ = 'animal_cuidador'
    
    id = Column(Integer, primary_key=True)
    id_animal = Column(Integer, ForeignKey('animales.id_animal'), nullable=False)
    id_cuidador = Column(Integer, ForeignKey('cuidadores.id_cuidador'), nullable=False)
    fecha_asignacion = Column(Date, nullable=False)
    es_cuidador_principal = Column(Boolean, nullable=False, default=False)
    notas = Column(Text)
    
    animal = relationship("Animal", back_populates="cuidadores")
    cuidador = relationship("Cuidador", back_populates="animales")
    
    __table_args__ = (
        UniqueConstraint('id_animal', 'id_cuidador', 'fecha_asignacion', name='uq_animal_cuidador_fecha'),
    )

class AnimalAlimentacion(Base):
    __tablename__ = 'animal_alimentacion'
    
    id = Column(Integer, primary_key=True)
    id_animal = Column(Integer, ForeignKey('animales.id_animal'), nullable=False)
    id_alimento = Column(Integer, ForeignKey('alimentos.id_alimento'), nullable=False)
    id_cuidador = Column(Integer, ForeignKey('cuidadores.id_cuidador'), nullable=False)
    fecha_alimentacion = Column(Date, nullable=False)
    hora_alimentacion = Column(Time)
    cantidad_kg = Column(Float, nullable=False)
    observaciones = Column(Text)
    
    animal = relationship("Animal", back_populates="alimentaciones")
    alimento = relationship("Alimento", back_populates="alimentaciones")
    cuidador = relationship("Cuidador", back_populates="alimentaciones")
    
    __table_args__ = (
        CheckConstraint('cantidad_kg > 0', name='chk_cantidad_alimento'),
    )

class VisitanteEvento(Base):
    __tablename__ = 'visitante_evento'
    
    id = Column(Integer, primary_key=True)
    id_visitante = Column(Integer, ForeignKey('visitantes.id_visitante'), nullable=False)
    id_evento = Column(Integer, ForeignKey('eventos.id_evento'), nullable=False)
    fecha_registro = Column(Time, nullable=False, default='now()')
    precio_pagado = Column(Float, nullable=False)
    asistio = Column(Boolean, nullable=False, default=False)
    calificacion = Column(Integer)
    comentarios = Column(Text)
    
    visitante = relationship("Visitante", back_populates="eventos")
    evento = relationship("Evento", back_populates="visitantes")
    
    __table_args__ = (
        UniqueConstraint('id_visitante', 'id_evento', name='uq_visitante_evento'),
        CheckConstraint('precio_pagado >= 0', name='chk_precio_pagado'),
        CheckConstraint('calificacion BETWEEN 1 AND 5', name='chk_calificacion'),
    )

class HabitatMantenimiento(Base):
    __tablename__ = 'habitat_mantenimiento'
    
    id = Column(Integer, primary_key=True)
    id_habitat = Column(Integer, ForeignKey('habitats.id_habitat'), nullable=False)
    id_empleado = Column(Integer, ForeignKey('empleados.id_empleado'), nullable=False)
    fecha_mantenimiento = Column(Date, nullable=False)
    tipo_mantenimiento = Column(ENUM(TipoMantenimientoEnum), nullable=False)
    descripcion_trabajo = Column(Text)
    costo = Column(Float, nullable=False)
    tiempo_horas = Column(Float, nullable=False)
    completado = Column(Boolean, nullable=False, default=False)
    
    habitat = relationship("Habitat", back_populates="mantenimientos")
    empleado = relationship("Empleado", back_populates="mantenimientos")
    
    __table_args__ = (
        CheckConstraint('costo >= 0', name='chk_costo_mantenimiento'),
        CheckConstraint('tiempo_horas >= 0', name='chk_tiempo_mantenimiento'),
    )

class VentaProducto(Base):
    __tablename__ = 'venta_productos'
    
    id = Column(Integer, primary_key=True)
    id_visitante = Column(Integer, ForeignKey('visitantes.id_visitante'), nullable=False)
    id_producto = Column(Integer, ForeignKey('productos.id_producto'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    fecha_venta = Column(Time, nullable=False, default='now()')
    metodo_pago = Column(ENUM(MetodoPagoEnum), nullable=False)
    descuento_aplicado = Column(Float)
    
    visitante = relationship("Visitante", back_populates="ventas")
    producto = relationship("Producto", back_populates="ventas")
    
    __table_args__ = (
        CheckConstraint('cantidad > 0', name='chk_cantidad_venta'),
        CheckConstraint('precio_unitario >= 0', name='chk_precio_unitario'),
        CheckConstraint('descuento_aplicado >= 0', name='chk_descuento'),
    )