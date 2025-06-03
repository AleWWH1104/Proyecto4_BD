# ESQUEMA DE BASE DE DATOS PARA ZOOLÓGICO - METADATOS TÉCNICOS

## ESTRUCTURA PRINCIPAL
- Tipos personalizados: 15 enums + 5 tipos compuestos
- Tablas: 16 principales + 5 tablas de relación
- Triggers: 3 (automatización crítica)
- Funciones: 4 (lógica de reportes)
- Vistas: 3 (consultas complejas predefinidas)

## TABLAS CLAVE Y RELACIONES
1. especies <-(1:N)- animales -(N:1)-> habitats
2. empleados <-(1:1)- [cuidadores, veterinarios]
3. animales <-(N:M)-> cuidadores (vía animal_cuidador)
4. animales <-(N:M)-> alimentos (vía animal_alimentacion)
5. visitantes <-(N:M)-> eventos (vía visitante_evento)
6. visitantes <-(N:M)-> productos (vía venta_productos)

## TRIGGERS CRÍTICOS
1. trigger_asignar_cuidadores (AFTER INSERT en animales)
   - Lógica: 
        IF especie = felino THEN asignar cuidador_especialidad='Grandes felinos'
        ELSE IF especie = ave THEN asignar cuidador_especialidad='Aves exóticas'
        ELSE asignar 'Generalista'
   - Orden: Años experiencia DESC

2. trigger_actualizar_stock_producto (AFTER INSERT en venta_productos)
   - Acción: 
        UPDATE productos SET stock_actual = stock_actual - NEW.cantidad
        IF stock_actual < stock_minimo THEN WARNING

3. trigger_verificar_capacidad_habitat (BEFORE INSERT/UPDATE en animales)
   - Validación: 
        IF COUNT(animales_en_habitat) >= capacidad_maxima THEN ERROR

## FUNCIONES DE REPORTES
1. reporte_ventas_periodo(fecha_inicio, fecha_fin)
   - Salida: 
        categoría_producto, 
        total_ventas, 
        producto_mas_vendido, 
        metodo_pago_preferido

2. estadisticas_ocupacion_habitats()
   - Salida: 
        id_habitat, 
        %_ocupacion, 
        estado_capacidad (Vacío/Bajo/Normal/Lleno)

3. calcular_costo_alimentacion_animal(id_animal, fecha_inicio, fecha_fin)
   - Salida: 
        costo_total, 
        kg_consumidos, 
        num_alimentaciones

## VISTAS COMPLEJAS
1. vista_financiera_mensual
   - Columnas clave: 
        ingresos_totales, 
        gastos_totales (salarios + mantenimiento + alimentos), 
        balance_mensual

2. vista_conservacion
   - Filtro: especies en peligro (estado_conservacion IN ('peligro_critico','peligro','vulnerable'))
   - Datos: 
        cantidad_en_zoo, 
        cuidadores_asignados, 
        condiciones_habitat

3. vista_control_animal
   - Datos consolidados: 
        animal + especie + habitat + cuidador_principal + ultima_alimentacion

## RESTRICCIONES CLAVE
- UNIQUE: numero_colegiado (veterinarios), nombre_cientifico (especies)
- CHECK: 
    capacidad_maxima > 0, 
    stock_actual >= 0, 
    salario >= 0
- FK: Todas las relaciones están aseguradas con ON UPDATE/DELETE policies

## TIPOS COMPUESTOS NOTABLES
1. coordenadas: (latitud, longitud, altitud)
2. info_nutricional: (calorías, proteínas, grasas...)
3. horario_evento: (días_semana[], hora_inicio, frecuencia)

## PATRONES DE DISEÑO
- Herencia: cuidadores/veterinarios → empleados (tablas separadas)
- Auditoría implícita: Triggers llevan registro de acciones críticas
- Normalización: Datos repetidos minimizados (ej: info_nutricional en tipo compuesto)
