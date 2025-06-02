--Triggers
-- TRIGGER: Asignar Cuidadores a Animales Automáticamente
CREATE OR REPLACE FUNCTION asignar_cuidadores_automaticos()
RETURNS TRIGGER AS $$
DECLARE
    v_cuidador_principal_id INTEGER;
    v_especialidad_cuidador TEXT;
    v_especialidad_requerida TEXT;
BEGIN
    -- Obtener especialidad requerida para la especie del nuevo animal
    SELECT 
        CASE 
            WHEN e.clase = 'Mammalia' AND e.orden = 'Carnivora' THEN 'Grandes felinos'
            WHEN e.clase = 'Aves' THEN 'Aves exóticas'
            WHEN e.familia = 'Ursidae' THEN 'Osos'
            ELSE 'Generalista'
        END INTO v_especialidad_requerida
    FROM especies e
    WHERE e.id_especie = NEW.id_especie;
    
    -- Buscar cuidador principal disponible con la especialidad requerida
    SELECT c.id_cuidador INTO v_cuidador_principal_id
    FROM cuidadores c
    JOIN empleados e ON c.id_cuidador = e.id_empleado
    WHERE c.especialidad = v_especialidad_requerida
    AND e.activo = TRUE
    ORDER BY c.años_experiencia DESC
    LIMIT 1;
    
    -- Si no hay cuidador con especialidad exacta, buscar generalista
    IF v_cuidador_principal_id IS NULL THEN
        SELECT c.id_cuidador INTO v_cuidador_principal_id
        FROM cuidadores c
        JOIN empleados e ON c.id_cuidador = e.id_empleado
        WHERE c.especialidad = 'Generalista'
        AND e.activo = TRUE
        ORDER BY c.años_experiencia DESC
        LIMIT 1;
    END IF;
    
    -- Asignar cuidador principal al animal
    IF v_cuidador_principal_id IS NOT NULL THEN
        INSERT INTO animal_cuidador (
            id_animal,
            id_cuidador,
            fecha_asignacion,
            es_cuidador_principal
        ) VALUES (
            NEW.id_animal,
            v_cuidador_principal_id,
            CURRENT_DATE,
            TRUE
        );
        
        RAISE NOTICE 'Asignado cuidador principal % al animal %', v_cuidador_principal_id, NEW.id_animal;
    ELSE
        RAISE WARNING 'No se encontró cuidador disponible para asignar al animal %', NEW.id_animal;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para ejecutar la función al insertar un nuevo animal
CREATE TRIGGER trigger_asignar_cuidadores
AFTER INSERT ON animales
FOR EACH ROW
EXECUTE FUNCTION asignar_cuidadores_automaticos();


-- TRIGGER: Actualizar stock de productos automáticamente en ventas
CREATE OR REPLACE FUNCTION actualizar_stock_producto()
RETURNS TRIGGER AS $$
BEGIN
    -- Reducir stock del producto vendido
    UPDATE productos 
    SET stock_actual = stock_actual - NEW.cantidad,
        updated_at = NOW()
    WHERE id_producto = NEW.id_producto;
    
    -- Verificar si el stock queda por debajo del mínimo
    IF (SELECT stock_actual FROM productos WHERE id_producto = NEW.id_producto) < 
       (SELECT stock_minimo FROM productos WHERE id_producto = NEW.id_producto) THEN
        
        RAISE WARNING 'ALERTA: El producto % está por debajo del stock mínimo', NEW.id_producto;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_actualizar_stock_producto
    AFTER INSERT ON venta_productos
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_stock_producto();


-- TRIGGER: Verificar capacidad máxima del hábitat antes de asignar animal
CREATE OR REPLACE FUNCTION verificar_capacidad_habitat()
RETURNS TRIGGER AS $$
DECLARE
    animales_actuales INTEGER;
    capacidad_max INTEGER;
BEGIN
    -- Obtener capacidad máxima del hábitat
    SELECT capacidad_maxima 
    INTO capacidad_max
    FROM habitats 
    WHERE id_habitat = NEW.id_habitat;
    
    -- Contar animales actuales en el hábitat
    SELECT COUNT(*) 
    INTO animales_actuales
    FROM animales 
    WHERE id_habitat = NEW.id_habitat;
    
    -- Verificar si se excede la capacidad
    IF animales_actuales >= capacidad_max THEN
        RAISE EXCEPTION 'No se puede asignar el animal. Hábitat % ha alcanzado su capacidad máxima de % animales', 
            NEW.id_habitat, capacidad_max;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_verificar_capacidad_habitat
    BEFORE INSERT OR UPDATE ON animales
    FOR EACH ROW
    WHEN (NEW.id_habitat IS NOT NULL)
    EXECUTE FUNCTION verificar_capacidad_habitat();