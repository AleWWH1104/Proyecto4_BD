-- ================================================================
-- 1. Inserción de datos en tablas principales sin dependencias fuertes
-- ================================================================

-- 1.1. Tabla: especies (5 registros)
INSERT INTO especies (nombre_cientifico, nombre_comun, reino, filo, clase, orden, familia, genero, estado_conservacion, esperanza_vida, peso_promedio) VALUES
('Panthera tigris', 'Tigre de Bengala', 'Animalia', 'Chordata', 'Mammalia', 'Carnivora', 'Felidae', 'Panthera', 'peligro', 18, 220.50),
('Ailuropoda melanoleuca', 'Panda Gigante', 'Animalia', 'Chordata', 'Mammalia', 'Carnivora', 'Ursidae', 'Ailuropoda', 'vulnerable', 20, 110.00),
('Giraffa camelopardalis', 'Jirafa', 'Animalia', 'Chordata', 'Mammalia', 'Artiodactyla', 'Giraffidae', 'Giraffa', 'casi_amenazado', 25, 1200.00),
('Loxodonta africana', 'Elefante Africano', 'Animalia', 'Chordata', 'Mammalia', 'Proboscidea', 'Elephantidae', 'Loxodonta', 'vulnerable', 60, 4500.00),
('Brachypelma hamorii', 'Tarántula de Rodillas Rojas', 'Animalia', 'Arthropoda', 'Arachnida', 'Araneae', 'Theraphosidae', 'Brachypelma', 'casi_amenazado', 15, 0.05);

-- 1.2. Tabla: tipos_habitat (5 registros)
INSERT INTO tipos_habitat (nombre, descripcion, temperatura_min, temperatura_max, humedad_min, humedad_max) VALUES
('Bosque Tropical', 'Hábitat denso y húmedo con mucha vegetación.', 22.00, 30.00, 70.00, 95.00),
('Área Montañosa', 'Terreno rocoso y escarpado, con variaciones de temperatura.', 5.00, 20.00, 40.00, 70.00),
('Desierto', 'Clima árido con grandes fluctuaciones de temperatura.', 15.00, 40.00, 10.00, 30.00),
('Pradera Abierta', 'Extensas áreas de pastizales con arbustos dispersos.', 10.00, 28.00, 50.00, 80.00),
('Recinto Acuático', 'Área diseñada para especies acuáticas y semi-acuáticas.', 18.00, 25.00, 80.00, 100.00);

-- 1.3. Tabla: proveedores (5 registros)
INSERT INTO proveedores (nombre_empresa, contacto_principal, email, telefono, direccion, tipo_proveedor, calificacion, activo) VALUES
('ZooFood S.A.', 'Juan Pérez', 'contacto@zoofood.com', '12345678', 'Calle Falsa 123, Ciudad', 'alimentos', 5, TRUE),
('MediAnimal Corp.', 'María Gómez', 'info@medicanimal.net', '87654321', 'Avenida Siempreviva 742, Pueblo', 'medicamentos', 4, TRUE),
('EquipZoológico Ltda.', 'Carlos Ruiz', 'ventas@equipzoo.com', '98761234', 'Blvd. de los Sueños 45, Villa', 'equipos', 4, TRUE),
('ConstructoZoo', 'Ana Torres', 'proyectos@constructozoo.org', '43218765', 'Plaza Central 1, Metrópolis', 'construccion', 3, TRUE),
('NutriZoo Supplies', 'Pedro Sánchez', 'pedro@nutrizoo.com', '55511223', 'Calle del Sol 8, Campo', 'alimentos', 5, TRUE);

-- 1.4. Tabla: tratamientos_medicos (5 registros)
INSERT INTO tratamientos_medicos (nombre, descripcion, costo_base, duracion_estimada_dias, tipo_tratamiento, requiere_sedacion) VALUES
('Vacuna Triple Felina', 'Vacuna anual para gatos grandes.', 50.00, 1, 'preventivo', FALSE),
('Antibiótico Espectro Amplio', 'Tratamiento para infecciones bacterianas.', 120.00, 7, 'curativo', FALSE),
('Cirugía Menor', 'Remoción de quiste benigno.', 500.00, 15, 'curativo', TRUE),
('Revisión General Anual', 'Chequeo completo de rutina.', 80.00, 1, 'rutina', FALSE),
('Fluidoterapia de Emergencia', 'Administración intravenosa de fluidos.', 200.00, 2, 'emergencia', TRUE);

-- 1.5. Tabla: visitantes (5 registros)
INSERT INTO visitantes (nombre, apellido, email, telefono, fecha_nacimiento, nacionalidad, tipo_visitante) VALUES
('Laura', 'Martínez', 'laura.m@email.com', '111222333', '1985-03-20', 'Guatemalteca', 'adulto'),
('Diego', 'García', 'diego.g@email.com', '444555666', '2010-08-12', 'Mexicana', 'niño'),
('Sofía', 'Rodríguez', 'sofia.r@email.com', '777888999', '2002-11-01', 'Española', 'estudiante'),
('Jorge', 'Hernández', 'jorge.h@email.com', '101010101', '1955-06-05', 'Argentina', 'adulto_mayor'),
('Isabel', 'Flores', 'isabel.f@email.com', '202020202', '1992-01-25', 'Colombiana', 'adulto');

-- ================================================================
-- 2. Inserción de datos con dependencias (empleados, departamentos, cuidadores, veterinarios)
-- ================================================================

-- 2.1. Tabla: empleados (5 registros) - Insertar algunos sin jefe_departamento_id al principio
INSERT INTO empleados (nombre, apellido, email, telefono, cargo, fecha_contratacion, salario, tipo_empleado, activo) VALUES
('Juan', 'Gómez', 'juan.g@zoo.com', '50212345678', 'Administrador General', '2015-01-01', 5000.00, 'administrativo', TRUE),
('Ana', 'López', 'ana.l@zoo.com', '50298765432', 'Jefe de Cuidadores', '2018-05-10', 3500.00, 'operativo', TRUE),
('Pedro', 'Díaz', 'pedro.d@zoo.com', '50211223344', 'Veterinario Principal', '2017-03-20', 4000.00, 'especialista', TRUE),
('Marta', 'Ramírez', 'marta.r@zoo.com', '50255667788', 'Cuidadora de Felinos', '2020-01-15', 2500.00, 'operativo', TRUE),
('Luis', 'Soto', 'luis.s@zoo.com', '50299887766', 'Asistente Administrativo', '2022-07-01', 2000.00, 'administrativo', TRUE);

-- 2.2. Tabla: departamentos (5 registros)
INSERT INTO departamentos (nombre, presupuesto_anual, descripcion, jefe_departamento_id) VALUES
('Dirección General', 1000000.00, 'Gestión y administración general del zoológico.', 1), -- Juan Gómez es id_empleado 1
('Operaciones de Cuidado Animal', 300000.00, 'Manejo diario y bienestar de los animales.', 2), -- Ana López es id_empleado 2
('Veterinaria', 250000.00, 'Salud y tratamientos médicos para los animales.', 3), -- Pedro Díaz es id_empleado 3
('Marketing y Eventos', 150000.00, 'Promoción y organización de eventos.', NULL),
('Recursos Humanos', 180000.00, 'Gestión del personal y beneficios.', NULL);

-- 2.3. Actualizar empleados con id_departamento (ya que departamentos ya existe)
UPDATE empleados SET id_departamento = 1 WHERE id_empleado = 1; -- Juan Gómez
UPDATE empleados SET id_departamento = 2 WHERE id_empleado = 2; -- Ana López
UPDATE empleados SET id_departamento = 3 WHERE id_empleado = 3; -- Pedro Díaz
UPDATE empleados SET id_departamento = 2 WHERE id_empleado = 4; -- Marta Ramírez
UPDATE empleados SET id_departamento = 1 WHERE id_empleado = 5; -- Luis Soto

-- 2.4. Tabla: cuidadores (5 registros)
INSERT INTO cuidadores (id_cuidador, especialidad, años_experiencia, certificaciones, nivel_autoridad) VALUES
(2, 'Mamíferos Grandes', 8, 'Primeros auxilios animales', 4), -- Ana López
(4, 'Felinos', 4, 'Comportamiento animal', 3), -- Marta Ramírez
((SELECT id_empleado FROM empleados WHERE nombre = 'Luis' AND apellido = 'Soto'), 'Aves', 2, 'Manejo de aves', 2), -- Ejemplo: un asistente administrativo también puede ser cuidador
((SELECT id_empleado FROM empleados WHERE nombre = 'Juan' AND apellido = 'Gómez'), 'Reptiles', 10, 'Herpetología avanzada', 5), -- Ejemplo: el admin general es también experto
((SELECT id_empleado FROM empleados WHERE nombre = 'Pedro' AND apellido = 'Díaz'), 'Primates', 7, 'Enriquecimiento ambiental', 4); -- Ejemplo: un veterinario también puede ser cuidador

-- 2.5. Tabla: veterinarios (5 registros)
INSERT INTO veterinarios (id_veterinario, numero_colegiado, especialidad_veterinaria, universidad_titulo, años_experiencia) VALUES
(3, 'VET-001-GT', 'Cirugía y medicina interna', 'Universidad del Valle', 10), -- Pedro Díaz

-- Asegurarse de que cada tupla tenga 5 valores
((SELECT id_empleado FROM empleados WHERE nombre = 'Juan' AND apellido = 'Gómez'), 'VET-002-GT', 'Salud pública veterinaria', 'Universidad San Carlos', 15), -- Añadido numero_colegiado
((SELECT id_empleado FROM empleados WHERE nombre = 'Ana' AND apellido = 'López'), 'VET-003-GT', 'Nutrición Animal', 'Universidad Rural', 7), -- Añadido numero_colegiado
((SELECT id_empleado FROM empleados WHERE nombre = 'Marta' AND apellido = 'Ramírez'), 'VET-004-GT', 'Dermatología', 'Universidad Mariano Gálvez', 3), -- Añadido numero_colegiado
((SELECT id_empleado FROM empleados WHERE nombre = 'Luis' AND apellido = 'Soto'), 'VET-005-GT', 'Cardiología', 'Universidad Panamericana', 5); -- Añadido numero_colegiado

-- ================================================================
-- 3. Inserción de datos con dependencias (habitats, animales, eventos, alimentos, productos)
-- ================================================================

-- 3.1. Tabla: habitats (5 registros)
INSERT INTO habitats (nombre, id_tipo_habitat, ubicacion, capacidad_maxima, area_metros_cuadrados, fecha_construccion, estado, costo_mantenimiento_mensual) VALUES
('Jungla de Asia', (SELECT id_tipo_habitat FROM tipos_habitat WHERE nombre = 'Bosque Tropical'), ROW(-1.2921, 36.8219, 1795)::coordenadas, 3, 400.00, '2019-03-01', 'activo', 800.00),
('Pico Rocoso', (SELECT id_tipo_habitat FROM tipos_habitat WHERE nombre = 'Área Montañosa'), ROW(40.7128, -74.0060, 50)::coordenadas, 2, 250.00, '2021-06-10', 'activo', 500.00),
('Dunas del Sahara', (SELECT id_tipo_habitat FROM tipos_habitat WHERE nombre = 'Desierto'), ROW(25.0000, 15.0000, 200)::coordenadas, 5, 600.00, '2018-09-20', 'activo', 700.00),
('Sabana Africana Ext.', (SELECT id_tipo_habitat FROM tipos_habitat WHERE nombre = 'Pradera Abierta'), ROW(-2.0000, 35.0000, 1000)::coordenadas, 10, 1000.00, '2017-01-05', 'activo', 1500.00),
('Laguna de Coral', (SELECT id_tipo_habitat FROM tipos_habitat WHERE nombre = 'Recinto Acuático'), ROW(18.0000, -66.0000, 10)::coordenadas, 8, 300.00, '2022-02-28', 'mantenimiento', 600.00);


-- 3.2. Tabla: animales (5 registros)
INSERT INTO animales (nombre, id_especie, id_habitat, fecha_nacimiento, sexo, peso_actual, altura, numero_identificacion, origen, estado_salud) VALUES
('Raja', (SELECT id_especie FROM especies WHERE nombre_cientifico = 'Panthera tigris'), (SELECT id_habitat FROM habitats WHERE nombre = 'Jungla de Asia'), '2019-01-20', 'M', 200.00, 1.05, 'TGR-001', 'rescate', 'excelente'),
('Mei', (SELECT id_especie FROM especies WHERE nombre_cientifico = 'Ailuropoda melanoleuca'), (SELECT id_habitat FROM habitats WHERE nombre = 'Pico Rocoso'), '2020-07-05', 'F', 105.00, 1.50, 'PND-002', 'intercambio', 'bueno'),
('Zara', (SELECT id_especie FROM especies WHERE nombre_cientifico = 'Giraffa camelopardalis'), (SELECT id_habitat FROM habitats WHERE nombre = 'Sabana Africana Ext.'), '2018-03-15', 'F', 1100.00, 5.20, 'GRF-003', 'nacido_zoologico', 'excelente'),
('Jumbo', (SELECT id_especie FROM especies WHERE nombre_cientifico = 'Loxodonta africana'), (SELECT id_habitat FROM habitats WHERE nombre = 'Sabana Africana Ext.'), '2005-09-01', 'M', 4200.00, 3.00, 'ELF-004', 'rescate', 'regular'),
('Arachna', (SELECT id_especie FROM especies WHERE nombre_cientifico = 'Brachypelma hamorii'), (SELECT id_habitat FROM habitats WHERE nombre = 'Dunas del Sahara'), '2023-01-01', 'F', 0.03, 0.05, 'TAR-005', 'compra', 'bueno');

-- 3.3. Tabla: eventos (5 registros)
INSERT INTO eventos (nombre, descripcion, fecha_inicio, fecha_fin, horario_inicio, horario_fin, capacidad_maxima, precio_entrada, tipo_evento, estado, horario_complejo) VALUES
('Alimentación de Tigres', 'Observa cómo alimentan a los tigres.', '2025-07-01', '2025-07-01', '14:00:00', '14:30:00', 50, 7.50, 'educativo', 'programado', ROW('{2,4}', '14:00:00', '14:30:00', 30, 'diario')::horario_evento), -- Martes y Jueves
('Charla Panda Gigante', 'Aprende sobre la conservación del panda.', '2025-07-15', '2025-07-15', '11:00:00', '11:45:00', 40, 6.00, 'educativo', 'programado', ROW('{3}', '11:00:00', '11:45:00', 45, 'semanal')::horario_evento), -- Miércoles
('Noche de Safari Nocturno', 'Tour especial para ver animales nocturnos.', '2025-08-01', '2025-08-01', '20:00:00', '22:00:00', 20, 25.00, 'especial', 'programado', ROW('{5}', '20:00:00', '22:00:00', 120, 'mensual')::horario_evento), -- Viernes
('Taller de Arte Animal', 'Actividad creativa para niños inspirada en animales.', '2025-07-20', '2025-07-20', '10:00:00', '12:00:00', 15, 10.00, 'entretenimiento', 'programado', ROW('{6}', '10:00:00', '12:00:00', 120, 'semanal')::horario_evento), -- Sábado
('Día de Concienciación del Elefante', 'Evento para educar sobre la protección de elefantes.', '2025-08-12', '2025-08-12', '09:00:00', '17:00:00', 100, 0.00, 'especial', 'programado', ROW('{7}', '09:00:00', '17:00:00', 480, 'anual')::horario_evento); -- Domingo

-- 3.4. Tabla: alimentos (5 registros)
INSERT INTO alimentos (nombre, id_proveedor, tipo_alimento, info_nutricional, calorias_por_kg, proteinas_porcentaje, grasas_porcentaje, carbohidratos_porcentaje, costo_por_kg, fecha_vencimiento, stock_actual, stock_minimo) VALUES
('Carne de Res Magra', (SELECT id_proveedor FROM proveedores WHERE nombre_empresa = 'ZooFood S.A.'), 'carnivoro', ROW(1500, 20.00, 10.00, 0.00, 0.00, '{"hierro", "B12"}')::info_nutricional, 1500, 20.00, 10.00, 0.00, 8.50, '2025-07-15', 500, 100),
('Bambú Fresco', (SELECT id_proveedor FROM proveedores WHERE nombre_empresa = 'NutriZoo Supplies'), 'herbivoro', ROW(150, 1.00, 0.50, 10.00, 5.00, '{"fibra", "C"}')::info_nutricional, 150, 1.00, 0.50, 10.00, 2.00, '2025-06-10', 1000, 200),
('Pienso para Jirafas', (SELECT id_proveedor FROM proveedores WHERE nombre_empresa = 'ZooFood S.A.'), 'herbivoro', ROW(2500, 15.00, 5.00, 50.00, 10.00, '{"A", "D"}')::info_nutricional, 2500, 15.00, 5.00, 50.00, 4.75, '2025-12-31', 750, 150),
('Frutas y Verduras Mixtas', (SELECT id_proveedor FROM proveedores WHERE nombre_empresa = 'NutriZoo Supplies'), 'omnivoro', ROW(400, 2.00, 1.00, 20.00, 3.00, '{"C", "K"}')::info_nutricional, 400, 2.00, 1.00, 20.00, 3.00, '2025-06-07', 300, 50),
('Insectos Vivo', (SELECT id_proveedor FROM proveedores WHERE nombre_empresa = 'ZooFood S.A.'), 'carnivoro', ROW(1800, 30.00, 15.00, 5.00, 2.00, '{"proteina", "calcio"}')::info_nutricional, 1800, 30.00, 15.00, 5.00, 12.00, '2025-06-05', 200, 30);


-- 3.5. Tabla: productos (5 registros)
INSERT INTO productos (nombre, descripcion, precio, stock_actual, stock_minimo, categoria, id_proveedor, activo) VALUES
('Peluche de León', 'Peluche suave de tigre, ideal para niños.', 15.99, 100, 20, 'souvenir', (SELECT id_proveedor FROM proveedores WHERE nombre_empresa = 'EquipZoológico Ltda.'), TRUE),
('Libro Animales del Zoo', 'Libro educativo sobre las especies del zoológico.', 9.50, 50, 10, 'educativo', (SELECT id_proveedor FROM proveedores WHERE nombre_empresa = 'EquipZoológico Ltda.'), TRUE),
('Camiseta Panda', 'Camiseta con diseño de panda, varias tallas.', 22.00, 75, 15, 'ropa', (SELECT id_proveedor FROM proveedores WHERE nombre_empresa = 'EquipZoológico Ltda.'), TRUE),
('Kit de Semillas "Mi Jardín"', 'Kit para plantar flores que atraen abejas.', 8.75, 30, 5, 'educativo', (SELECT id_proveedor FROM proveedores WHERE nombre_empresa = 'EquipZoológico Ltda.'), TRUE),
('Mug con Logo del Zoo', 'Taza de café coleccionable con el logo del zoológico.', 12.00, 80, 20, 'souvenir', (SELECT id_proveedor FROM proveedores WHERE nombre_empresa = 'EquipZoológico Ltda.'), TRUE);

-- ================================================================
-- 4. Inserción de datos en tablas de cruce
-- ================================================================

-- 4.1. Tabla: animal_cuidador (5 registros)
INSERT INTO animal_cuidador (id_animal, id_cuidador, fecha_asignacion, es_cuidador_principal, notas) VALUES
((SELECT id_animal FROM animales WHERE numero_identificacion = 'TGR-001'), (SELECT id_cuidador FROM cuidadores WHERE especialidad = 'Felinos'), '2024-01-01', TRUE, 'Cuidadora principal, muy atenta a su dieta.'),
((SELECT id_animal FROM animales WHERE numero_identificacion = 'PND-002'), (SELECT id_cuidador FROM cuidadores WHERE especialidad = 'Mamíferos Grandes'), '2024-01-05', TRUE, 'Manejo cuidadoso, necesita paciencia.'),
((SELECT id_animal FROM animales WHERE numero_identificacion = 'GRF-003'), (SELECT id_cuidador FROM cuidadores WHERE especialidad = 'Mamíferos Grandes'), '2024-02-01', FALSE, 'Asistente en alimentación y limpieza.'),
((SELECT id_animal FROM animales WHERE numero_identificacion = 'ELF-004'), (SELECT id_cuidador FROM cuidadores WHERE especialidad = 'Mamíferos Grandes'), '2024-03-10', TRUE, 'Animal de manejo complejo, requiere experiencia.'),
((SELECT id_animal FROM animales WHERE numero_identificacion = 'TAR-005'), (SELECT id_cuidador FROM cuidadores WHERE especialidad = 'Reptiles'), '2024-04-01', TRUE, 'Ambiente controlado y seguro.');

-- 4.2. Tabla: animal_alimentacion (5 registros)
INSERT INTO animal_alimentacion (id_animal, id_alimento, id_cuidador, fecha_alimentacion, hora_alimentacion, cantidad_kg, observaciones) VALUES
((SELECT id_animal FROM animales WHERE numero_identificacion = 'TGR-001'), (SELECT id_alimento FROM alimentos WHERE nombre = 'Carne de Res Magra'), (SELECT id_cuidador FROM cuidadores WHERE especialidad = 'Felinos'), '2025-05-30', '14:00:00', 5.00, 'Comió todo con apetito.'),
((SELECT id_animal FROM animales WHERE numero_identificacion = 'PND-002'), (SELECT id_alimento FROM alimentos WHERE nombre = 'Bambú Fresco'), (SELECT id_cuidador FROM cuidadores WHERE especialidad = 'Mamíferos Grandes'), '2025-05-30', '09:00:00', 10.00, 'Consumió gran parte del bambú.'),
((SELECT id_animal FROM animales WHERE numero_identificacion = 'GRF-003'), (SELECT id_alimento FROM alimentos WHERE nombre = 'Pienso para Jirafas'), (SELECT id_cuidador FROM cuidadores WHERE especialidad = 'Mamíferos Grandes'), '2025-05-29', '10:30:00', 8.00, 'Dieta regular, buen estado.'),
((SELECT id_animal FROM animales WHERE numero_identificacion = 'ELF-004'), (SELECT id_alimento FROM alimentos WHERE nombre = 'Frutas y Verduras Mixtas'), (SELECT id_cuidador FROM cuidadores WHERE especialidad = 'Mamíferos Grandes'), '2025-05-29', '15:00:00', 20.00, 'Suplemento nutricional.'),
((SELECT id_animal FROM animales WHERE numero_identificacion = 'TAR-005'), (SELECT id_alimento FROM alimentos WHERE nombre = 'Insectos Vivo'), (SELECT id_cuidador FROM cuidadores WHERE especialidad = 'Reptiles'), '2025-05-31', '18:00:00', 0.01, 'Alimentación regular, sano.');

-- 4.3. Tabla: visitante_evento (5 registros)
INSERT INTO visitante_evento (id_visitante, id_evento, fecha_registro, precio_pagado, asistio, calificacion, comentarios) VALUES
((SELECT id_visitante FROM visitantes WHERE email = 'laura.m@email.com'), (SELECT id_evento FROM eventos WHERE nombre = 'Alimentación de Tigres'), '2025-05-20 10:00:00', 7.50, TRUE, 5, 'Muy interesante y educativo.'),
((SELECT id_visitante FROM visitantes WHERE email = 'diego.g@email.com'), (SELECT id_evento FROM eventos WHERE nombre = 'Charla Panda Gigante'), '2025-05-25 11:30:00', 6.00, TRUE, 4, 'Al niño le encantó el panda.'),
((SELECT id_visitante FROM visitantes WHERE email = 'sofia.r@email.com'), (SELECT id_evento FROM eventos WHERE nombre = 'Noche de Safari Nocturno'), '2025-06-01 19:00:00', 25.00, FALSE, NULL, 'No pudo asistir por un imprevisto.'),
((SELECT id_visitante FROM visitantes WHERE email = 'jorge.h@email.com'), (SELECT id_evento FROM eventos WHERE nombre = 'Taller de Arte Animal'), '2025-06-05 09:00:00', 10.00, TRUE, 5, 'Excelente actividad para mis nietos.'),
((SELECT id_visitante FROM visitantes WHERE email = 'isabel.f@email.com'), (SELECT id_evento FROM eventos WHERE nombre = 'Día de Concienciación del Elefante'), '2025-06-10 08:30:00', 0.00, TRUE, 4, 'Importante iniciativa, buena organización.');

-- 4.4. Tabla: habitat_mantenimiento (5 registros)
INSERT INTO habitat_mantenimiento (id_habitat, id_empleado, fecha_mantenimiento, tipo_mantenimiento, descripcion_trabajo, costo, tiempo_horas, completado) VALUES
((SELECT id_habitat FROM habitats WHERE nombre = 'Jungla de Asia'), (SELECT id_empleado FROM empleados WHERE email = 'marta.r@zoo.com'), '2025-05-01', 'limpieza', 'Limpieza profunda de la vegetación y suelos.', 150.00, 8.00, TRUE),
((SELECT id_habitat FROM habitats WHERE nombre = 'Pico Rocoso'), (SELECT id_empleado FROM empleados WHERE email = 'ana.l@zoo.com'), '2025-05-10', 'reparacion', 'Reparación de malla de seguridad.', 300.00, 12.00, TRUE),
((SELECT id_habitat FROM habitats WHERE nombre = 'Dunas del Sahara'), (SELECT id_empleado FROM empleados WHERE email = 'luis.s@zoo.com'), '2025-05-15', 'inspeccion', 'Inspección de sistemas de ventilación.', 80.00, 4.00, TRUE),
((SELECT id_habitat FROM habitats WHERE nombre = 'Sabana Africana Ext.'), (SELECT id_empleado FROM empleados WHERE email = 'juan.g@zoo.com'), '2025-05-20', 'mejora', 'Instalación de nuevos elementos de enriquecimiento.', 500.00, 20.00, FALSE),
((SELECT id_habitat FROM habitats WHERE nombre = 'Laguna de Coral'), (SELECT id_empleado FROM empleados WHERE email = 'pedro.d@zoo.com'), '2025-05-25', 'limpieza', 'Limpieza del filtro y calidad del agua.', 200.00, 10.00, TRUE);

-- 4.5. Tabla: venta_productos (5 registros)
INSERT INTO venta_productos (id_visitante, id_producto, cantidad, precio_unitario, fecha_venta, metodo_pago, descuento_aplicado) VALUES
((SELECT id_visitante FROM visitantes WHERE email = 'laura.m@email.com'), (SELECT id_producto FROM productos WHERE nombre = 'Peluche de León'), 1, 15.99, '2025-05-30 11:00:00', 'tarjeta', 0.00),
((SELECT id_visitante FROM visitantes WHERE email = 'diego.g@email.com'), (SELECT id_producto FROM productos WHERE nombre = 'Libro Animales del Zoo'), 1, 9.50, '2025-05-30 14:00:00', 'efectivo', 0.00),
((SELECT id_visitante FROM visitantes WHERE email = 'sofia.r@email.com'), (SELECT id_producto FROM productos WHERE nombre = 'Camiseta Panda'), 2, 22.00, '2025-05-28 16:30:00', 'tarjeta', 5.00), -- 5% de descuento
((SELECT id_visitante FROM visitantes WHERE email = 'jorge.h@email.com'), (SELECT id_producto FROM productos WHERE nombre = 'Mug con Logo del Zoo'), 3, 12.00, '2025-05-27 10:00:00', 'efectivo', 0.00),
((SELECT id_visitante FROM visitantes WHERE email = 'isabel.f@email.com'), (SELECT id_producto FROM productos WHERE nombre = 'Kit de Semillas "Mi Jardín"'), 1, 8.75, '2025-05-29 13:15:00', 'transferencia', 0.00);

-- 4.6. Tabla: horarios (5 registros)
INSERT INTO horarios (dia_semana, hora_inicio, hora_fin, tipo_actividad, descripcion, id_empleado, id_evento) VALUES
('lunes', '08:00:00', '16:00:00', 'Cuidado Animal', 'Rutina de cuidado y limpieza en hábitats.', (SELECT id_empleado FROM empleados WHERE email = 'marta.r@zoo.com'), NULL),
('martes', '09:00:00', '12:00:00', 'Revisión Veterinaria', 'Chequeos de salud programados.', (SELECT id_empleado FROM empleados WHERE email = 'pedro.d@zoo.com'), NULL),
('miercoles', '14:00:00', '14:30:00', 'Alimentación Pública', 'Evento de alimentación de Tigres.', NULL, (SELECT id_evento FROM eventos WHERE nombre = 'Alimentación de Tigres')),
('jueves', '10:00:00', '16:00:00', 'Mantenimiento de Infraestructura', 'Tareas de mantenimiento en áreas comunes.', (SELECT id_empleado FROM empleados WHERE email = 'luis.s@zoo.com'), NULL),
('viernes', '11:00:00', '11:45:00', 'Charla Educativa', 'Charla sobre la conservación del Panda.', NULL, (SELECT id_evento FROM eventos WHERE nombre = 'Charla Panda Gigante'));