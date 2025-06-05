# app/streamlitview/home.py
import sys
import os
# Añade el root del proyecto al path (sube 2 niveles desde este archivo)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import streamlit as st
from database import get_db
from models import Animal, Evento, Habitat, Especie, TipoHabitat
from crud import crud
from crud import crudvista
from datetime import date, time
import uuid

# --- Helper Functions for Data Retrieval (Used in Streamlit forms) ---

def get_all_especies(db):
    return db.query(Especie).all()

def get_all_tipos_habitat(db):
    return db.query(TipoHabitat).all()

# --- Streamlit App Structure ---

st.set_page_config(layout="wide", page_title="Gestión de Zoológico - CRUD")

st.title("Gestión de Zoológico - CRUD")

# Sidebar for navigation
st.sidebar.title("Navegación")
selection = st.sidebar.radio(
    "Selecciona una opción:",
    ["Dashboard Principal", "Animales", "Hábitats", "Eventos"]
)

db = next(get_db())

try:
    if selection == "Dashboard Principal":
        st.header("Bienvenido al Panel de Gestión del Zoológico")
        st.write("Usa el menú de la izquierda para navegar entre las operaciones CRUD para Animales, Hábitats y Eventos, o para ver las vistas de datos predefinidas.")
        
        st.subheader("Resumen Rápido")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Animales", crud.get_animals(db, skip=0, limit=10000).__len__())
        with col2:
            st.metric("Total Hábitats", crud.get_habitats(db, skip=0, limit=10000).__len__())
        with col3:
            st.metric("Total Eventos", crud.get_eventos(db, skip=0, limit=10000).__len__())

    # --- Animales CRUD ---
    elif selection == "Animales":
        st.header("Gestión de Animales")
        operation = st.selectbox("Selecciona una operación:", ["Crear Animal", "Ver Animales", "Actualizar Animal", "Eliminar Animal"])

        if operation == "Crear Animal":
            st.subheader("Crear Nuevo Animal")
            with st.form("create_animal_form"):
                nombre = st.text_input("Nombre del Animal", key="animal_nombre_create")
                
                especies = get_all_especies(db)
                especie_options = {e.nombre_comun: e.id_especie for e in especies}
                selected_especie_name = st.selectbox("Especie", list(especie_options.keys()), key="animal_especie_create")
                id_especie = especie_options.get(selected_especie_name)

                habitats = crud.get_habitats(db)
                habitat_options = {h.nombre: h.id_habitat for h in habitats}
                selected_habitat_name = st.selectbox("Hábitat", list(habitat_options.keys()), key="animal_habitat_create")
                id_habitat = habitat_options.get(selected_habitat_name)

                fecha_nacimiento = st.date_input("Fecha de Nacimiento", value=date.today(), key="animal_fnac_create")
                sexo = st.selectbox("Sexo", ["M", "F", "Desconocido"], key="animal_sexo_create")
                peso_actual = st.number_input("Peso Actual (kg)", min_value=0.0, format="%.2f", key="animal_peso_create")
                altura = st.number_input("Altura (m)", min_value=0.0, format="%.2f", key="animal_altura_create")
                numero_identificacion = st.text_input("Número de Identificación (único)", value=f"ANI-{uuid.uuid4().hex[:8].upper()}", key="animal_id_create")
                origen = st.text_input("Origen", key="animal_origen_create")
                estado_salud = st.text_input("Estado de Salud", key="animal_salud_create")

                submitted = st.form_submit_button("Crear Animal")
                if submitted:
                    if not all([nombre, id_especie, id_habitat, fecha_nacimiento, sexo, peso_actual, altura, numero_identificacion, origen, estado_salud]):
                        st.error("Por favor, rellena todos los campos obligatorios.")
                    else:
                        try:
                            new_animal_data = {
                                "nombre": nombre,
                                "id_especie": id_especie,
                                "id_habitat": id_habitat,
                                "fecha_nacimiento": fecha_nacimiento,
                                "sexo": sexo,
                                "peso_actual": peso_actual,
                                "altura": altura,
                                "numero_identificacion": numero_identificacion,
                                "origen": origen,
                                "estado_salud": estado_salud
                            }
                            created_animal = crud.create_animal(db, new_animal_data)
                            st.success(f"Animal '{created_animal.nombre}' creado con éxito.")
                            st.write(created_animal)
                        except Exception as e:
                            st.error(f"Error al crear animal: {e}")

        elif operation == "Ver Animales":
            st.subheader("Lista de Animales")
            animals = crud.get_animals(db)
            if animals:
                animal_data = [
                    {
                        "ID": a.id_animal,
                        "Nombre": a.nombre,
                        "Especie": a.especie.nombre_comun if a.especie else "N/A",
                        "Hábitat": a.habitat.nombre if a.habitat else "N/A",
                        "Nacimiento": a.fecha_nacimiento,
                        "Sexo": a.sexo,
                        "Peso (kg)": a.peso_actual,
                        "Altura (m)": a.altura,
                        "ID Num": a.numero_identificacion,
                        "Origen": a.origen,
                        "Salud": a.estado_salud
                    } for a in animals
                ]
                st.dataframe(animal_data, use_container_width=True)
            else:
                st.info("No hay animales registrados.")

        elif operation == "Actualizar Animal":
            st.subheader("Actualizar Animal Existente")
            animals = crud.get_animals(db)
            if animals:
                animal_display_names = {f"{a.nombre} (ID: {a.id_animal})": a.id_animal for a in animals}
                selected_animal_display = st.selectbox("Selecciona un animal para actualizar:", list(animal_display_names.keys()), key="update_animal_select")
                selected_animal_id = animal_display_names.get(selected_animal_display)

                if selected_animal_id:
                    animal_to_update = crud.get_animal(db, selected_animal_id)
                    if animal_to_update:
                        with st.form("update_animal_form"):
                            st.write(f"Actualizando animal: **{animal_to_update.nombre}**")
                            new_nombre = st.text_input("Nuevo Nombre", value=animal_to_update.nombre, key="animal_nombre_update")
                            
                            especies = get_all_especies(db)
                            especie_options = {e.nombre_comun: e.id_especie for e in especies}
                            current_especie_name = animal_to_update.especie.nombre_comun if animal_to_update.especie else "N/A"
                            selected_especie_update_name = st.selectbox(
                                "Nueva Especie", 
                                list(especie_options.keys()), 
                                index=list(especie_options.keys()).index(current_especie_name) if current_especie_name in especie_options else 0,
                                key="animal_especie_update"
                            )
                            new_id_especie = especie_options.get(selected_especie_update_name)

                            habitats = crud.get_habitats(db)
                            habitat_options = {h.nombre: h.id_habitat for h in habitats}
                            current_habitat_name = animal_to_update.habitat.nombre if animal_to_update.habitat else "N/A"
                            selected_habitat_update_name = st.selectbox(
                                "Nuevo Hábitat", 
                                list(habitat_options.keys()), 
                                index=list(habitat_options.keys()).index(current_habitat_name) if current_habitat_name in habitat_options else 0,
                                key="animal_habitat_update"
                            )
                            new_id_habitat = habitat_options.get(selected_habitat_update_name)

                            new_fecha_nacimiento = st.date_input("Nueva Fecha de Nacimiento", value=animal_to_update.fecha_nacimiento, key="animal_fnac_update")
                            new_sexo = st.selectbox("Nuevo Sexo", ["M", "F", "Desconocido"], index=["M", "F", "Desconocido"].index(animal_to_update.sexo) if animal_to_update.sexo in ["M", "F", "Desconocido"] else 0, key="animal_sexo_update")
                            new_peso_actual = st.number_input("Nuevo Peso Actual (kg)", value=float(animal_to_update.peso_actual), min_value=0.0, format="%.2f", key="animal_peso_update")
                            new_altura = st.number_input("Nueva Altura (m)", value=float(animal_to_update.altura), min_value=0.0, format="%.2f", key="animal_altura_update")
                            new_origen = st.text_input("Nuevo Origen", value=animal_to_update.origen, key="animal_origen_update")
                            new_estado_salud = st.text_input("Nuevo Estado de Salud", value=animal_to_update.estado_salud, key="animal_salud_update")

                            update_submitted = st.form_submit_button("Actualizar Animal")
                            if update_submitted:
                                try:
                                    update_data = {
                                        "nombre": new_nombre,
                                        "id_especie": new_id_especie,
                                        "id_habitat": new_id_habitat,
                                        "fecha_nacimiento": new_fecha_nacimiento,
                                        "sexo": new_sexo,
                                        "peso_actual": new_peso_actual,
                                        "altura": new_altura,
                                        "origen": new_origen,
                                        "estado_salud": new_estado_salud
                                    }
                                    updated_animal = crud.update_animal(db, selected_animal_id, update_data)
                                    st.success(f"Animal '{updated_animal.nombre}' actualizado con éxito.")
                                    st.write(updated_animal)
                                except Exception as e:
                                    st.error(f"Error al actualizar animal: {e}")
                    else:
                        st.warning("Animal no encontrado.")
            else:
                st.info("No hay animales para actualizar.")

        elif operation == "Eliminar Animal":
            st.subheader("Eliminar Animal")
            animals = crud.get_animals(db)
            if animals:
                animal_display_names = {f"{a.nombre} (ID: {a.id_animal})": a.id_animal for a in animals}
                selected_animal_display = st.selectbox("Selecciona un animal para eliminar:", list(animal_display_names.keys()), key="delete_animal_select")
                selected_animal_id = animal_display_names.get(selected_animal_display)

                if st.button("Eliminar Animal", key="delete_animal_button"):
                    if selected_animal_id:
                        try:
                            deleted_animal = crud.delete_animal(db, selected_animal_id)
                            if deleted_animal:
                                st.success(f"Animal '{deleted_animal.nombre}' eliminado con éxito.")
                            else:
                                st.warning("Animal no encontrado o ya eliminado.")
                        except Exception as e:
                            st.error(f"Error al eliminar animal: {e}")
                    else:
                        st.warning("Por favor, selecciona un animal.")
            else:
                st.info("No hay animales para eliminar.")

    # --- Hábitats CRUD ---
    elif selection == "Hábitats":
        st.header("Gestión de Hábitats")
        operation = st.selectbox("Selecciona una operación:", ["Crear Hábitat", "Ver Hábitats", "Actualizar Hábitat", "Eliminar Hábitat"])

        if operation == "Crear Hábitat":
            st.subheader("Crear Nuevo Hábitat")
            with st.form("create_habitat_form"):
                nombre = st.text_input("Nombre del Hábitat", key="habitat_nombre_create")
                
                tipos_habitat = get_all_tipos_habitat(db)
                tipo_habitat_options = {th.nombre: th.id_tipo_habitat for th in tipos_habitat}
                selected_tipo_habitat_name = st.selectbox("Tipo de Hábitat", list(tipo_habitat_options.keys()), key="habitat_tipo_create")
                id_tipo_habitat = tipo_habitat_options.get(selected_tipo_habitat_name)

                col_loc1, col_loc2, col_loc3 = st.columns(3)
                with col_loc1:
                    latitud = st.number_input("Latitud", format="%.4f", key="habitat_lat_create")
                with col_loc2:
                    longitud = st.number_input("Longitud", format="%.4f", key="habitat_lon_create")
                with col_loc3:
                    altitud = st.number_input("Altitud (m)", key="habitat_alt_create")
                
                capacidad_maxima = st.number_input("Capacidad Máxima", min_value=1, value=5, key="habitat_cap_create")
                area_metros_cuadrados = st.number_input("Área (m²)", min_value=0.0, format="%.2f", key="habitat_area_create")
                fecha_construccion = st.date_input("Fecha de Construcción", value=date.today(), key="habitat_fcons_create")
                estado = st.selectbox("Estado", ["activo", "inactivo", "mantenimiento"], key="habitat_estado_create")
                costo_mantenimiento_mensual = st.number_input("Costo Mantenimiento Mensual", min_value=0.0, format="%.2f", key="habitat_costo_create")

                submitted = st.form_submit_button("Crear Hábitat")
                if submitted:
                    if not all([nombre, id_tipo_habitat, capacidad_maxima, area_metros_cuadrados, fecha_construccion, estado, costo_mantenimiento_mensual]):
                        st.error("Por favor, rellena todos los campos obligatorios.")
                    else:
                        try:
                            new_habitat_data = {
                                "nombre": nombre,
                                "id_tipo_habitat": id_tipo_habitat,
                                "ubicacion": {"latitud": latitud, "longitud": longitud, "altitud": altitud},
                                "capacidad_maxima": capacidad_maxima,
                                "area_metros_cuadrados": area_metros_cuadrados,
                                "fecha_construccion": fecha_construccion,
                                "estado": estado,
                                "costo_mantenimiento_mensual": costo_mantenimiento_mensual
                            }
                            created_habitat = crud.create_habitat(db, new_habitat_data)
                            st.success(f"Hábitat '{created_habitat.nombre}' creado con éxito.")
                            st.write(created_habitat)
                        except Exception as e:
                            st.error(f"Error al crear hábitat: {e}")

        elif operation == "Ver Hábitats":
            st.subheader("Lista de Hábitats")
            habitats = crud.get_habitats(db)
            if habitats:
                habitat_data = [
                    {
                        "ID": h.id_habitat,
                        "Nombre": h.nombre,
                        "Tipo": h.tipo_habitat.nombre if h.tipo_habitat else "N/A",
                        "Ubicación": f"Lat:{h.ubicacion['latitud']}, Lon:{h.ubicacion['longitud']}" if h.ubicacion else "N/A",
                        "Capacidad": h.capacidad_maxima,
                        "Área (m²)": h.area_metros_cuadrados,
                        "Construcción": h.fecha_construccion,
                        "Estado": h.estado,
                        "Costo Mant.": h.costo_mantenimiento_mensual
                    } for h in habitats
                ]
                st.dataframe(habitat_data, use_container_width=True)
            else:
                st.info("No hay hábitats registrados.")

        elif operation == "Actualizar Hábitat":
            st.subheader("Actualizar Hábitat Existente")
            habitats = crud.get_habitats(db)
            if habitats:
                habitat_display_names = {f"{h.nombre} (ID: {h.id_habitat})": h.id_habitat for h in habitats}
                selected_habitat_display = st.selectbox("Selecciona un hábitat para actualizar:", list(habitat_display_names.keys()), key="update_habitat_select")
                selected_habitat_id = habitat_display_names.get(selected_habitat_display)

                if selected_habitat_id:
                    habitat_to_update = crud.get_habitat(db, selected_habitat_id)
                    if habitat_to_update:
                        with st.form("update_habitat_form"):
                            st.write(f"Actualizando hábitat: **{habitat_to_update.nombre}**")
                            new_nombre = st.text_input("Nuevo Nombre", value=habitat_to_update.nombre, key="habitat_nombre_update")
                            
                            tipos_habitat = get_all_tipos_habitat(db)
                            tipo_habitat_options = {th.nombre: th.id_tipo_habitat for th in tipos_habitat}
                            current_tipo_habitat_name = habitat_to_update.tipo_habitat.nombre if habitat_to_update.tipo_habitat else "N/A"
                            selected_tipo_habitat_update_name = st.selectbox(
                                "Nuevo Tipo de Hábitat", 
                                list(tipo_habitat_options.keys()), 
                                index=list(tipo_habitat_options.keys()).index(current_tipo_habitat_name) if current_tipo_habitat_name in tipo_habitat_options else 0,
                                key="habitat_tipo_update"
                            )
                            new_id_tipo_habitat = tipo_habitat_options.get(selected_tipo_habitat_update_name)

                            current_lat = habitat_to_update.ubicacion['latitud'] if habitat_to_update.ubicacion else 0.0
                            current_lon = habitat_to_update.ubicacion['longitud'] if habitat_to_update.ubicacion else 0.0
                            current_alt = habitat_to_update.ubicacion['altitud'] if habitat_to_update.ubicacion else 0.0

                            col_loc1_up, col_loc2_up, col_loc3_up = st.columns(3)
                            with col_loc1_up:
                                new_latitud = st.number_input("Nueva Latitud", value=float(current_lat), format="%.4f", key="habitat_lat_update")
                            with col_loc2_up:
                                new_longitud = st.number_input("Nueva Longitud", value=float(current_lon), format="%.4f", key="habitat_lon_update")
                            with col_loc3_up:
                                new_altitud = st.number_input("Nueva Altitud (m)", value=float(current_alt), key="habitat_alt_update")

                            new_capacidad_maxima = st.number_input("Nueva Capacidad Máxima", value=habitat_to_update.capacidad_maxima, min_value=1, key="habitat_cap_update")
                            new_area_metros_cuadrados = st.number_input("Nueva Área (m²)", value=float(habitat_to_update.area_metros_cuadrados), min_value=0.0, format="%.2f", key="habitat_area_update")
                            new_fecha_construccion = st.date_input("Nueva Fecha de Construcción", value=habitat_to_update.fecha_construccion, key="habitat_fcons_update")
                            new_estado = st.selectbox("Nuevo Estado", ["activo", "inactivo", "mantenimiento"], index=["activo", "inactivo", "mantenimiento"].index(habitat_to_update.estado), key="habitat_estado_update")
                            new_costo_mantenimiento_mensual = st.number_input("Nuevo Costo Mantenimiento Mensual", value=float(habitat_to_update.costo_mantenimiento_mensual), min_value=0.0, format="%.2f", key="habitat_costo_update")

                            update_submitted = st.form_submit_button("Actualizar Hábitat")
                            if update_submitted:
                                try:
                                    update_data = {
                                        "nombre": new_nombre,
                                        "id_tipo_habitat": new_id_tipo_habitat,
                                        "ubicacion": {"latitud": new_latitud, "longitud": new_longitud, "altitud": new_altitud},
                                        "capacidad_maxima": new_capacidad_maxima,
                                        "area_metros_cuadrados": new_area_metros_cuadrados,
                                        "fecha_construccion": new_fecha_construccion,
                                        "estado": new_estado,
                                        "costo_mantenimiento_mensual": new_costo_mantenimiento_mensual
                                    }
                                    updated_habitat = crud.update_habitat(db, selected_habitat_id, update_data)
                                    st.success(f"Hábitat '{updated_habitat.nombre}' actualizado con éxito.")
                                    st.write(updated_habitat)
                                except Exception as e:
                                    st.error(f"Error al actualizar hábitat: {e}")
                    else:
                        st.warning("Hábitat no encontrado.")
            else:
                st.info("No hay hábitats para actualizar.")

        elif operation == "Eliminar Hábitat":
            st.subheader("Eliminar Hábitat")
            habitats = crud.get_habitats(db)
            if habitats:
                habitat_display_names = {f"{h.nombre} (ID: {h.id_habitat})": h.id_habitat for h in habitats}
                selected_habitat_display = st.selectbox("Selecciona un hábitat para eliminar:", list(habitat_display_names.keys()), key="delete_habitat_select")
                selected_habitat_id = habitat_display_names.get(selected_habitat_display)

                if st.button("Eliminar Hábitat", key="delete_habitat_button"):
                    if selected_habitat_id:
                        # Check if any animals are still linked to this habitat
                        animals_in_habitat = db.query(Animal).filter(Animal.id_habitat == selected_habitat_id).first()
                        if animals_in_habitat:
                            st.warning(f"No se puede eliminar el hábitat '{selected_habitat_display}' porque aún tiene animales asociados. Por favor, reasigna o elimina los animales primero.")
                        else:
                            try:
                                deleted_habitat = crud.delete_habitat(db, selected_habitat_id)
                                if deleted_habitat:
                                    st.success(f"Hábitat '{deleted_habitat.nombre}' eliminado con éxito.")
                                else:
                                    st.warning("Hábitat no encontrado o ya eliminado.")
                            except Exception as e:
                                st.error(f"Error al eliminar hábitat: {e}")
                    else:
                        st.warning("Por favor, selecciona un hábitat.")
            else:
                st.info("No hay hábitats para eliminar.")

    # --- Eventos CRUD ---
    elif selection == "Eventos":
        st.header("Gestión de Eventos")
        operation = st.selectbox("Selecciona una operación:", ["Crear Evento", "Ver Eventos", "Actualizar Evento", "Eliminar Evento"])

        if operation == "Crear Evento":
            st.subheader("Crear Nuevo Evento")
            with st.form("create_evento_form"):
                nombre = st.text_input("Nombre del Evento", key="evento_nombre_create")
                descripcion = st.text_area("Descripción", key="evento_desc_create")
                fecha_inicio = st.date_input("Fecha de Inicio", value=date.today(), key="evento_f_inicio_create")
                fecha_fin = st.date_input("Fecha de Fin", value=date.today(), key="evento_f_fin_create")
                horario_inicio = st.time_input("Horario de Inicio", value=time(9, 0), key="evento_h_inicio_create")
                horario_fin = st.time_input("Horario de Fin", value=time(17, 0), key="evento_h_fin_create")
                capacidad_maxima = st.number_input("Capacidad Máxima", min_value=1, value=100, key="evento_cap_create")
                precio_entrada = st.number_input("Precio de Entrada", min_value=0.0, format="%.2f", key="evento_precio_create")
                tipo_evento = st.text_input("Tipo de Evento", key="evento_tipo_create")
                estado = st.selectbox("Estado", ["programado", "activo", "finalizado", "cancelado"], key="evento_estado_create")
                
                st.markdown("---")
                st.write("**Horario Complejo (JSON)**")
                st.info("Introduce un diccionario JSON válido. Ejemplo: `{'dias_semana': [1, 3], 'hora_inicio': '09:00:00', 'hora_fin': '12:00:00', 'duracion_minutos': 180, 'frecuencia': 'semanal'}`")
                horario_complejo_str = st.text_area("Horario Complejo (JSON)", value="{}", key="evento_horario_complejo_create")

                submitted = st.form_submit_button("Crear Evento")
                if submitted:
                    try:
                        horario_complejo_dict = {}
                        if horario_complejo_str.strip():
                            import json
                            horario_complejo_dict = json.loads(horario_complejo_str)
                            # Basic validation for required keys
                            required_keys = ["dias_semana", "hora_inicio", "hora_fin", "duracion_minutos", "frecuencia"]
                            if not all(k in horario_complejo_dict for k in required_keys):
                                st.error(f"Horario Complejo JSON debe contener las claves: {', '.join(required_keys)}")
                                st.stop()

                        new_event_data = {
                            "nombre": nombre,
                            "descripcion": descripcion,
                            "fecha_inicio": fecha_inicio,
                            "fecha_fin": fecha_fin,
                            "horario_inicio": horario_inicio,
                            "horario_fin": horario_fin,
                            "capacidad_maxima": capacidad_maxima,
                            "precio_entrada": precio_entrada,
                            "tipo_evento": tipo_evento,
                            "estado": estado,
                            "horario_complejo": horario_complejo_dict
                        }
                        created_evento = crud.create_evento(db, new_event_data)
                        st.success(f"Evento '{created_evento.nombre}' creado con éxito.")
                        st.write(created_evento)
                    except json.JSONDecodeError:
                        st.error("Horario Complejo debe ser un JSON válido.")
                    except Exception as e:
                        st.error(f"Error al crear evento: {e}")

        elif operation == "Ver Eventos":
            st.subheader("Lista de Eventos")
            eventos = crud.get_eventos(db)
            if eventos:
                evento_data = [
                    {
                        "ID": e.id_evento,
                        "Nombre": e.nombre,
                        "Descripción": e.descripcion,
                        "Fecha Inicio": e.fecha_inicio,
                        "Fecha Fin": e.fecha_fin,
                        "Hora Inicio": e.horario_inicio,
                        "Hora Fin": e.horario_fin,
                        "Capacidad": e.capacidad_maxima,
                        "Precio": e.precio_entrada,
                        "Tipo": e.tipo_evento,
                        "Estado": e.estado,
                        "Horario Complejo": e.horario_complejo
                    } for e in eventos
                ]
                st.dataframe(evento_data, use_container_width=True)
            else:
                st.info("No hay eventos registrados.")

        elif operation == "Actualizar Evento":
            st.subheader("Actualizar Evento Existente")
            eventos = crud.get_eventos(db)
            if eventos:
                evento_display_names = {f"{e.nombre} (ID: {e.id_evento})": e.id_evento for e in eventos}
                selected_evento_display = st.selectbox("Selecciona un evento para actualizar:", list(evento_display_names.keys()), key="update_evento_select")
                selected_evento_id = evento_display_names.get(selected_evento_display)

                if selected_evento_id:
                    evento_to_update = crud.get_evento(db, selected_evento_id)
                    if evento_to_update:
                        with st.form("update_evento_form"):
                            st.write(f"Actualizando evento: **{evento_to_update.nombre}**")
                            new_nombre = st.text_input("Nuevo Nombre", value=evento_to_update.nombre, key="evento_nombre_update")
                            new_descripcion = st.text_area("Nueva Descripción", value=evento_to_update.descripcion, key="evento_desc_update")
                            new_fecha_inicio = st.date_input("Nueva Fecha de Inicio", value=evento_to_update.fecha_inicio, key="evento_f_inicio_update")
                            new_fecha_fin = st.date_input("Nueva Fecha de Fin", value=evento_to_update.fecha_fin, key="evento_f_fin_update")
                            new_horario_inicio = st.time_input("Nuevo Horario de Inicio", value=evento_to_update.horario_inicio, key="evento_h_inicio_update")
                            new_horario_fin = st.time_input("Nuevo Horario de Fin", value=evento_to_update.horario_fin, key="evento_h_fin_update")
                            new_capacidad_maxima = st.number_input("Nueva Capacidad Máxima", value=evento_to_update.capacidad_maxima, min_value=1, key="evento_cap_update")
                            new_precio_entrada = st.number_input("Nuevo Precio de Entrada", value=float(evento_to_update.precio_entrada), min_value=0.0, format="%.2f", key="evento_precio_update")
                            new_tipo_evento = st.text_input("Nuevo Tipo de Evento", value=evento_to_update.tipo_evento, key="evento_tipo_update")
                            new_estado = st.selectbox("Nuevo Estado", ["programado", "activo", "finalizado", "cancelado"], index=["programado", "activo", "finalizado", "cancelado"].index(evento_to_update.estado), key="evento_estado_update")
                            
                            st.markdown("---")
                            st.write("**Horario Complejo (JSON)**")
                            st.info("Introduce un diccionario JSON válido. Ejemplo: `{'dias_semana': [1, 3], 'hora_inicio': '09:00:00', 'hora_fin': '12:00:00', 'duracion_minutos': 180, 'frecuencia': 'semanal'}`")
                            current_horario_complejo_str = str(evento_to_update.horario_complejo) if evento_to_update.horario_complejo else "{}"
                            new_horario_complejo_str = st.text_area("Horario Complejo (JSON)", value=current_horario_complejo_str, key="evento_horario_complejo_update")


                            update_submitted = st.form_submit_button("Actualizar Evento")
                            if update_submitted:
                                try:
                                    new_horario_complejo_dict = {}
                                    if new_horario_complejo_str.strip():
                                        import json
                                        new_horario_complejo_dict = json.loads(new_horario_complejo_str)
                                        # Basic validation for required keys
                                        required_keys = ["dias_semana", "hora_inicio", "hora_fin", "duracion_minutos", "frecuencia"]
                                        if not all(k in new_horario_complejo_dict for k in required_keys):
                                            st.error(f"Horario Complejo JSON debe contener las claves: {', '.join(required_keys)}")
                                            st.stop()
                                        
                                    update_data = {
                                        "nombre": new_nombre,
                                        "descripcion": new_descripcion,
                                        "fecha_inicio": new_fecha_inicio,
                                        "fecha_fin": new_fecha_fin,
                                        "horario_inicio": new_horario_inicio,
                                        "horario_fin": new_horario_fin,
                                        "capacidad_maxima": new_capacidad_maxima,
                                        "precio_entrada": new_precio_entrada,
                                        "tipo_evento": new_tipo_evento,
                                        "estado": new_estado,
                                        "horario_complejo": new_horario_complejo_dict
                                    }
                                    updated_evento = crud.update_evento(db, selected_evento_id, update_data)
                                    st.success(f"Evento '{updated_evento.nombre}' actualizado con éxito.")
                                    st.write(updated_evento)
                                except json.JSONDecodeError:
                                    st.error("Horario Complejo debe ser un JSON válido.")
                                except Exception as e:
                                    st.error(f"Error al actualizar evento: {e}")
                    else:
                        st.warning("Evento no encontrado.")
            else:
                st.info("No hay eventos para actualizar.")

        elif operation == "Eliminar Evento":
            st.subheader("Eliminar Evento")
            eventos = crud.get_eventos(db)
            if eventos:
                evento_display_names = {f"{e.nombre} (ID: {e.id_evento})": e.id_evento for e in eventos}
                selected_evento_display = st.selectbox("Selecciona un evento para eliminar:", list(evento_display_names.keys()), key="delete_evento_select")
                selected_evento_id = evento_display_names.get(selected_evento_display)

                if st.button("Eliminar Evento", key="delete_evento_button"):
                    if selected_evento_id:
                        try:
                            deleted_evento = crud.delete_evento(db, selected_evento_id)
                            if deleted_evento:
                                st.success(f"Evento '{deleted_evento.nombre}' eliminado con éxito.")
                            else:
                                st.warning("Evento no encontrado o ya eliminado.")
                        except Exception as e:
                            st.error(f"Error al eliminar evento: {e}")
                    else:
                        st.warning("Por favor, selecciona un evento.")
            else:
                st.info("No hay eventos para eliminar.")

except Exception as e:
    st.error(f"Ocurrió un error inesperado: {e}")
    db.rollback()
finally:
    db.close()