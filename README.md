# Peluzoo - Sistema de Gestión para Zoológicos

## Equipo 👥

- Iris Ayala
- Gabriel Bran
- David Dominguez
- Jonathan Díaz
- Anggie Quezada

## Requisitos 📋
![Docker](https://img.shields.io/badge/Docker-✓-blue?logo=docker)
![Python](https://img.shields.io/badge/Python-3.13+-green?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue?logo=postgresql)
- Docker 🐳
- Python 3.13+ 🐍
- pip 📦

## Pasos para iniciar el proyecto

> **Requisitos:** tener instalado Docker, Python y pip antes de comenzar.


1. **Clona el repositorio**
   ```
   git clone https://github.com/AleWWH1104/Proyecto4_BD.git
   ```

2. **Entra en el directorio del proyecto**
   ```
   cd Proyecto4_BD
   ```

3. **Crea un entorno virtual**
   ```
   python -m venv venv
   ```

4. **Activa el entorno virtual**
   ```
   venv\Scripts\activate
   ```
   > Si usas Linux/Mac, el comando es:  
   > `source venv/Scripts/activate`

5. **Instala las dependencias**
   ```
   pip install -r requirements.txt
   ```

6. **Inicia los servicios con Docker Compose**
   ```
   docker-compose up -d
   ```

7. **Ejecuta la aplicación Streamlit**
   ```
   streamlit run .\app\streamlitview\Inicio.py
   ```
   > Si usas Linux/Mac, el comando es:  
   > `streamlit run ./app/streamlitview/Inicio.py`

**Abre la aplicación en tu navegador:** http://localhost:8501 después de iniciar Streamlit (Si es otro puerto abrir en ese)
---


## Uso 🖥️

Accede a los módulos principales desde el menú lateral:

- 🏠 **Inicio**: Dashboard resumen
- 🐾 **Animales**: Registro y seguimiento
- 🌿 **Hábitats**: Gestión de espacios
- 🎪 **Eventos**: Programación y asistencia
- 📈 **Reportes**: Generación de análisis
- 📊 **Vistas**: Consultas predefinidas


---

# ESQUEMA DE BASE DE DATOS PARA ZOOLÓGICO - EXPLICACIÓN

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
