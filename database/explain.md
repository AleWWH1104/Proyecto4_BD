# ESQUEMA DE BASE DE DATOS PARA ZOOLÓGICO - EXPLICACIÓN PARA HUMANOS

## ¿Qué hace este sistema?
Gestiona TODAS las operaciones de un zoológico moderno:
- Animales y sus cuidados
- Hábitats y mantenimiento
- Empleados (cuidadores, veterinarios)
- Visitantes y eventos
- Productos y ventas
- Finanzas y reportes

## Partes clave que debes entender:

### 1. Animales y sus cuidados
- Cada animal tiene:
  - Especie (ej: "Panthera leo")
  - Hábitat asignado (con capacidad máxima)
  - Cuidador principal (asignado automáticamente)
  - Registro de alimentación (qué come, cuándo, cuánto)
  - Estado de salud (de "excelente" a "crítico")

### 2. Hábitats
- Cada hábitat tiene:
  - Ubicación GPS (latitud/longitud)
  - Capacidad máxima de animales
  - Estado ("activo", "en mantenimiento")
  - Costo mensual de mantenimiento

### 3. Sistema Automático
- Al agregar un NUEVO animal:
  - Se verifica que el hábitat tenga espacio (si no, muestra error)
  - Se asigna automáticamente un cuidador especializado:
    - Felinos -> Cuidadores de "Grandes felinos"
    - Aves -> Cuidadores de "Aves exóticas"
    - Otros -> Cuidadores "Generalistas"

### 4. Tienda y Ventas
- Cuando se vende un producto:
  - El stock baja automáticamente
  - Si quedan pocas unidades, el sistema avisa
- Reportes de ventas muestran:
  - Productos más vendidos
  - Métodos de pago preferidos
  - Ingresos por categoría

### 5. Reportes Importantes
- Financiero mensual:
  - Ingresos (ventas + eventos)
  - Gastos (salarios + comida + mantenimiento)
  - Balance final (ganancias/pérdidas)
  
- Estadísticas de hábitats:
  - % de ocupación
  - Costo de mantenimiento
  - Estado de capacidad ("Vacío", "Lleno", etc)

### 6. Datos Curiosos
- Los veterinarios tienen número de colegiado único
- Los alimentos tienen info nutricional detallada
- Los eventos tienen horarios complejos (ej: "todos los martes de 10am a 12pm")

## ¿Cómo usar el sistema?
- Para agregar animal: Insertar en tabla "animales"
- Para registrar venta: Insertar en "venta_productos"
- Para ver reportes: Usar las funciones:
  - reporte_ventas_periodo()
  - estadisticas_ocupacion_habitats()
  - vista_financiera_mensual (es una vista)

## ¡Importante!
- Los hábitats NO pueden superar su capacidad máxima
- Los cuidadores principales se asignan AUTOMÁTICAMENTE
- El stock de productos se actualiza SOLO al vender
