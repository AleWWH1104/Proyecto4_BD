# Peluzoo - Sistema de Gestión para Zoológicos



## Descripción 📝

Sistema completo para administrar todos los aspectos de un zoológico moderno:

- 🐘 Gestión de animales y hábitats
- 📅 Eventos y visitantes
- 💰 Control financiero
- 📊 Reportes avanzados

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

## Características Clave ✨

✅ Automatización de cuidados animales  
✅ Control de capacidad de hábitats  
✅ Exportación a CSV

## Equipo 👥

- Iris Ayala
- Gabriel Bran
- David Dominguez
- Jonathan Díaz
- Anggie Quezada

---

