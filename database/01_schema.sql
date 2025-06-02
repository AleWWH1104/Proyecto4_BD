-- ================================================================
-- 1. DEFINICIÓN DE TIPOS DE DATOS PERSONALIZADOS Y ENUMS
-- ================================================================

-- 1.1. Estado de conservación de especies
CREATE TYPE estado_conservacion_enum AS ENUM (
    'extinto',
    'extinto_naturaleza',
    'peligro_critico',
    'peligro',
    'vulnerable',
    'casi_amenazado',
    'preocupacion_menor'
);

-- 1.2. Coordenadas geográficas para ubicación de hábitats
CREATE TYPE coordenadas AS (
    latitud     DECIMAL(10,8),
    longitud    DECIMAL(11,8),
    altitud     INTEGER
);

-- 1.3. Información nutricional completa (para alimentos)
CREATE TYPE info_nutricional AS (
    calorias_por_100g   INTEGER,
    proteinas           DECIMAL(5,2),
    grasas              DECIMAL(5,2),
    carbohidratos       DECIMAL(5,2),
    fibra               DECIMAL(5,2),
    vitaminas           TEXT[]
);

-- 1.4. Registro de signos vitales (para usos médicos/veterinarios)
CREATE TYPE signos_vitales AS (
    temperatura                 DECIMAL(4,2),
    frecuencia_cardiaca         INTEGER,
    frecuencia_respiratoria     INTEGER,
    presion_arterial            VARCHAR(10),
    peso                        DECIMAL(8,2)
);

-- 1.5. Horario complejo para eventos
CREATE TYPE horario_evento AS (
    dias_semana         INTEGER[],      -- Array de días (1 = lunes, …, 7 = domingo)
    hora_inicio         TIME,
    hora_fin            TIME,
    duracion_minutos    INTEGER,
    frecuencia          VARCHAR(20)      -- 'diario', 'semanal', 'mensual', etc.
);

-- ================================================================
-- 1.6. ENUMS PARA CAMPOS CATEGÓRICOS
-- ================================================================

-- 1.6.1. Estado de un hábitat
CREATE TYPE estado_habitat_enum AS ENUM (
    'activo',
    'mantenimiento',
    'cerrado'
);

-- 1.6.2. Sexo de un animal
CREATE TYPE sexo_animal_enum AS ENUM (
    'M',
    'F',
    'indefinido'
);

-- 1.6.3. Origen de un animal
CREATE TYPE origen_animal_enum AS ENUM (
    'nacido_zoologico',
    'rescate',
    'intercambio',
    'compra'
);

-- 1.6.4. Estado de salud de un animal
CREATE TYPE estado_salud_enum AS ENUM (
    'excelente',
    'bueno',
    'regular',
    'malo',
    'critico'
);

-- 1.6.5. Tipo de visitante
CREATE TYPE tipo_visitante_enum AS ENUM (
    'adulto',
    'niño',
    'estudiante',
    'adulto_mayor'
);

-- 1.6.6. Tipo de proveedor
CREATE TYPE tipo_proveedor_enum AS ENUM (
    'alimentos',
    'medicamentos',
    'equipos',
    'construccion'
);

-- 1.6.7. Tipo de alimento
CREATE TYPE tipo_alimento_enum AS ENUM (
    'carnivoro',
    'herbivoro',
    'omnivoro',
    'suplemento'
);

-- 1.6.8. Tipo de tratamiento médico
CREATE TYPE tipo_tratamiento_enum AS ENUM (
    'preventivo',
    'curativo',
    'emergencia',
    'rutina'
);

-- 1.6.9. Tipo de evento
CREATE TYPE tipo_evento_enum AS ENUM (
    'educativo',
    'entretenimiento',
    'especial',
    'temporal'
);

-- 1.6.10. Estado de un evento
CREATE TYPE estado_evento_enum AS ENUM (
    'programado',
    'en_curso',
    'finalizado',
    'cancelado'
);

-- 1.6.11. Día de la semana (para horarios)
CREATE TYPE dia_semana_enum AS ENUM (
    'lunes',
    'martes',
    'miercoles',
    'jueves',
    'viernes',
    'sabado',
    'domingo'
);

-- 1.6.12. Método de pago en ventas
CREATE TYPE metodo_pago_enum AS ENUM (
    'efectivo',
    'tarjeta',
    'transferencia'
);

-- 1.6.13. Tipo de empleado
CREATE TYPE tipo_empleado_enum AS ENUM (
    'administrativo',
    'operativo',
    'especialista'
);

-- 1.6.14. Tipo de mantenimiento para hábitats
CREATE TYPE tipo_mantenimiento_enum AS ENUM (
    'limpieza',
    'reparacion',
    'mejora',
    'inspeccion'
);

-- 1.6.15. Categoría de producto
CREATE TYPE categoria_producto_enum AS ENUM (
    'souvenir',
    'alimentacion',
    'juguetes',
    'ropa',
    'educativo'
);


-- ================================================================
-- 2. TABLAS PRINCIPALES (REORDENADAS PARA DEPENDENCIAS)
-- ================================================================

-- 2.1. Tabla: especies
CREATE TABLE especies (
    id_especie              SERIAL PRIMARY KEY,
    nombre_cientifico       TEXT NOT NULL UNIQUE,
    nombre_comun            TEXT,
    reino                   TEXT,
    filo                    TEXT,
    clase                   TEXT,
    orden                   TEXT,
    familia                 TEXT,
    genero                  TEXT,
    estado_conservacion     estado_conservacion_enum,
    esperanza_vida          INTEGER,              -- en años
    peso_promedio           DECIMAL(5,2),         -- en kg (promedio)
    created_at              TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP   NOT NULL DEFAULT NOW()
);

-- 2.2. Tabla: tipos_habitat
CREATE TABLE tipos_habitat (
    id_tipo_habitat         SERIAL PRIMARY KEY,
    nombre                  TEXT    NOT NULL UNIQUE,
    descripcion             TEXT,
    temperatura_min         DECIMAL(5,2),         -- en °C
    temperatura_max         DECIMAL(5,2),         -- en °C
    humedad_min             DECIMAL(5,2),         -- en %
    humedad_max             DECIMAL(5,2),         -- en %
    created_at              TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP   NOT NULL DEFAULT NOW()
);

-- 2.3. Tabla: habitats
CREATE TABLE habitats (
    id_habitat              SERIAL PRIMARY KEY,
    nombre                  TEXT    NOT NULL,
    id_tipo_habitat         INTEGER NOT NULL
        REFERENCES tipos_habitat(id_tipo_habitat)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    ubicacion               coordenadas,            -- tipo compuesto
    capacidad_maxima        INTEGER NOT NULL CHECK (capacidad_maxima > 0),
    area_metros_cuadrados   DECIMAL(8,2) NOT NULL CHECK (area_metros_cuadrados > 0),
    fecha_construccion      DATE,
    estado                  estado_habitat_enum    NOT NULL,
    costo_mantenimiento_mensual DECIMAL(10,2) NOT NULL CHECK (costo_mantenimiento_mensual >= 0),
    created_at              TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP   NOT NULL DEFAULT NOW()
);

-- 2.4. Tabla: empleados
CREATE TABLE empleados (
    id_empleado             SERIAL PRIMARY KEY,
    nombre                  TEXT    NOT NULL,
    apellido                TEXT    NOT NULL,
    email                   TEXT    UNIQUE,
    telefono                TEXT,
    id_departamento         INTEGER
        -- Se definirá la FK después de crear departamentos
        -- ON UPDATE CASCADE ON DELETE SET NULL
        ,
    cargo                   TEXT,
    fecha_contratacion      DATE,
    salario                 DECIMAL(12,2) NOT NULL CHECK (salario >= 0),
    tipo_empleado           tipo_empleado_enum    NOT NULL,
    activo                  BOOLEAN NOT NULL DEFAULT TRUE,
    created_at              TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP   NOT NULL DEFAULT NOW()
);

-- 2.5. Tabla: departamentos
CREATE TABLE departamentos (
    id_departamento         SERIAL PRIMARY KEY,
    nombre                  TEXT    NOT NULL UNIQUE,
    presupuesto_anual       DECIMAL(12,2) NOT NULL CHECK (presupuesto_anual >= 0),
    descripcion             TEXT,
    jefe_departamento_id    INTEGER
        REFERENCES empleados(id_empleado)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    created_at              TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP   NOT NULL DEFAULT NOW()
);

-- 2.6. Ahora que existe departamentos, agregamos la FK en empleados
ALTER TABLE empleados
    ADD CONSTRAINT fk_empleados_departamento
    FOREIGN KEY (id_departamento)
    REFERENCES departamentos(id_departamento)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- 2.7. Tabla: cuidadores (hereda de empleados)
CREATE TABLE cuidadores (
    id_cuidador             INTEGER PRIMARY KEY
        REFERENCES empleados(id_empleado)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    especialidad            TEXT,
    años_experiencia        INTEGER CHECK (años_experiencia >= 0),
    certificaciones         TEXT,
    nivel_autoridad         INTEGER NOT NULL CHECK (nivel_autoridad BETWEEN 1 AND 5),
    created_at              TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP   NOT NULL DEFAULT NOW()
);

-- 2.8. Tabla: veterinarios (hereda de empleados)
CREATE TABLE veterinarios (
    id_veterinario          INTEGER PRIMARY KEY
        REFERENCES empleados(id_empleado)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    numero_colegiado        TEXT    NOT NULL UNIQUE,
    especialidad_veterinaria TEXT,
    universidad_titulo      TEXT,
    años_experiencia        INTEGER CHECK (años_experiencia >= 0),
    created_at              TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP   NOT NULL DEFAULT NOW()
);

-- 2.9. Tabla: animales
CREATE TABLE animales (
    id_animal               SERIAL PRIMARY KEY,
    nombre                  TEXT,
    id_especie              INTEGER NOT NULL
        REFERENCES especies(id_especie)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    id_habitat              INTEGER NOT NULL
        REFERENCES habitats(id_habitat)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    fecha_nacimiento        DATE,
    sexo                    sexo_animal_enum    NOT NULL,
    peso_actual             DECIMAL(8,2) NOT NULL CHECK (peso_actual > 0),
    altura                  DECIMAL(5,2),
    numero_identificacion   TEXT    UNIQUE NOT NULL,
    origen                  origen_animal_enum  NOT NULL,
    estado_salud            estado_salud_enum   NOT NULL,
    created_at              TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP   NOT NULL DEFAULT NOW()
);

-- 2.10. Tabla: visitantes
CREATE TABLE visitantes (
    id_visitante            SERIAL PRIMARY KEY,
    nombre                  TEXT    NOT NULL,
    apellido                TEXT    NOT NULL,
    email                   TEXT    UNIQUE,
    telefono                TEXT,
    fecha_nacimiento        DATE,
    nacionalidad            TEXT,
    tipo_visitante          tipo_visitante_enum NOT NULL,
    created_at              TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP   NOT NULL DEFAULT NOW()
);

-- 2.11. Tabla: proveedores
CREATE TABLE proveedores (
    id_proveedor            SERIAL PRIMARY KEY,
    nombre_empresa          TEXT    NOT NULL,
    contacto_principal      TEXT,
    email                   TEXT    UNIQUE,
    telefono                TEXT,
    direccion               TEXT,
    tipo_proveedor          tipo_proveedor_enum NOT NULL,
    calificacion            INTEGER NOT NULL CHECK (calificacion BETWEEN 1 AND 5),
    activo                  BOOLEAN NOT NULL DEFAULT TRUE,
    created_at              TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP   NOT NULL DEFAULT NOW()
);

-- 2.12. Tabla: alimentos
CREATE TABLE alimentos (
    id_alimento             SERIAL PRIMARY KEY,
    nombre                  TEXT    NOT NULL,
    id_proveedor            INTEGER NOT NULL
        REFERENCES proveedores(id_proveedor)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    tipo_alimento           tipo_alimento_enum  NOT NULL,
    info_nutricional        info_nutricional,      -- tipo compuesto
    calorias_por_kg         INTEGER,
    proteinas_porcentaje    DECIMAL(5,2),
    grasas_porcentaje       DECIMAL(5,2),
    carbohidratos_porcentaje DECIMAL(5,2),
    costo_por_kg            DECIMAL(10,2) NOT NULL CHECK (costo_por_kg >= 0),
    fecha_vencimiento       DATE,
    stock_actual            INTEGER NOT NULL CHECK (stock_actual >= 0),
    stock_minimo            INTEGER NOT NULL CHECK (stock_minimo >= 0),
    created_at              TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP   NOT NULL DEFAULT NOW()
);

-- 2.13. Tabla: tratamientos_medicos
CREATE TABLE tratamientos_medicos (
    id_tratamiento          SERIAL PRIMARY KEY,
    nombre                  TEXT    NOT NULL,
    descripcion             TEXT,
    costo_base              DECIMAL(12,2) NOT NULL CHECK (costo_base >= 0),
    duracion_estimada_dias  INTEGER NOT NULL CHECK (duracion_estimada_dias >= 0),
    tipo_tratamiento        tipo_tratamiento_enum NOT NULL,
    requiere_sedacion       BOOLEAN NOT NULL DEFAULT FALSE,
    created_at              TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP   NOT NULL DEFAULT NOW()
);

-- 2.14. Tabla: eventos
CREATE TABLE eventos (
    id_evento               SERIAL PRIMARY KEY,
    nombre                  TEXT    NOT NULL,
    descripcion             TEXT,
    fecha_inicio            DATE    NOT NULL,
    fecha_fin               DATE,
    horario_inicio          TIME,
    horario_fin             TIME,
    capacidad_maxima        INTEGER NOT NULL CHECK (capacidad_maxima > 0),
    precio_entrada          DECIMAL(8,2) NOT NULL CHECK (precio_entrada >= 0),
    tipo_evento             tipo_evento_enum   NOT NULL,
    estado                  estado_evento_enum NOT NULL,
    horario_complejo        horario_evento,        -- tipo compuesto (opcional)
    created_at              TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP   NOT NULL DEFAULT NOW()
);

-- 2.15. Tabla: productos
CREATE TABLE productos (
    id_producto             SERIAL PRIMARY KEY,
    nombre                  TEXT    NOT NULL,
    descripcion             TEXT,
    precio                  DECIMAL(10,2) NOT NULL CHECK (precio >= 0),
    stock_actual            INTEGER NOT NULL CHECK (stock_actual >= 0),
    stock_minimo            INTEGER NOT NULL CHECK (stock_minimo >= 0),
    categoria               categoria_producto_enum NOT NULL,
    id_proveedor            INTEGER NOT NULL
        REFERENCES proveedores(id_proveedor)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    activo                  BOOLEAN NOT NULL DEFAULT TRUE,
    created_at              TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP   NOT NULL DEFAULT NOW()
);

-- 2.16. Tabla: horarios
CREATE TABLE horarios (
    id_horario              SERIAL PRIMARY KEY,
    dia_semana              dia_semana_enum     NOT NULL,
    hora_inicio             TIME    NOT NULL,
    hora_fin                TIME    NOT NULL,
    tipo_actividad          TEXT,
    descripcion             TEXT,
    id_empleado             INTEGER
        REFERENCES empleados(id_empleado)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    id_evento               INTEGER
        REFERENCES eventos(id_evento)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    created_at              TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP   NOT NULL DEFAULT NOW()
);


-- ================================================================
-- 3. TABLAS DE CRUCE (RELACIONES N:M)
-- ================================================================

-- 3.1. animal_cuidador (animales ↔ cuidadores)
CREATE TABLE animal_cuidador (
    id                      SERIAL PRIMARY KEY,
    id_animal               INTEGER NOT NULL
        REFERENCES animales(id_animal)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    id_cuidador             INTEGER NOT NULL
        REFERENCES cuidadores(id_cuidador)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    fecha_asignacion        DATE    NOT NULL,
    es_cuidador_principal   BOOLEAN NOT NULL DEFAULT FALSE,
    notas                   TEXT,
    created_at              TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP   NOT NULL DEFAULT NOW(),
    UNIQUE (id_animal, id_cuidador, fecha_asignacion)
);

-- 3.2. animal_alimentacion (animales ↔ alimentos)
CREATE TABLE animal_alimentacion (
    id                      SERIAL PRIMARY KEY,
    id_animal               INTEGER NOT NULL
        REFERENCES animales(id_animal)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    id_alimento             INTEGER NOT NULL
        REFERENCES alimentos(id_alimento)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    id_cuidador             INTEGER NOT NULL
        REFERENCES cuidadores(id_cuidador)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    fecha_alimentacion      DATE    NOT NULL,
    hora_alimentacion       TIME,
    cantidad_kg             DECIMAL(8,2) NOT NULL CHECK (cantidad_kg > 0),
    observaciones           TEXT,
    created_at              TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP   NOT NULL DEFAULT NOW()
);

-- 3.3. visitante_evento (visitantes ↔ eventos)
CREATE TABLE visitante_evento (
    id                      SERIAL PRIMARY KEY,
    id_visitante            INTEGER NOT NULL
        REFERENCES visitantes(id_visitante)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    id_evento               INTEGER NOT NULL
        REFERENCES eventos(id_evento)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    fecha_registro          TIMESTAMP   NOT NULL DEFAULT NOW(),
    precio_pagado           DECIMAL(8,2) NOT NULL CHECK (precio_pagado >= 0),
    asistio                 BOOLEAN NOT NULL DEFAULT FALSE,
    calificacion            INTEGER CHECK (calificacion BETWEEN 1 AND 5),
    comentarios             TEXT,
    created_at              TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP   NOT NULL DEFAULT NOW(),
    UNIQUE (id_visitante, id_evento)
);

-- 3.4. habitat_mantenimiento (habitats ↔ empleados)
CREATE TABLE habitat_mantenimiento (
    id                      SERIAL PRIMARY KEY,
    id_habitat              INTEGER NOT NULL
        REFERENCES habitats(id_habitat)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    id_empleado             INTEGER NOT NULL
        REFERENCES empleados(id_empleado)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    fecha_mantenimiento     DATE    NOT NULL,
    tipo_mantenimiento      tipo_mantenimiento_enum NOT NULL,
    descripcion_trabajo     TEXT,
    costo                   DECIMAL(10,2) NOT NULL CHECK (costo >= 0),
    tiempo_horas            DECIMAL(5,2) NOT NULL CHECK (tiempo_horas >= 0),
    completado              BOOLEAN NOT NULL DEFAULT FALSE,
    created_at              TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP   NOT NULL DEFAULT NOW()
);

-- 3.5. venta_productos (visitantes ↔ productos)
CREATE TABLE venta_productos (
    id                      SERIAL PRIMARY KEY,
    id_visitante            INTEGER NOT NULL
        REFERENCES visitantes(id_visitante)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    id_producto             INTEGER NOT NULL
        REFERENCES productos(id_producto)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    cantidad                INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario         DECIMAL(10,2) NOT NULL CHECK (precio_unitario >= 0),
    fecha_venta             TIMESTAMP   NOT NULL DEFAULT NOW(),
    metodo_pago             metodo_pago_enum    NOT NULL,
    descuento_aplicado      DECIMAL(5,2) CHECK (descuento_aplicado >= 0),
    created_at              TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP   NOT NULL DEFAULT NOW()
);

