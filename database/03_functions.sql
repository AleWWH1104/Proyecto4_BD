--FUNCIÓN: Generar reporte de ventas por período
CREATE OR REPLACE FUNCTION reporte_ventas_periodo(
    p_fecha_inicio DATE DEFAULT CURRENT_DATE - INTERVAL '30 days',
    p_fecha_fin DATE DEFAULT CURRENT_DATE
)
RETURNS TABLE (
    categoria_producto categoria_producto_enum,
    total_productos_vendidos INTEGER,
    ingresos_totales DECIMAL(12,2),
    producto_mas_vendido TEXT,
    cantidad_mas_vendida INTEGER,
    metodo_pago_preferido metodo_pago_enum
) AS $$
BEGIN
    RETURN QUERY
    WITH ventas_resumen AS (
        SELECT 
            p.categoria,
            p.nombre as nombre_producto,
            SUM(vp.cantidad) as total_cantidad,
            SUM(vp.cantidad * vp.precio_unitario) as total_ingresos,
            vp.metodo_pago
        FROM venta_productos vp
        INNER JOIN productos p ON vp.id_producto = p.id_producto
        WHERE DATE(vp.fecha_venta) BETWEEN p_fecha_inicio AND p_fecha_fin
        GROUP BY p.categoria, p.nombre, vp.metodo_pago
    ),
    producto_top AS (
        SELECT DISTINCT ON (categoria)
            categoria,
            nombre_producto,
            total_cantidad
        FROM ventas_resumen
        ORDER BY categoria, total_cantidad DESC
    ),
    metodo_pago_top AS (
        SELECT DISTINCT ON (categoria)
            categoria,
            metodo_pago
        FROM ventas_resumen
        ORDER BY categoria, total_cantidad DESC
    )
    SELECT 
        vr.categoria,
        SUM(vr.total_cantidad)::INTEGER as total_productos_vendidos,
        SUM(vr.total_ingresos)::DECIMAL(12,2) as ingresos_totales,
        pt.nombre_producto as producto_mas_vendido,
        pt.total_cantidad::INTEGER as cantidad_mas_vendida,
        mpt.metodo_pago as metodo_pago_preferido
    FROM ventas_resumen vr
    LEFT JOIN producto_top pt ON vr.categoria = pt.categoria
    LEFT JOIN metodo_pago_top mpt ON vr.categoria = mpt.categoria
    GROUP BY vr.categoria, pt.nombre_producto, pt.total_cantidad, mpt.metodo_pago
    ORDER BY ingresos_totales DESC;
END;
$$ LANGUAGE plpgsql;

--FUNCIÓN: Obtener estadísticas de ocupación de hábitats
CREATE OR REPLACE FUNCTION estadisticas_ocupacion_habitats()
RETURNS TABLE (
    id_habitat INTEGER,
    nombre_habitat TEXT,
    tipo_habitat TEXT,
    capacidad_maxima INTEGER,
    animales_actuales INTEGER,
    porcentaje_ocupacion DECIMAL(5,2),
    estado_capacidad TEXT,
    costo_mantenimiento_mensual DECIMAL(10,2)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        h.id_habitat,
        h.nombre as nombre_habitat,
        th.nombre as tipo_habitat,
        h.capacidad_maxima,
        COUNT(a.id_animal)::INTEGER as animales_actuales,
        CASE 
            WHEN h.capacidad_maxima > 0 THEN 
                ROUND((COUNT(a.id_animal) * 100.0 / h.capacidad_maxima), 2)
            ELSE 0
        END::DECIMAL(5,2) as porcentaje_ocupacion,
        CASE 
            WHEN COUNT(a.id_animal) = 0 THEN 'VACÍO'
            WHEN COUNT(a.id_animal) < h.capacidad_maxima * 0.7 THEN 'BAJA OCUPACIÓN'
            WHEN COUNT(a.id_animal) < h.capacidad_maxima THEN 'OCUPACIÓN NORMAL'
            ELSE 'CAPACIDAD MÁXIMA'
        END as estado_capacidad,
        h.costo_mantenimiento_mensual
    FROM habitats h
    LEFT JOIN tipos_habitat th ON h.id_tipo_habitat = th.id_tipo_habitat
    LEFT JOIN animales a ON h.id_habitat = a.id_habitat
    GROUP BY h.id_habitat, h.nombre, th.nombre, h.capacidad_maxima, h.costo_mantenimiento_mensual
    ORDER BY porcentaje_ocupacion DESC;
END;
$$ LANGUAGE plpgsql;

-- FUNCIÓN: Calcular costo total de alimentación por animal en un período
CREATE OR REPLACE FUNCTION calcular_costo_alimentacion_animal(
    p_id_animal INTEGER,
    p_fecha_inicio DATE DEFAULT CURRENT_DATE - INTERVAL '30 days',
    p_fecha_fin DATE DEFAULT CURRENT_DATE
)
RETURNS TABLE (
    id_animal INTEGER,
    nombre_animal TEXT,
    especie TEXT,
    total_costo DECIMAL(12,2),
    total_kg_consumidos DECIMAL(10,2),
    numero_alimentaciones INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        a.id_animal,
        a.nombre,
        e.nombre_comun as especie,
        COALESCE(SUM(aa.cantidad_kg * al.costo_por_kg), 0)::DECIMAL(12,2) as total_costo,
        COALESCE(SUM(aa.cantidad_kg), 0)::DECIMAL(10,2) as total_kg_consumidos,
        COUNT(aa.id)::INTEGER as numero_alimentaciones
    FROM animales a
    LEFT JOIN especies e ON a.id_especie = e.id_especie
    LEFT JOIN animal_alimentacion aa ON a.id_animal = aa.id_animal 
        AND aa.fecha_alimentacion BETWEEN p_fecha_inicio AND p_fecha_fin
    LEFT JOIN alimentos al ON aa.id_alimento = al.id_alimento
    WHERE a.id_animal = p_id_animal
    GROUP BY a.id_animal, a.nombre, e.nombre_comun;
END;
$$ LANGUAGE plpgsql;