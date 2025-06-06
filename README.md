# Proyecto4_BD

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
---

