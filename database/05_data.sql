-- TRUNCATE ALL TABLES TO ENSURE A CLEAN START (OPTIONAL, BUT RECOMMENDED FOR TESTING)
-- BE CAREFUL WITH CASCADE IF YOU HAVE OTHER DEPENDENCIES OUTSIDE OF THESE SCRIPTS.
-- TRUNCATE TABLE venta_productos, habitat_mantenimiento, visitante_evento, animal_alimentacion, animal_cuidador, horarios RESTART IDENTITY CASCADE;
-- TRUNCATE TABLE animales, habitats, eventos, alimentos, productos RESTART IDENTITY CASCADE;
-- TRUNCATE TABLE cuidadores, veterinarios, departamentos, empleados RESTART IDENTITY CASCADE;
-- TRUNCATE TABLE especies, tipos_habitat, proveedores, tratamientos_medicos, visitantes RESTART IDENTITY CASCADE;

-- ================================================================
-- 1. Inserción de datos en tablas principales sin dependencias fuertes
--    (50 registros cada una)
-- ================================================================

-- 1.1. Tabla: especies (50 registros)
INSERT INTO especies (nombre_cientifico, nombre_comun, reino, filo, clase, orden, familia, genero, estado_conservacion, esperanza_vida, peso_promedio)
SELECT
    'Especie Científica ' || s.id,
    'Especie Común ' || s.id,
    (ARRAY['Animalia', 'Plantae', 'Fungi'])[1 + (s.id % 3)],
    'Filo ' || (s.id % 10),
    'Clase ' || (s.id % 10),
    'Orden ' || (s.id % 10),
    'Familia ' || (s.id % 10),
    'Genero ' || (s.id % 10),
    (ARRAY['peligro', 'vulnerable', 'casi_amenazado', 'preocupacion_menor'])[1 + (s.id % 4)]::estado_conservacion_enum,
    FLOOR(RANDOM() * 50) + 5,
    ROUND(((RANDOM() * 500) + 0.1)::NUMERIC, 2)
FROM generate_series(1, 50) AS s(id);

-- 1.2. Tabla: tipos_habitat (50 registros)
INSERT INTO tipos_habitat (nombre, descripcion, temperatura_min, temperatura_max, humedad_min, humedad_max)
SELECT
    'Tipo Hábitat ' || s.id,
    'Descripción para el hábitat ' || s.id || '.',
    ROUND(((RANDOM() * 15) + 5)::NUMERIC, 2),
    ROUND(((RANDOM() * 20) + 25)::NUMERIC, 2),
    ROUND(((RANDOM() * 30) + 30)::NUMERIC, 2),
    ROUND(((RANDOM() * 20) + 70)::NUMERIC, 2)
FROM generate_series(1, 50) AS s(id);

-- 1.3. Tabla: proveedores (50 registros)
INSERT INTO proveedores (nombre_empresa, contacto_principal, email, telefono, direccion, tipo_proveedor, calificacion, activo)
SELECT
    'Proveedor ' || s.id || ' S.A.',
    'Contacto ' || s.id,
    'contacto' || s.id || '@proveedor.com',
    '502' || LPAD((s.id * 1000 + FLOOR(RANDOM() * 999))::text, 7, '0'),
    'Dirección ' || s.id || ', Ciudad ' || (s.id % 5),
    (ARRAY['alimentos', 'medicamentos', 'equipos', 'construccion'])[1 + (s.id % 4)]::tipo_proveedor_enum,
    (s.id % 5) + 1,
    TRUE
FROM generate_series(1, 50) AS s(id);

-- 1.4. Tabla: tratamientos_medicos (50 registros)
INSERT INTO tratamientos_medicos (nombre, descripcion, costo_base, duracion_estimada_dias, tipo_tratamiento, requiere_sedacion)
SELECT
    'Tratamiento Médico ' || s.id,
    'Descripción del tratamiento médico ' || s.id || '.',
    ROUND(((RANDOM() * 1000) + 20)::NUMERIC, 2),
    FLOOR(RANDOM() * 30) + 1,
    (ARRAY['preventivo', 'curativo', 'rutina', 'emergencia'])[1 + (s.id % 4)]::tipo_tratamiento_enum,
    (s.id % 2 = 0)
FROM generate_series(1, 50) AS s(id);

-- 1.5. Tabla: visitantes (50 registros)
INSERT INTO visitantes (nombre, apellido, email, telefono, fecha_nacimiento, nacionalidad, tipo_visitante)
SELECT
    'VisitanteNombre' || s.id,
    'VisitanteApellido' || s.id,
    'visitante' || s.id || '@mail.com',
    '502' || LPAD((s.id * 1000 + FLOOR(RANDOM() * 999))::text, 7, '0'),
    (CURRENT_DATE - (FLOOR(RANDOM() * 60 * 365) + 365 * 5)::int * INTERVAL '1 day')::date,
    (ARRAY['Guatemalteca', 'Mexicana', 'Española', 'Argentina', 'Colombiana', 'Canadiense', 'Estadounidense'])[1 + (s.id % 7)],
    (ARRAY['adulto', 'niño', 'estudiante', 'adulto_mayor'])[1 + (s.id % 4)]::tipo_visitante_enum
FROM generate_series(1, 50) AS s(id);

-- ================================================================
-- 2. Inserción de datos con dependencias (empleados, departamentos, cuidadores, veterinarios)
--    (50 registros cada una)
-- ================================================================

-- 2.1. Tabla: empleados (50 registros) - Insertar sin id_departamento inicialmente
INSERT INTO empleados (nombre, apellido, email, telefono, cargo, fecha_contratacion, salario, tipo_empleado, activo)
SELECT
    'EmpleadoNombre' || s.id,
    'EmpleadoApellido' || s.id,
    'empleado' || s.id || '@zoo.com',
    '502' || LPAD((s.id * 1000 + FLOOR(RANDOM() * 999))::text, 7, '0'),
    (ARRAY['Administrador', 'Jefe de Cuidadores', 'Veterinario', 'Cuidador', 'Asistente Administrativo', 'Tecnico de Mantenimiento'])[1 + (s.id % 6)],
    (CURRENT_DATE - (FLOOR(RANDOM() * 10 * 365))::int * INTERVAL '1 day')::date,
    ROUND(((RANDOM() * 3000) + 1500)::NUMERIC, 2),
    (ARRAY['administrativo', 'operativo', 'especialista'])[1 + (s.id % 3)]::tipo_empleado_enum,
    TRUE
FROM generate_series(1, 50) AS s(id);

-- 2.2. Tabla: departamentos (50 registros)
INSERT INTO departamentos (nombre, presupuesto_anual, descripcion, jefe_departamento_id)
SELECT
    'Departamento ' || s.id,
    ROUND(((RANDOM() * 500000) + 100000)::NUMERIC, 2),
    'Descripción del departamento ' || s.id || '.',
    NULL
FROM generate_series(1, 50) AS s(id);

-- 2.3. Actualizar empleados con id_departamento
UPDATE empleados e
SET id_departamento = d_asign.random_departamento_id
FROM (
    SELECT
        id_empleado,
        (SELECT id_departamento FROM departamentos ORDER BY RANDOM() LIMIT 1) AS random_departamento_id
    FROM empleados
) AS d_asign
WHERE e.id_empleado = d_asign.id_empleado;

-- Actualizar jefe_departamento_id en departamentos (uno para cada departamento)
UPDATE departamentos d
SET jefe_departamento_id = (SELECT id_empleado FROM empleados WHERE id_departamento IS NOT NULL ORDER BY RANDOM() LIMIT 1)
WHERE d.jefe_departamento_id IS NULL;


-- 2.4. Tabla: cuidadores (50 registros)
INSERT INTO cuidadores (id_cuidador, especialidad, años_experiencia, certificaciones, nivel_autoridad)
SELECT
    e.id_empleado,
    (ARRAY['Mamíferos Grandes', 'Felinos', 'Aves', 'Reptiles', 'Primates', 'Anfibios', 'Peces'])[1 + (e.id_empleado % 7)],
    FLOOR(RANDOM() * 15) + 1,
    (ARRAY['Primeros auxilios animales', 'Comportamiento animal', 'Herpetología avanzada', 'Enriquecimiento ambiental', 'Nutrición veterinaria'])[1 + (e.id_empleado % 5)],
    (e.id_empleado % 5) + 1
FROM empleados e
WHERE e.id_empleado <= 50;

-- 2.5. Tabla: veterinarios (50 registros)
INSERT INTO veterinarios (id_veterinario, numero_colegiado, especialidad_veterinaria, universidad_titulo, años_experiencia)
SELECT
    e.id_empleado,
    'VET-' || LPAD(e.id_empleado::text, 3, '0') || '-GT',
    (ARRAY['Cirugía y medicina interna', 'Salud pública veterinaria', 'Nutrición Animal', 'Dermatología', 'Cardiología', 'Parasitología', 'Radiología'])[1 + (e.id_empleado % 7)],
    (ARRAY['Universidad del Valle', 'Universidad San Carlos', 'Universidad Rural', 'Universidad Mariano Gálvez', 'Universidad Panamericana'])[1 + (e.id_empleado % 5)],
    FLOOR(RANDOM() * 20) + 1
FROM empleados e
WHERE e.tipo_empleado = 'especialista' AND e.cargo LIKE '%Veterinario%'
ORDER BY e.id_empleado
LIMIT 50;

INSERT INTO veterinarios (id_veterinario, numero_colegiado, especialidad_veterinaria, universidad_titulo, años_experiencia)
SELECT
    e.id_empleado,
    'VET-' || LPAD(e.id_empleado::text, 3, '0') || '-GT',
    (ARRAY['Cirugía y medicina interna', 'Salud pública veterinaria', 'Nutrición Animal', 'Dermatología', 'Cardiología', 'Parasitología', 'Radiología'])[1 + (e.id_empleado % 7)],
    (ARRAY['Universidad del Valle', 'Universidad San Carlos', 'Universidad Rural', 'Universidad Mariano Gálvez', 'Universidad Panamericana'])[1 + (e.id_empleado % 5)],
    FLOOR(RANDOM() * 20) + 1
FROM empleados e
WHERE e.id_empleado NOT IN (SELECT id_veterinario FROM veterinarios)
ORDER BY RANDOM()
LIMIT (50 - (SELECT COUNT(*) FROM veterinarios));

-- ================================================================
-- 3. Inserción de datos con dependencias (habitats, animales, eventos, alimentos, productos)
--    (50 registros cada una)
-- ================================================================

-- 3.1. Tabla: habitats (50 registros)
INSERT INTO habitats (nombre, id_tipo_habitat, ubicacion, capacidad_maxima, area_metros_cuadrados, fecha_construccion, estado, costo_mantenimiento_mensual)
SELECT
    'Hábitat ' || s.id,
    (SELECT id_tipo_habitat FROM tipos_habitat ORDER BY RANDOM() LIMIT 1),
    ROW(RANDOM() * 180 - 90, RANDOM() * 360 - 180, FLOOR(RANDOM() * 2000))::coordenadas,
    FLOOR(RANDOM() * 50) + 50, -- Capacity between 50 and 100
    ROUND(((RANDOM() * 1000) + 100)::NUMERIC, 2),
    (CURRENT_DATE - (FLOOR(RANDOM() * 10 * 365))::int * INTERVAL '1 day')::date,
    (ARRAY['activo', 'mantenimiento'])[1 + (s.id % 2)]::estado_habitat_enum,
    ROUND(((RANDOM() * 1000) + 200)::NUMERIC, 2)
FROM generate_series(1, 50) AS s(id);

-- 3.2. Tabla: animales (50 registros)
INSERT INTO animales (nombre, id_especie, id_habitat, fecha_nacimiento, sexo, peso_actual, altura, numero_identificacion, origen, estado_salud)
SELECT
    'Animal' || s.id,
    (SELECT id_especie FROM especies ORDER BY RANDOM() LIMIT 1),
    (SELECT id_habitat FROM habitats ORDER BY RANDOM() LIMIT 1),
    (CURRENT_DATE - (FLOOR(RANDOM() * 30 * 365) + 365)::int * INTERVAL '1 day')::date,
    (ARRAY['M', 'F'])[1 + (s.id % 2)]::sexo_animal_enum,
    ROUND(((RANDOM() * 500) + 0.1)::NUMERIC, 2),
    ROUND(((RANDOM() * 3) + 0.1)::NUMERIC, 2),
    'ANI-' || LPAD(s.id::text, 3, '0'),
    (ARRAY['rescate', 'intercambio', 'nacido_zoologico', 'compra'])[1 + (s.id % 4)]::origen_animal_enum,
    (ARRAY['excelente', 'bueno', 'regular'])[1 + (s.id % 3)]::estado_salud_enum
FROM generate_series(1, 50) AS s(id);

-- 3.3. Tabla: eventos (50 registros)
INSERT INTO eventos (nombre, descripcion, fecha_inicio, fecha_fin, horario_inicio, horario_fin, capacidad_maxima, precio_entrada, tipo_evento, estado, horario_complejo)
SELECT
    'Evento ' || s.id,
    'Descripción del evento ' || s.id || '.',
    (CURRENT_DATE + (FLOOR(RANDOM() * 365))::int * INTERVAL '1 day')::date,
    (CURRENT_DATE + (FLOOR(RANDOM() * 365) + 1)::int * INTERVAL '1 day')::date,
    (TIME '09:00:00' + (FLOOR(RANDOM() * 8) * INTERVAL '1 hour')),
    (TIME '09:00:00' + (FLOOR(RANDOM() * 8) * INTERVAL '1 hour') + (FLOOR(RANDOM() * 2) * INTERVAL '1 hour')),
    FLOOR(RANDOM() * 100) + 10,
    ROUND(((RANDOM() * 20) + 5)::NUMERIC, 2),
    (ARRAY['educativo', 'especial', 'entretenimiento'])[1 + (s.id % 3)]::tipo_evento_enum,
    (ARRAY['programado', 'cancelado', 'finalizado'])[1 + (s.id % 3)]::estado_evento_enum,
    ROW(ARRAY[FLOOR(RANDOM() * 7) + 1, FLOOR(RANDOM() * 7) + 1]::int[],
        (TIME '09:00:00' + (FLOOR(RANDOM() * 8) * INTERVAL '1 hour')),
        (TIME '09:00:00' + (FLOOR(RANDOM() * 8) * INTERVAL '1 hour') + (FLOOR(RANDOM() * 2) * INTERVAL '1 hour')),
        FLOOR(RANDOM() * 240) + 30,
        (ARRAY['diario', 'semanal', 'mensual', 'anual'])[1 + (s.id % 4)]
    )::horario_evento
FROM generate_series(1, 50) AS s(id);

-- 3.4. Tabla: alimentos (50 registros)
INSERT INTO alimentos (nombre, id_proveedor, tipo_alimento, info_nutricional, calorias_por_kg, proteinas_porcentaje, grasas_porcentaje, carbohidratos_porcentaje, costo_por_kg, fecha_vencimiento, stock_actual, stock_minimo)
SELECT
    'Alimento ' || s.id,
    (SELECT id_proveedor FROM proveedores ORDER BY RANDOM() LIMIT 1),
    (ARRAY['carnivoro', 'herbivoro', 'omnivoro'])[1 + (s.id % 3)]::tipo_alimento_enum,
    ROW(
        FLOOR(RANDOM() * 2000) + 100,
        ROUND((RANDOM() * 30)::NUMERIC, 2),
        ROUND((RANDOM() * 20)::NUMERIC, 2),
        ROUND((RANDOM() * 50)::NUMERIC, 2),
        ROUND((RANDOM() * 10)::NUMERIC, 2),
        (ARRAY['{"hierro", "B12"}', '{"fibra", "C"}', '{"A", "D"}', '{"C", "K"}', '{"proteina", "calcio"}'])[1 + (s.id % 5)]
    )::info_nutricional,
    FLOOR(RANDOM() * 2000) + 100,
    ROUND((RANDOM() * 30)::NUMERIC, 2),
    ROUND((RANDOM() * 20)::NUMERIC, 2),
    ROUND((RANDOM() * 50)::NUMERIC, 2),
    ROUND(((RANDOM() * 10) + 1)::NUMERIC, 2),
    (CURRENT_DATE + (FLOOR(RANDOM() * 365))::int * INTERVAL '1 day')::date,
    FLOOR(RANDOM() * 1000) + 50,
    FLOOR(RANDOM() * 50) + 10
FROM generate_series(1, 50) AS s(id);

-- 3.5. Tabla: productos (50 registros)
INSERT INTO productos (nombre, descripcion, precio, stock_actual, stock_minimo, categoria, id_proveedor, activo)
SELECT
    'Producto ' || s.id,
    'Descripción del producto ' || s.id || '.',
    ROUND(((RANDOM() * 40) + 5)::NUMERIC, 2),
    FLOOR(RANDOM() * 500) + 50, -- Stock actual between 50 and 550
    FLOOR(RANDOM() * 30) + 5,
    (ARRAY['souvenir', 'educativo', 'ropa'])[1 + (s.id % 3)]::categoria_producto_enum,
    (SELECT id_proveedor FROM proveedores ORDER BY RANDOM() LIMIT 1),
    TRUE
FROM generate_series(1, 50) AS s(id);

-- ================================================================
-- 4. Inserción de datos en tablas de cruce
--    (50 registros cada una, asegurando IDs válidos)
-- ================================================================

-- 4.1. Tabla: animal_cuidador (50 registros)
INSERT INTO animal_cuidador (id_animal, id_cuidador, fecha_asignacion, es_cuidador_principal, notas)
SELECT
    (SELECT id_animal FROM animales ORDER BY id_animal OFFSET (s.id - 1) LIMIT 1),
    (SELECT id_cuidador FROM cuidadores ORDER BY id_cuidador OFFSET (s.id - 1) LIMIT 1),
    (CURRENT_DATE - (s.id - 1)::int * INTERVAL '1 day')::date,
    (s.id % 2 = 0),
    'Nota del cuidador ' || s.id || '.'
FROM generate_series(1, 50) AS s(id);

-- 4.2. Tabla: animal_alimentacion (50 registros)
INSERT INTO animal_alimentacion (id_animal, id_alimento, id_cuidador, fecha_alimentacion, hora_alimentacion, cantidad_kg, observaciones)
SELECT
    (SELECT id_animal FROM animales ORDER BY RANDOM() LIMIT 1),
    (SELECT id_alimento FROM alimentos ORDER BY RANDOM() LIMIT 1),
    (SELECT id_cuidador FROM cuidadores ORDER BY RANDOM() LIMIT 1),
    (CURRENT_DATE - (FLOOR(RANDOM() * 30))::int * INTERVAL '1 day')::date,
    (TIME '08:00:00' + (FLOOR(RANDOM() * 10) * INTERVAL '1 hour')),
    ROUND(((RANDOM() * 10) + 0.1)::NUMERIC, 2),
    'Observación de alimentación ' || s.id || '.'
FROM generate_series(1, 50) AS s(id);

-- 4.3. Tabla: visitante_evento (50 registros)
INSERT INTO visitante_evento (id_visitante, id_evento, fecha_registro, precio_pagado, asistio, calificacion, comentarios)
SELECT
    (SELECT id_visitante FROM visitantes ORDER BY id_visitante OFFSET (s.id - 1) LIMIT 1),
    (SELECT id_evento FROM eventos ORDER BY id_evento OFFSET (s.id - 1) LIMIT 1),
    (NOW() - (FLOOR(RANDOM() * 30 * 24 * 60) * INTERVAL '1 minute')),
    ROUND(((RANDOM() * 20) + 5)::NUMERIC, 2),
    (s.id % 5 != 0),
    CASE WHEN (s.id % 5 != 0) THEN (s.id % 5) + 1 ELSE NULL END,
    'Comentario del visitante ' || s.id || '.'
FROM generate_series(1, 50) AS s(id);

-- 4.4. Tabla: habitat_mantenimiento (50 registros)
INSERT INTO habitat_mantenimiento (id_habitat, id_empleado, fecha_mantenimiento, tipo_mantenimiento, descripcion_trabajo, costo, tiempo_horas, completado)
SELECT
    (SELECT id_habitat FROM habitats ORDER BY RANDOM() LIMIT 1),
    (SELECT id_empleado FROM empleados ORDER BY RANDOM() LIMIT 1),
    (CURRENT_DATE - (FLOOR(RANDOM() * 90))::int * INTERVAL '1 day')::date,
    (ARRAY['limpieza', 'reparacion', 'inspeccion', 'mejora'])[1 + (s.id % 4)]::tipo_mantenimiento_enum,
    'Trabajo de mantenimiento ' || s.id || '.',
    ROUND(((RANDOM() * 400) + 50)::NUMERIC, 2),
    ROUND(((RANDOM() * 10) + 1)::NUMERIC, 2),
    (s.id % 3 != 0)
FROM generate_series(1, 50) AS s(id);

-- 4.5. Tabla: venta_productos (50 registros)
INSERT INTO venta_productos (id_visitante, id_producto, cantidad, precio_unitario, fecha_venta, metodo_pago, descuento_aplicado)
SELECT
    (SELECT id_visitante FROM visitantes ORDER BY RANDOM() LIMIT 1),
    (SELECT id_producto FROM productos ORDER BY RANDOM() LIMIT 1),
    FLOOR(RANDOM() * 5) + 1,
    (SELECT ROUND((p.precio * (1 - RANDOM() * 0.1))::NUMERIC, 2) FROM productos p ORDER BY RANDOM() LIMIT 1),
    (NOW() - (FLOOR(RANDOM() * 60 * 24 * 30) * INTERVAL '1 minute')),
    (ARRAY['tarjeta', 'efectivo', 'transferencia'])[1 + (s.id % 3)]::metodo_pago_enum,
    ROUND((RANDOM() * 0.15)::NUMERIC, 2)
FROM generate_series(1, 50) AS s(id);

-- 4.6. Tabla: horarios (50 registros)
INSERT INTO horarios (dia_semana, hora_inicio, hora_fin, tipo_actividad, descripcion, id_empleado, id_evento)
SELECT
    (ARRAY['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'])[1 + (s.id % 7)]::dia_semana_enum,
    (TIME '08:00:00' + (FLOOR(RANDOM() * 8) * INTERVAL '1 hour')),
    (TIME '08:00:00' + (FLOOR(RANDOM() * 8) * INTERVAL '1 hour') + (FLOOR(RANDOM() * 2) * INTERVAL '1 hour')),
    -- FIX: Removed ::tipo_actividad_enum cast, assuming it's VARCHAR/TEXT or has a different enum name
    (ARRAY['Cuidado Animal', 'Revision Veterinaria', 'Alimentacion Publica', 'Mantenimiento de Infraestructura', 'Charla Educativa', 'Administrativo'])[1 + (s.id % 6)],
    'Actividad programada ' || s.id || '.',
    CASE WHEN (s.id % 2 = 0) THEN (SELECT id_empleado FROM empleados ORDER BY RANDOM() LIMIT 1) ELSE NULL END,
    CASE WHEN (s.id % 2 != 0) THEN (SELECT id_evento FROM eventos ORDER BY RANDOM() LIMIT 1) ELSE NULL END
FROM generate_series(1, 50) AS s(id);

-- ================================================================
-- 5. Generación masiva de datos para alcanzar +500 registros
--    (Para tablas con alta frecuencia de inserción o interrelaciones)
-- ================================================================

-- 5.1. Generación de 100 visitantes adicionales
--    Se generarán emails únicos con un UUID, y nacionalidades y tipos aleatorios
INSERT INTO visitantes (nombre, apellido, email, telefono, fecha_nacimiento, nacionalidad, tipo_visitante)
SELECT
    'Visitante' || (ROW_NUMBER() OVER () + 5) AS nombre, -- Empieza desde el 6to visitante
    'Apellido' || (ROW_NUMBER() OVER () + 5) AS apellido,
    'visitor' || REPLACE(GEN_RANDOM_UUID()::TEXT, '-', '') || '@example.com' AS email,
    '502' || LPAD((FLOOR(RANDOM() * 99999999))::TEXT, 8, '0') AS telefono,
    (CURRENT_DATE - (FLOOR(RANDOM() * 365 * 50) + 365 * 10 || ' days')::INTERVAL)::DATE AS fecha_nacimiento,
    CASE FLOOR(RANDOM() * 5)
        WHEN 0 THEN 'Guatemalteca'
        WHEN 1 THEN 'Mexicana'
        WHEN 2 THEN 'Salvadoreña'
        WHEN 3 THEN 'Hondureña'
        ELSE 'Costarricense'
    END AS nacionalidad,
    (CASE FLOOR(RANDOM() * 4) -- ¡CORRECCIÓN AQUÍ!
        WHEN 0 THEN 'adulto'
        WHEN 1 THEN 'niño'
        WHEN 2 THEN 'estudiante'
        ELSE 'adulto_mayor'
    END)::tipo_visitante_enum AS tipo_visitante -- <<--- CAST explícito
FROM GENERATE_SERIES(1, 100);

-- 5.2. Generación masiva de Registros de Alimentación Animal (alrededor de 200 registros)
--    Combinando animales existentes, alimentos y cuidadores
INSERT INTO animal_alimentacion (id_animal, id_alimento, id_cuidador, fecha_alimentacion, hora_alimentacion, cantidad_kg, observaciones)
SELECT
    a.id_animal,
    al.id_alimento,
    c.id_cuidador,
    (CURRENT_DATE - (FLOOR(RANDOM() * 365) || ' days')::INTERVAL)::DATE AS fecha_alimentacion,
    (TIME '08:00:00' + (FLOOR(RANDOM() * 10) * INTERVAL '1 hour'))::TIME AS hora_alimentacion,
    (RANDOM() * 10 + 0.1)::DECIMAL(8,2) AS cantidad_kg, -- Cantidad entre 0.1 y 10.1 kg
    CASE FLOOR(RANDOM() * 3)
        WHEN 0 THEN 'Comió con apetito.'
        WHEN 1 THEN 'Alimentación estándar.'
        ELSE 'Observado consumiendo la ración completa.'
    END AS observaciones
FROM
    animales a,
    alimentos al,
    cuidadores c
ORDER BY RANDOM()
LIMIT 200;

-- 5.3. Generación masiva de Asistencias a Eventos (alrededor de 200 registros)
--    Combinando visitantes y eventos existentes
INSERT INTO visitante_evento (id_visitante, id_evento, fecha_registro, precio_pagado, asistio, calificacion, comentarios)
SELECT
    v.id_visitante,
    e.id_evento,
    (CURRENT_TIMESTAMP - (FLOOR(RANDOM() * 300) || ' days')::INTERVAL - (FLOOR(RANDOM() * 24) || ' hours')::INTERVAL - (FLOOR(RANDOM() * 60) || ' minutes')::INTERVAL)::TIMESTAMP AS fecha_registro,
    e.precio_entrada * (1 - (FLOOR(RANDOM() * 2) * 0.1))::DECIMAL(8,2) AS precio_pagado, -- Descuento del 0% o 10%
    CASE WHEN RANDOM() < 0.9 THEN TRUE ELSE FALSE END AS asistio, -- 90% de probabilidad de asistir
    (FLOOR(RANDOM() * 5) + 1)::INTEGER AS calificacion, -- Calificación del 1 al 5
    CASE FLOOR(RANDOM() * 4)
        WHEN 0 THEN 'Evento muy bueno, lo recomendaría.'
        WHEN 1 THEN 'Experiencia agradable y educativa.'
        WHEN 2 THEN 'Faltó algo de interacción, pero bien.'
        WHEN 3 THEN 'Buena organización.'
        ELSE 'Sin comentarios.'
    END AS comentarios
FROM
    visitantes v,
    eventos e
WHERE
    e.fecha_inicio <= CURRENT_DATE + INTERVAL '30 days' -- Solo eventos pasados o próximos 30 días
ORDER BY RANDOM()
LIMIT 200
ON CONFLICT (id_visitante, id_evento) DO NOTHING; -- <--- ¡Añadido aquí!

-- 5.4. Generación masiva de Mantenimientos de Hábitats (alrededor de 50 registros)
--    Combinando hábitats y empleados existentes
INSERT INTO habitat_mantenimiento (id_habitat, id_empleado, fecha_mantenimiento, tipo_mantenimiento, descripcion_trabajo, costo, tiempo_horas, completado)
SELECT
    h.id_habitat,
    e.id_empleado,
    (CURRENT_DATE - (FLOOR(RANDOM() * 180) || ' days')::INTERVAL)::DATE AS fecha_mantenimiento,
    (CASE FLOOR(RANDOM() * 4) -- ¡CORRECCIÓN AQUÍ!
        WHEN 0 THEN 'limpieza'
        WHEN 1 THEN 'reparacion'
        WHEN 2 THEN 'inspeccion'
        ELSE 'mejora'
    END)::tipo_mantenimiento_enum AS tipo_mantenimiento, -- <<--- CAST explícito (Asumo que tienes un ENUM para esto)
    'Trabajo de mantenimiento rutinario en ' || h.nombre AS descripcion_trabajo,
    (RANDOM() * 500 + 50)::DECIMAL(10,2) AS costo,
    (RANDOM() * 16 + 1)::DECIMAL(5,2) AS tiempo_horas,
    CASE WHEN RANDOM() < 0.95 THEN TRUE ELSE FALSE END AS completado -- 95% de probabilidad de completado
FROM
    habitats h,
    empleados e
WHERE
    e.tipo_empleado IN ('operativo', 'especialista') -- Empleados relevantes para mantenimiento
ORDER BY RANDOM()
LIMIT 50;

-- 5.5. Generación masiva de Ventas de Productos (alrededor de 50 registros)
--    Combinando visitantes y productos existentes
INSERT INTO venta_productos (id_visitante, id_producto, cantidad, precio_unitario, fecha_venta, metodo_pago, descuento_aplicado)
SELECT
    v.id_visitante,
    p.id_producto,
    (FLOOR(RANDOM() * 3) + 1)::INTEGER AS cantidad, -- Cantidad entre 1 y 3
    p.precio AS precio_unitario,
    (CURRENT_TIMESTAMP - (FLOOR(RANDOM() * 300) || ' days')::INTERVAL - (FLOOR(RANDOM() * 24) || ' hours')::INTERVAL)::TIMESTAMP AS fecha_venta,
    (CASE FLOOR(RANDOM() * 3) -- ¡CORRECCIÓN AQUÍ!
        WHEN 0 THEN 'tarjeta'
        WHEN 1 THEN 'efectivo'
        ELSE 'transferencia'
    END)::metodo_pago_enum AS metodo_pago, -- <<--- CAST explícito (Asumo que tienes un ENUM para esto)
    (FLOOR(RANDOM() * 2) * 0.05)::DECIMAL(8,2) AS descuento_aplicado -- 0% o 5% de descuento
FROM
    visitantes v,
    productos p
ORDER BY RANDOM()
LIMIT 50;