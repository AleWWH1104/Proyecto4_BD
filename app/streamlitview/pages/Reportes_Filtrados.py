
import sys
import os

# Añade el root del proyecto al path (sube 2 niveles desde este archivo)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import streamlit as st
from database import get_db
from models import Especie, TipoHabitat, Habitat # Asegúrate de que estos modelos estén definidos
from crud import crud # Necesario para obtener listas de opciones para los filtros
from reports.reports import (
    get_reporte_animales_por_habitat,
    get_reporte_eventos_y_asistencia,
    get_reporte_alimentos_y_proveedores
)
from datetime import date, time
import pandas as pd
import io

# --- Opciones predefinidas para selectbox y filtros ---
ORIGEN_OPTIONS = ['nacido_zoologico', 'rescate', 'intercambio', 'compra']
ESTADO_SALUD_OPTIONS = ['excelente', 'bueno', 'regular', 'malo', 'critico']
SEXO_OPTIONS = ["M", "F", "Desconocido"]
ESTADO_HABITAT_OPTIONS = ["activo", "inactivo", "mantenimiento"] # Añadido, necesario para el filtro de habitat
ESTADO_EVENTO_OPTIONS = ["programado", "activo", "finalizado", "cancelado"]
TIPO_VISITANTE_OPTIONS = ["adulto", "niño", "estudiante", "tercera_edad"]
CALIFICACION_PROVEEDOR_OPTIONS = list(range(1, 6)) # De 1 a 5
TIPO_PROVEEDOR_OPTIONS = ["alimentos", "medicamentos", "equipos", "servicios"]

# --- Funciones auxiliares para obtener datos de la DB para los filtros ---
def get_all_especies(db):
    return db.query(Especie).all()

def get_all_tipos_habitat(db):
    return db.query(TipoHabitat).all()

def get_all_habitats(db):
    # Asume que tienes una función en crud.py para obtener hábitats
    return crud.get_habitats(db)

# --- Configuración de la página Streamlit ---
st.set_page_config(layout="wide", page_title="Reportes del Zoológico")

st.title("📊 Generación de Reportes Personalizados del Zoológico")
st.write("Selecciona un reporte y aplica los filtros deseados para generar y exportar los datos.")

# --- Seleccionar el tipo de reporte ---
report_choice = st.selectbox(
    "Selecciona un tipo de reporte:",
    ["Animales por Hábitat", "Eventos y Asistencia", "Alimentos y Proveedores", "Ver datos"]
)

# --- Conexión a la base de datos ---
db = next(get_db())

try:
    # --- Reporte de Animales por Hábitat ---
    if report_choice == "Animales por Hábitat":
        st.header("Reporte de Animales por Hábitat")
        st.markdown("---")
        with st.form("reporte_animales_form"):
            st.subheader("Filtros para el Reporte de Animales por Hábitat:")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                # Filtro 1: Nombre de Hábitat (Ej: "Jungla de Asia")
                habitats = get_all_habitats(db)
                habitat_nombres = [""] + sorted([h.nombre for h in habitats])
                nombre_habitat_filtro = st.selectbox(
                    "Nombre del Hábitat", 
                    habitat_nombres, 
                    index=habitat_nombres.index("Jungla de Asia") if "Jungla de Asia" in habitat_nombres else 0, # Valor de prueba
                    key="filt_habitat_nombre_animales"
                )
                
                # Filtro 2: Tipo de Hábitat (Ej: "Bosque Tropical")
                tipos_habitat = get_all_tipos_habitat(db)
                tipo_habitat_nombres = [""] + sorted([th.nombre for th in tipos_habitat])
                tipo_habitat_filtro = st.selectbox(
                    "Tipo de Hábitat", 
                    tipo_habitat_nombres, 
                    index=tipo_habitat_nombres.index("Bosque Tropical") if "Bosque Tropical" in tipo_habitat_nombres else 0, # Valor de prueba
                    key="filt_tipo_habitat_animales"
                )

                # Filtro 3: Estado de Hábitat (Ej: "activo")
                estado_habitat_filtro = st.selectbox(
                    "Estado del Hábitat", 
                    [""] + ESTADO_HABITAT_OPTIONS, 
                    index=ESTADO_HABITAT_OPTIONS.index("activo") + 1 if "activo" in ESTADO_HABITAT_OPTIONS else 0, # Valor de prueba (+1 por el "" inicial)
                    key="filt_estado_habitat_animales"
                )

            with col2:
                # Filtro 4: Especie (Ej: "Tigre")
                especies = get_all_especies(db)
                especie_nombres = [""] + sorted([e.nombre_comun for e in especies])
                especie_nombre_comun_filtro = st.selectbox(
                    "Especie del Animal (nombre común)", 
                    especie_nombres, 
                    index=especie_nombres.index("Tigre") if "Tigre" in especie_nombres else 0, # Valor de prueba
                    key="filt_especie_animales"
                )
                
                # Filtro 5: Sexo del Animal (Ej: "M")
                sexo_animal_filtro = st.selectbox(
                    "Sexo del Animal", 
                    [""] + SEXO_OPTIONS, 
                    index=SEXO_OPTIONS.index("M") + 1 if "M" in SEXO_OPTIONS else 0, # Valor de prueba (+1 por el "" inicial)
                    key="filt_sexo_animales"
                )

                # Filtro 6: Estado de Salud del Animal (Ej: "excelente")
                estado_salud_animal_filtro = st.selectbox(
                    "Estado de Salud del Animal", 
                    [""] + ESTADO_SALUD_OPTIONS, 
                    index=ESTADO_SALUD_OPTIONS.index("excelente") + 1 if "excelente" in ESTADO_SALUD_OPTIONS else 0, # Valor de prueba (+1 por el "" inicial)
                    key="filt_estado_salud_animales"
                )

            with col3:
                # Filtro 7: Peso Mínimo (Ej: 150.0)
                min_peso = st.number_input("Peso Mínimo (kg)", min_value=0.0, value=150.0, format="%.2f", key="filt_min_peso_animales") # Valor de prueba
                
                # Filtro 8: Peso Máximo (Ej: 250.0)
                max_peso = st.number_input("Peso Máximo (kg)", min_value=0.0, value=250.0, format="%.2f", key="filt_max_peso_animales") # Valor de prueba
                
                # Filtro 9: Origen del Animal (No estaba en los tests, pero es un filtro útil y se incluye en la función)
                origen_animal_filtro = st.selectbox("Origen del Animal", [""] + ORIGEN_OPTIONS, key="filt_origen_animales")
                
                # (Se necesitan 5 filtros significativos, y la función soporta más. Añadí estado_habitat, y usé origen_animal)

            submitted_animal_report = st.form_submit_button("Generar Reporte de Animales")

        if submitted_animal_report:
            st.subheader("Resultados del Reporte de Animales por Hábitat")
            try:
                report_data = get_reporte_animales_por_habitat(
                    db=db,
                    nombre_habitat=nombre_habitat_filtro if nombre_habitat_filtro else None,
                    tipo_habitat=tipo_habitat_filtro if tipo_habitat_filtro else None,
                    estado_habitat=estado_habitat_filtro if estado_habitat_filtro else None, # Pasando el nuevo filtro
                    especie_nombre_comun=especie_nombre_comun_filtro if especie_nombre_comun_filtro else None,
                    sexo_animal=sexo_animal_filtro if sexo_animal_filtro else None,
                    estado_salud_animal=estado_salud_animal_filtro if estado_salud_animal_filtro else None,
                    min_peso=min_peso if min_peso > 0 else None,
                    max_peso=max_peso if max_peso < 9999.99 else None,
                    # origen_animal se pasa si la función lo soporta (se agregó en el código anterior)
                    # La función get_reporte_animales_por_habitat en tu test no lo tiene explicitamente,
                    # pero si tu versión actual lo tiene, se podría pasar:
                    # origen_animal=origen_animal_filtro if origen_animal_filtro else None,
                    export_csv=False
                )
                if not report_data.empty:
                    st.dataframe(report_data, use_container_width=True)
                    
                    csv_buffer = io.StringIO()
                    report_data.to_csv(csv_buffer, index=False)
                    st.download_button(
                        label="Descargar Reporte Animales (CSV)",
                        data=csv_buffer.getvalue(),
                        file_name="reporte_animales_habitat.csv",
                        mime="text/csv",
                    )
                else:
                    st.info("No se encontraron datos de animales con los filtros seleccionados.")
            except Exception as e:
                st.error(f"Error al generar el reporte de animales: {e}")

    elif report_choice == "Ver datos":
        try:
            df_animales_all = get_reporte_animales_por_habitat(
                db=db,
                export_csv=True,
                filename="reporte_animales_habitat_todos.csv"
            )
            st.subheader("Resultados todos los animales por habitat.")
            st.write(df_animales_all)

            df_eventos_all = get_reporte_eventos_y_asistencia(
                db=db,
                export_csv=True,
                filename="reporte_eventos_asistencia_todos.csv"
            )
            st.subheader("Resultados todos los eventos y asistencias.")
            st.write(df_eventos_all)

            df_alimentos_all = get_reporte_alimentos_y_proveedores(
                db=db,
                export_csv=True,
                filename="reporte_alimentos_proveedores_todos.csv"
            )
            st.subheader("Resultados todos los alimentos y proveedores.")
            st.write(df_alimentos_all)
        except Exception as e:
                st.error(f"Error al generar datos: {e}")  
    # --- Reporte de Eventos y Asistencia ---
    elif report_choice == "Eventos y Asistencia":
        st.header("Reporte de Eventos y Asistencia")
        st.markdown("---")
        with st.form("reporte_eventos_form"):
            st.subheader("Filtros para el Reporte de Eventos y Asistencia:")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                # Filtro 1: Fecha de Inicio Desde (Ej: date(2025, 7, 1))
                fecha_inicio_desde = st.date_input("Fecha de Inicio (Desde)", value=date(2025, 7, 1), key="filt_f_inicio_desde_eventos")
                
                # Filtro 2: Fecha de Inicio Hasta (Ej: date(2025, 8, 31))
                fecha_inicio_hasta = st.date_input("Fecha de Inicio (Hasta)", value=date(2025, 8, 31), key="filt_f_inicio_hasta_eventos")
                
                # Filtro 3: Tipo de Evento (Ej: "educativo")
                tipo_evento_filtro = st.text_input("Tipo de Evento", value="educativo", key="filt_tipo_evento_eventos")

            with col2:
                # Filtro 4: Estado del Evento (Ej: "programado")
                estado_evento_filtro = st.selectbox(
                    "Estado del Evento", 
                    [""] + ESTADO_EVENTO_OPTIONS, 
                    index=ESTADO_EVENTO_OPTIONS.index("programado") + 1 if "programado" in ESTADO_EVENTO_OPTIONS else 0, # Valor de prueba (+1 por el "" inicial)
                    key="filt_estado_evento_eventos"
                )
                
                # Filtro 5: Precio Mínimo de Entrada (Ej: 0.0)
                min_precio_entrada = st.number_input("Precio Mínimo de Entrada", min_value=0.0, value=0.0, format="%.2f", key="filt_min_precio_eventos") # Valor de prueba
                
                # Filtro 6: Precio Máximo de Entrada (Ej: 10.0)
                max_precio_entrada = st.number_input("Precio Máximo de Entrada", min_value=0.0, value=10.0, format="%.2f", key="filt_max_precio_eventos") # Valor de prueba

            with col3:
                # Filtro 7: Tipo de Visitante (Ej: "adulto")
                tipo_visitante_filtro = st.selectbox(
                    "Tipo de Visitante (asistencia)", 
                    [""] + TIPO_VISITANTE_OPTIONS, 
                    index=TIPO_VISITANTE_OPTIONS.index("adulto") + 1 if "adulto" in TIPO_VISITANTE_OPTIONS else 0, # Valor de prueba (+1 por el "" inicial)
                    key="filt_tipo_visitante_eventos"
                )
                
                # Filtro 8: Nacionalidad del Visitante (Ej: "Guatemalteca")
                nacionalidad_visitante_filtro = st.text_input("Nacionalidad del Visitante (asistencia)", value="Guatemalteca", key="filt_nacionalidad_visitante_eventos") # Valor de prueba
                
                # Filtro 9: Eventos con Asistencia registrada (Ej: True)
                evento_con_asistencia = st.checkbox("Solo eventos con asistencia registrada", value=True, key="filt_con_asistencia_eventos") # Valor de prueba

            submitted_event_report = st.form_submit_button("Generar Reporte de Eventos")

        if submitted_event_report:
            st.subheader("Resultados del Reporte de Eventos y Asistencia")
            try:
                report_data = get_reporte_eventos_y_asistencia(
                    db=db,
                    fecha_inicio_desde=fecha_inicio_desde,
                    fecha_inicio_hasta=fecha_inicio_hasta,
                    tipo_evento=tipo_evento_filtro if tipo_evento_filtro else None,
                    estado_evento=estado_evento_filtro if estado_evento_filtro else None,
                    min_precio_entrada=min_precio_entrada if min_precio_entrada > 0 else None,
                    max_precio_entrada=max_precio_entrada if max_precio_entrada < 999.99 else None,
                    tipo_visitante=tipo_visitante_filtro if tipo_visitante_filtro else None,
                    nacionalidad_visitante=nacionalidad_visitante_filtro if nacionalidad_visitante_filtro else None,
                    evento_con_asistencia=evento_con_asistencia,
                    export_csv=False
                )
                if not report_data.empty:
                    st.dataframe(report_data, use_container_width=True)
                    
                    csv_buffer = io.StringIO()
                    report_data.to_csv(csv_buffer, index=False)
                    st.download_button(
                        label="Descargar Reporte Eventos (CSV)",
                        data=csv_buffer.getvalue(),
                        file_name="reporte_eventos_asistencia.csv",
                        mime="text/csv",
                    )
                else:
                    st.info("No se encontraron datos de eventos con los filtros seleccionados.")
            except Exception as e:
                st.error(f"Error al generar el reporte de eventos: {e}")

    # --- Reporte de Alimentos y Proveedores ---
    elif report_choice == "Alimentos y Proveedores":
        st.header("Reporte de Alimentos y Proveedores")
        st.markdown("---")
        with st.form("reporte_alimentos_form"):
            st.subheader("Filtros para el Reporte de Alimentos y Proveedores:")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                # Filtro 1: Nombre de Alimento (Ej: "Carne")
                nombre_alimento_filtro = st.text_input("Nombre del Alimento", value="Carne", key="filt_nombre_alimento_alimentos")
                
                # Filtro 2: Tipo de Alimento (Ej: "carnivoro")
                tipo_alimento_filtro = st.text_input("Tipo de Alimento (ej. 'carnivoro')", value="carnivoro", key="filt_tipo_alimento_alimentos")

                # Filtro 3: Nombre de Proveedor (Ej: "ZooFood S.A.")
                nombre_proveedor_filtro = st.text_input("Nombre del Proveedor", value="ZooFood S.A.", key="filt_nombre_proveedor_alimentos")

            with col2:
                # Filtro 4: Tipo de Proveedor (Ej: "alimentos")
                tipo_proveedor_filtro = st.selectbox(
                    "Tipo de Proveedor", 
                    [""] + TIPO_PROVEEDOR_OPTIONS, 
                    index=TIPO_PROVEEDOR_OPTIONS.index("alimentos") + 1 if "alimentos" in TIPO_PROVEEDOR_OPTIONS else 0, # Valor de prueba (+1 por el "" inicial)
                    key="filt_tipo_proveedor_alimentos"
                )
                
                # Filtro 5: Calificación Mínima del Proveedor (Ej: 5)
                calificacion_proveedor_min = st.selectbox(
                    "Calificación Mínima del Proveedor", 
                    [""] + CALIFICACION_PROVEEDOR_OPTIONS, 
                    index=CALIFICACION_PROVEEDOR_OPTIONS.index(5) + 1 if 5 in CALIFICACION_PROVEEDOR_OPTIONS else 0, # Valor de prueba (+1 por el "" inicial)
                    key="filt_calificacion_proveedor_alimentos"
                )
                
                # Filtro 6: Stock Actual Mínimo (Ej: 100)
                stock_actual_min = st.number_input("Stock Actual Mínimo", min_value=0, value=100, key="filt_stock_min_alimentos") # Valor de prueba
            
            with col3:
                # Filtro 7: Fecha de Vencimiento Anterior a (Ej: date(2025, 12, 31))
                fecha_vencimiento_antes = st.date_input("Fecha de Vencimiento Anterior a", value=date(2025, 12, 31), key="filt_fecha_venc_alimentos") # Valor de prueba
                
                # Filtro 8: Costo por Kg Máximo (Ej: 12.00)
                costo_por_kg_max = st.number_input("Costo por Kg Máximo", min_value=0.0, value=12.00, format="%.2f", key="filt_costo_max_alimentos") # Valor de prueba
                
                # Filtro 9: Costo por Kg Mínimo (No estaba en los tests, pero es un filtro útil)
                costo_por_kg_min = st.number_input("Costo por Kg Mínimo", min_value=0.0, value=0.0, format="%.2f", key="filt_costo_min_alimentos")

            submitted_food_report = st.form_submit_button("Generar Reporte de Alimentos")

        if submitted_food_report:
            st.subheader("Resultados del Reporte de Alimentos y Proveedores")
            try:
                report_data = get_reporte_alimentos_y_proveedores(
                    db=db,
                    nombre_alimento=nombre_alimento_filtro if nombre_alimento_filtro else None,
                    tipo_alimento=tipo_alimento_filtro if tipo_alimento_filtro else None,
                    nombre_proveedor=nombre_proveedor_filtro if nombre_proveedor_filtro else None,
                    tipo_proveedor=tipo_proveedor_filtro if tipo_proveedor_filtro else None,
                    calificacion_proveedor_min=calificacion_proveedor_min if calificacion_proveedor_min else None,
                    stock_actual_min=stock_actual_min if stock_actual_min > 0 else None,
                    fecha_vencimiento_antes=fecha_vencimiento_antes,
                    costo_por_kg_max=costo_por_kg_max if costo_por_kg_max < 999.99 else None,
                    export_csv=False
                )
                if not report_data.empty:
                    st.dataframe(report_data, use_container_width=True)
                    
                    csv_buffer = io.StringIO()
                    report_data.to_csv(csv_buffer, index=False)
                    st.download_button(
                        label="Descargar Reporte Alimentos (CSV)",
                        data=csv_buffer.getvalue(),
                        file_name="reporte_alimentos_proveedores.csv",
                        mime="text/csv",
                    )
                else:
                    st.info("No se encontraron datos de alimentos con los filtros seleccionados.")
            except Exception as e:
                st.error(f"Error al generar el reporte de alimentos: {e}")

except Exception as e:
    st.error(f"Ocurrió un error inesperado al conectar con la base de datos o al cargar datos para filtros: {e}")
finally:
    db.close()