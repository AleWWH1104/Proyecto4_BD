-- Vista Financiera Mensual
CREATE OR REPLACE VIEW vista_financiera_mensual AS
SELECT 
    meses.mes_year AS mes,
    
    -- Ingresos
    ROUND(COALESCE(ingresos_eventos.total, 0), 2) AS ingresos_eventos,
    ROUND(COALESCE(ingresos_ventas.total, 0), 2) AS ingresos_ventas,
    
    -- Gastos
    ROUND(COALESCE(costos_mantenimiento.total, 0), 2) AS costos_mantenimiento,
    ROUND(COALESCE(gastos_tratamientos.total, 0), 2) AS gastos_tratamientos,
    ROUND(COALESCE(costos_alimentos.total, 0), 2) AS costos_alimentos,
    ROUND(COALESCE(costos_salarios.total, 0), 2) AS costos_salarios,
    
    -- Totales
    ROUND(COALESCE(ingresos_eventos.total, 0) + COALESCE(ingresos_ventas.total, 0), 2) AS ingresos_totales,
    ROUND(COALESCE(costos_mantenimiento.total, 0) + COALESCE(gastos_tratamientos.total, 0) + 
          COALESCE(costos_alimentos.total, 0) + COALESCE(costos_salarios.total, 0), 2) AS gastos_totales,
    
    -- Balance
    ROUND((COALESCE(ingresos_eventos.total, 0) + COALESCE(ingresos_ventas.total, 0)) -
          (COALESCE(costos_mantenimiento.total, 0) + COALESCE(gastos_tratamientos.total, 0) + 
           COALESCE(costos_alimentos.total, 0) + COALESCE(costos_salarios.total, 0)), 2) AS balance_mensual

FROM (
    -- Generar todos los meses que tienen datos
    SELECT DISTINCT TO_CHAR(fecha_registro, 'YYYY-MM') AS mes_year
    FROM visitante_evento
    UNION
    SELECT DISTINCT TO_CHAR(fecha_venta, 'YYYY-MM') AS mes_year
    FROM venta_productos
    UNION
    SELECT DISTINCT TO_CHAR(fecha_mantenimiento, 'YYYY-MM') AS mes_year
    FROM habitat_mantenimiento
    UNION
    SELECT DISTINCT TO_CHAR(fecha_alimentacion, 'YYYY-MM') AS mes_year
    FROM animal_alimentacion
) meses

LEFT JOIN (
    SELECT 
        TO_CHAR(fecha_registro, 'YYYY-MM') AS mes_year,
        SUM(precio_pagado) AS total
    FROM visitante_evento
    GROUP BY TO_CHAR(fecha_registro, 'YYYY-MM')
) ingresos_eventos ON meses.mes_year = ingresos_eventos.mes_year

LEFT JOIN (
    SELECT 
        TO_CHAR(fecha_venta, 'YYYY-MM') AS mes_year,
        SUM(cantidad * precio_unitario * (1 - COALESCE(descuento_aplicado, 0)/100)) AS total
    FROM venta_productos
    GROUP BY TO_CHAR(fecha_venta, 'YYYY-MM')
) ingresos_ventas ON meses.mes_year = ingresos_ventas.mes_year

LEFT JOIN (
    SELECT 
        TO_CHAR(fecha_mantenimiento, 'YYYY-MM') AS mes_year,
        SUM(costo) AS total
    FROM habitat_mantenimiento
    GROUP BY TO_CHAR(fecha_mantenimiento, 'YYYY-MM')
) costos_mantenimiento ON meses.mes_year = costos_mantenimiento.mes_year

LEFT JOIN (
    SELECT 
        TO_CHAR(aa.fecha_alimentacion, 'YYYY-MM') AS mes_year,
        SUM(tm.costo_base) AS total
    FROM tratamientos_medicos tm
    JOIN animal_alimentacion aa ON tm.id_tratamiento = aa.id_alimento
    GROUP BY TO_CHAR(aa.fecha_alimentacion, 'YYYY-MM')
) gastos_tratamientos ON meses.mes_year = gastos_tratamientos.mes_year

LEFT JOIN (
    SELECT 
        TO_CHAR(aa.fecha_alimentacion, 'YYYY-MM') AS mes_year,
        SUM(aa.cantidad_kg * al.costo_por_kg) AS total
    FROM animal_alimentacion aa
    JOIN alimentos al ON aa.id_alimento = al.id_alimento
    GROUP BY TO_CHAR(aa.fecha_alimentacion, 'YYYY-MM')
) costos_alimentos ON meses.mes_year = costos_alimentos.mes_year

LEFT JOIN (
    SELECT 
        TO_CHAR(CURRENT_DATE, 'YYYY-MM') AS mes_year,
        SUM(salario) AS total
    FROM empleados 
    WHERE activo = true
    GROUP BY TO_CHAR(CURRENT_DATE, 'YYYY-MM')
) costos_salarios ON meses.mes_year = costos_salarios.mes_year

ORDER BY meses.mes_year DESC;

--Vista de Conservación y Especies Amenazadas (Priorización de esfuerzos de conservación)
CREATE OR REPLACE VIEW vista_conservacion AS
SELECT 
    e.id_especie,
    e.nombre_cientifico,
    e.nombre_comun,
    e.estado_conservacion,
    COUNT(a.id_animal) AS cantidad_en_zoo,
    e.esperanza_vida,
    h.nombre AS habitat_principal,
    th.temperatura_min || '°C - ' || th.temperatura_max || '°C' AS rango_temperatura,
    th.humedad_min || '% - ' || th.humedad_max || '%' AS rango_humedad,
    COUNT(DISTINCT ac.id_cuidador) AS cuidadores_asignados,
    COUNT(DISTINCT v.id_veterinario) AS veterinarios_especializados
FROM 
    especies e
LEFT JOIN 
    animales a ON e.id_especie = a.id_especie
LEFT JOIN 
    habitats h ON a.id_habitat = h.id_habitat
LEFT JOIN 
    tipos_habitat th ON h.id_tipo_habitat = th.id_tipo_habitat
LEFT JOIN 
    animal_cuidador ac ON a.id_animal = ac.id_animal
LEFT JOIN 
    veterinarios v ON EXISTS (
        SELECT 1 FROM animal_alimentacion aa 
        WHERE aa.id_animal = a.id_animal 
        AND aa.id_cuidador = v.id_veterinario
    )
WHERE 
    e.estado_conservacion IN ('peligro_critico', 'peligro', 'vulnerable')
GROUP BY 
    e.id_especie, e.nombre_cientifico, e.nombre_comun, e.estado_conservacion, 
    e.esperanza_vida, h.nombre, th.temperatura_min, th.temperatura_max, 
    th.humedad_min, th.humedad_max
ORDER BY 
    CASE e.estado_conservacion
        WHEN 'peligro_critico' THEN 1
        WHEN 'peligro' THEN 2
        WHEN 'vulnerable' THEN 3
        ELSE 4
    END,
    COUNT(a.id_animal) DESC;

--Vista de Control Animal (Información clave sobre animales y su cuidado)
CREATE OR REPLACE VIEW vista_control_animal AS
SELECT 
    a.id_animal,
    a.nombre AS nombre_animal,
    e.nombre_comun AS especie,
    e.estado_conservacion,
    h.nombre AS habitat,
    th.nombre AS tipo_habitat,
    a.estado_salud,
    a.peso_actual,
    a.fecha_nacimiento,
    EXTRACT(YEAR FROM AGE(CURRENT_DATE, a.fecha_nacimiento)) AS edad_aproximada,
    c.nombre || ' ' || c.apellido AS cuidador_principal,
    COUNT(DISTINCT ac.id_cuidador) AS total_cuidadores_asignados,
    (SELECT MAX(fecha_alimentacion) 
     FROM animal_alimentacion 
     WHERE id_animal = a.id_animal) AS ultima_alimentacion_fecha,
    (SELECT SUM(cantidad_kg) 
     FROM animal_alimentacion 
     WHERE id_animal = a.id_animal) AS total_alimento_kg
FROM 
    animales a
JOIN 
    especies e ON a.id_especie = e.id_especie
JOIN 
    habitats h ON a.id_habitat = h.id_habitat
JOIN 
    tipos_habitat th ON h.id_tipo_habitat = th.id_tipo_habitat
LEFT JOIN 
    animal_cuidador ac ON a.id_animal = ac.id_animal AND ac.es_cuidador_principal = TRUE
LEFT JOIN 
    cuidadores cu ON ac.id_cuidador = cu.id_cuidador
LEFT JOIN 
    empleados c ON cu.id_cuidador = c.id_empleado
GROUP BY 
    a.id_animal, a.nombre, e.nombre_comun, e.estado_conservacion, h.nombre, 
    th.nombre, a.estado_salud, a.peso_actual, a.fecha_nacimiento, c.nombre, c.apellido;