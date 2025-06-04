# app/main.py
from database import engine, Base, SessionLocal, get_db
from models import Animal, Evento, Habitat, Especie, TipoHabitat
from crud import crud
from datetime import date, time

def create_tables():
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente.")

def main():
    print("Iniciando pruebas CRUD...")

    # create_tables() # Comenta esta línea si ya tienes el esquema cargado por Docker

    db = next(get_db())

    try:
        # --- Pruebas para Especies y Tipos de Hábitat (necesarias para Animales y Habitats) ---
        print("\n--- Creando datos base (Especie y TipoHabitat) ---")
        nueva_especie_data = {
            "nombre_cientifico": "Panthera leo",
            "nombre_comun": "León",
            "reino": "Animalia",
            "clase": "Mammalia",
            "estado_conservacion": "vulnerable",
            "esperanza_vida": 15,
            "peso_promedio": 190.0
        }
        especie_leon = db.query(Especie).filter_by(nombre_cientifico="Panthera leo").first()
        if not especie_leon:
            especie_leon = Especie(**nueva_especie_data)
            db.add(especie_leon)
            db.commit()
            db.refresh(especie_leon)
            print(f"Especie creada: {especie_leon}")
        else:
            print(f"Especie 'León' ya existe: {especie_leon}")

        nuevo_tipo_habitat_data = {
            "nombre": "Sabana Africana",
            "descripcion": "Hábitat abierto con pastizales.",
            "temperatura_min": 20.0,
            "temperatura_max": 35.0,
            "humedad_min": 30.0,
            "humedad_max": 60.0
        }
        tipo_habitat_sabana = db.query(TipoHabitat).filter_by(nombre="Sabana Africana").first()
        if not tipo_habitat_sabana:
            tipo_habitat_sabana = TipoHabitat(**nuevo_tipo_habitat_data)
            db.add(tipo_habitat_sabana)
            db.commit()
            db.refresh(tipo_habitat_sabana)
            print(f"Tipo de Hábitat creado: {tipo_habitat_sabana}")
        else:
            print(f"Tipo de Hábitat 'Sabana Africana' ya existe: {tipo_habitat_sabana}")


        # --- Pruebas CRUD para Habitats ---
        print("\n--- Pruebas CRUD para Habitats ---")

        # 1. Crear Hábitat
        print("\n--- Crear Hábitat ---")
        habitat_data = {
            "nombre": "Recinto de Leones",
            "id_tipo_habitat": tipo_habitat_sabana.id_tipo_habitat,
            "ubicacion": {"latitud": -1.2921, "longitud": 36.8219, "altitud": 1795},
            "capacidad_maxima": 5,
            "area_metros_cuadrados": 500.0,
            "fecha_construccion": date(2020, 1, 15),
            "estado": "activo",
            "costo_mantenimiento_mensual": 1200.50
        }
        nuevo_habitat = crud.create_habitat(db, habitat_data)
        print(f"Hábitat creado: {nuevo_habitat}")

        # 2. Leer Hábitat por ID
        print("\n--- Leer Hábitat ---")
        habitat_leido = crud.get_habitat(db, nuevo_habitat.id_habitat)
        print(f"Hábitat leído: {habitat_leido}")

        # 3. Actualizar Hábitat
        print("\n--- Actualizar Hábitat ---")
        update_data_habitat = {"estado": "mantenimiento", "costo_mantenimiento_mensual": 1500.00}
        habitat_actualizado = crud.update_habitat(db, nuevo_habitat.id_habitat, update_data_habitat)
        print(f"Hábitat actualizado: {habitat_actualizado}")

        # 4. Obtener todos los Hábitats
        print("\n--- Obtener todos los Hábitats ---")
        all_habitats = crud.get_habitats(db)
        for h in all_habitats:
            print(f"  - {h}")


        # --- Pruebas CRUD para Animales ---
        print("\n--- Pruebas CRUD para Animales ---")

        # 1. Crear Animal (o obtener si ya existe)
        print("\n--- Crear Animal ---")
        animal_numero_identificacion = "LEO-001" # Define el número de identificación
        
        # Primero, intenta buscar el animal por su número de identificación
        existente_animal = db.query(Animal).filter_by(numero_identificacion=animal_numero_identificacion).first()

        if existente_animal:
            nuevo_animal = existente_animal
            print(f"Animal '{animal_numero_identificacion}' ya existe: {nuevo_animal}")
        else:
            animal_data = {
                "nombre": "Simba",
                "id_especie": especie_leon.id_especie,
                "id_habitat": nuevo_habitat.id_habitat,
                "fecha_nacimiento": date(2021, 5, 10),
                "sexo": "M",
                "peso_actual": 180.5,
                "altura": 1.2,
                "numero_identificacion": animal_numero_identificacion, # Usa la variable
                "origen": "nacido_zoologico",
                "estado_salud": "excelente"
            }
            nuevo_animal = crud.create_animal(db, animal_data)
            print(f"Animal creado: {nuevo_animal}")

        # 2. Leer Animal por ID
        print("\n--- Leer Animal ---")
        animal_leido = crud.get_animal(db, nuevo_animal.id_animal)
        print(f"Animal leído: {animal_leido}")

        # 3. Actualizar Animal
        print("\n--- Actualizar Animal ---")
        update_data_animal = {"peso_actual": 195.0, "estado_salud": "bueno"}
        animal_actualizado = crud.update_animal(db, nuevo_animal.id_animal, update_data_animal)
        print(f"Animal actualizado: {animal_actualizado}")

        # 4. Obtener todos los Animales
        print("\n--- Obtener todos los Animales ---")
        all_animals = crud.get_animals(db)
        for a in all_animals:
            print(f"  - {a}")


        # --- Pruebas CRUD para Eventos ---
        print("\n--- Pruebas CRUD para Eventos ---")

        # 1. Crear Evento
        print("\n--- Crear Evento ---")
        evento_data = {
            "nombre": "Charla sobre Leones",
            "descripcion": "Una charla educativa sobre el comportamiento de los leones.",
            "fecha_inicio": date(2025, 7, 10),
            "fecha_fin": date(2025, 7, 10),
            "horario_inicio": time(10, 0),
            "horario_fin": time(11, 0),
            "capacidad_maxima": 30,
            "precio_entrada": 5.00,
            "tipo_evento": "educativo",
            "estado": "programado",
            # Asegúrate que el formato de 'hora_inicio' y 'hora_fin' aquí sea de cadena para el TypeDecorator
            "horario_complejo": {
                "dias_semana": [4], # Jueves
                "hora_inicio": "10:00:00", 
                "hora_fin": "11:00:00",
                "duracion_minutos": 60,
                "frecuencia": "semanal"
            }
        }
        nuevo_evento = crud.create_evento(db, evento_data)
        print(f"Evento creado: {nuevo_evento}")

        # 2. Leer Evento por ID
        print("\n--- Leer Evento ---")
        evento_leido = crud.get_evento(db, nuevo_evento.id_evento)
        print(f"Evento leído: {evento_leido}")

        # 3. Actualizar Evento
        print("\n--- Actualizar Evento ---")
        update_data_evento = {"precio_entrada": 7.50, "estado": "en_curso"}
        evento_actualizado = crud.update_evento(db, nuevo_evento.id_evento, update_data_evento)
        print(f"Evento actualizado: {evento_actualizado}")

        # 4. Obtener todos los Eventos
        print("\n--- Obtener todos los Eventos ---")
        all_eventos = crud.get_eventos(db)
        for e in all_eventos:
            print(f"  - {e}")

        # --- Eliminar (opcional, para limpiar) ---
        print("\n--- Limpiando datos (Eliminando) ---")
        #delete_animal(db, nuevo_animal.id_animal)
        #delete_evento(db, nuevo_evento.id_evento)
        #delete_habitat(db, nuevo_habitat.id_habitat)
        #print("Registros eliminados.")

    except Exception as e:
        print(f"Ocurrió un error durante las pruebas: {e}")
        db.rollback() # En caso de error, haz rollback
    finally:
        db.close()
        print("\nPruebas CRUD finalizadas.")

if __name__ == "__main__":
    main()