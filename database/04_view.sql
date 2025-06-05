-- Vista Financiera Mensual Mejorada
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
           COALESCE(costos_alimentos.total, 0) + COALESCE(costos_salarios.total, 0)), 2) AS balance_mensual,

    -- Métricas adicionales
    COALESCE(eventos_realizados.cantidad, 0) AS eventos_realizados,
    COALESCE(ventas_realizadas.cantidad, 0) AS ventas_realizadas,
    CASE 
        WHEN (COALESCE(ingresos_eventos.total, 0) + COALESCE(ingresos_ventas.total, 0)) > 0 THEN
            ROUND(((COALESCE(ingresos_eventos.total, 0) + COALESCE(ingresos_ventas.total, 0)) -
                 (COALESCE(costos_mantenimiento.total, 0) + COALESCE(gastos_tratamientos.total, 0) + 
                  COALESCE(costos_alimentos.total, 0) + COALESCE(costos_salarios.total, 0)) / 
                 (COALESCE(ingresos_eventos.total, 0) + COALESCE(ingresos_ventas.total, 0)) * 100, 2)
        ELSE 0 
    END AS margen_beneficio

FROM (
    -- Generar todos los meses que tienen datos de forma más eficiente
    SELECT DISTINCT TO_CHAR(fecha, 'YYYY-MM') AS mes_year
    FROM (
        SELECT fecha_registro AS fecha FROM visitante_evento
        UNION ALL
        SELECT fecha_venta FROM venta_productos
        UNION ALL
        SELECT fecha_mantenimiento FROM habitat_mantenimiento
        UNION ALL
        SELECT fecha_alimentacion FROM animal_alimentacion
    ) todas_fechas
) meses

-- Ingresos por eventos
LEFT JOIN (
    SELECT 
        TO_CHAR(fecha_registro, 'YYYY-MM') AS mes_year,
        SUM(precio_pagado) AS total,
        COUNT(*) AS cantidad
    FROM visitante_evento
    WHERE asistio = TRUE
    GROUP BY TO_CHAR(fecha_registro, 'YYYY-MM')
) ingresos_eventos ON meses.mes_year = ingresos_eventos.mes_year

-- Ingresos por ventas
LEFT JOIN (
    SELECT 
        TO_CHAR(fecha_venta, 'YYYY-MM') AS mes_year,
        SUM(cantidad * precio_unitario * (1 - COALESCE(descuento_aplicado, 0)/100)) AS total,
        COUNT(*) AS cantidad
    FROM venta_productos
    GROUP BY TO_CHAR(fecha_venta, 'YYYY-MM')
) ingresos_ventas ON meses.mes_year = ingresos_ventas.mes_year

-- Costos de mantenimiento de hábitats
LEFT JOIN (
    SELECT 
        TO_CHAR(fecha_mantenimiento, 'YYYY-MM') AS mes_year,
        SUM(costo) AS total
    FROM habitat_mantenimiento
    WHERE completado = TRUE
    GROUP BY TO_CHAR(fecha_mantenimiento, 'YYYY-MM')
) costos_mantenimiento ON meses.mes_year = costos_mantenimiento.mes_year

-- Gastos por tratamientos médicos (corregido)
LEFT JOIN (
    SELECT 
        TO_CHAR(fecha_alimentacion, 'YYYY-MM') AS mes_year,
        SUM(tm.costo_base) AS total
    FROM tratamientos_medicos tm
    JOIN animal_alimentacion aa ON tm.id_tratamiento = aa.id_tratamiento
    GROUP BY TO_CHAR(fecha_alimentacion, 'YYYY-MM')
) gastos_tratamientos ON meses.mes_year = gastos_tratamientos.mes_year

-- Costos de alimentos
LEFT JOIN (
    SELECT 
        TO_CHAR(aa.fecha_alimentacion, 'YYYY-MM') AS mes_year,
        SUM(aa.cantidad_kg * al.costo_por_kg) AS total
    FROM animal_alimentacion aa
    JOIN alimentos al ON aa.id_alimento = al.id_alimento
    GROUP BY TO_CHAR(aa.fecha_alimentacion, 'YYYY-MM')
) costos_alimentos ON meses.mes_year = costos_alimentos.mes_year

-- Costos de salarios (mejorado para calcular por mes)
LEFT JOIN (
    SELECT 
        TO_CHAR(fecha_contratacion, 'YYYY-MM') AS mes_year,
        SUM(salario) AS total
    FROM empleados 
    WHERE activo = true
    GROUP BY TO_CHAR(fecha_contratacion, 'YYYY-MM')
) costos_salarios ON meses.mes_year = costos_salarios.mes_year

-- Contador de eventos realizados
LEFT JOIN (
    SELECT 
        TO_CHAR(fecha_inicio, 'YYYY-MM') AS mes_year,
        COUNT(*) AS cantidad
    FROM eventos
    WHERE estado = 'finalizado'
    GROUP BY TO_CHAR(fecha_inicio, 'YYYY-MM')
) eventos_realizados ON meses.mes_year = eventos_realizados.mes_year

-- Contador de ventas realizadas
LEFT JOIN (
    SELECT 
        TO_CHAR(fecha_venta, 'YYYY-MM') AS mes_year,
        COUNT(*) AS cantidad
    FROM venta_productos
    GROUP BY TO_CHAR(fecha_venta, 'YYYY-MM')
) ventas_realizadas ON meses.mes_year = ventas_realizadas.mes_year

ORDER BY meses.mes_year DESC;