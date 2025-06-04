# app/main.py
from database import engine, Base, SessionLocal, get_db
from models import Animal, Evento, Habitat, Especie, TipoHabitat
from crud import crud
from crud import crudvista
from datetime import date, time
import uuid # Para generar IDs únicos

def main():
    print("Iniciando pruebas CRUD y de Vistas...")

    # create_tables() # Esta función crea las tablas; Docker ya lo hace con 01_schema.sql.
                      # Mantenla comentada a menos que modifiques los modelos y necesites recrear.

    db = next(get_db())

    try:
        # --- PRUEBAS DE CREACIÓN DE UN NUEVO REGISTRO PARA PROBAR CRUD ---
        # Estos son ejemplos para probar la funcionalidad CREATE del CRUD.
        # Se generarán con identificadores únicos para no chocar con 05_data.sql.

        print("\n--- Creación de un nuevo registro para probar CRUD (evitando duplicados) ---")
        
        # Obtener una especie y un tipo de hábitat existentes de la base de datos
        # Asumiendo que 05_data.sql ya insertó estos, los obtenemos para FKs.
        especie_existente = db.query(Especie).filter_by(nombre_cientifico="Panthera tigris").first()
        if not especie_existente:
            print("ERROR: Especie 'Panthera tigris' no encontrada. Asegúrate de que 05_data.sql se ha ejecutado.")
            return
        
        tipo_habitat_existente = db.query(TipoHabitat).filter_by(nombre="Bosque Tropical").first()
        if not tipo_habitat_existente:
            print("ERROR: Tipo de Hábitat 'Bosque Tropical' no encontrado. Asegúrate de que 05_data.sql se ha ejecutado.")
            return

        # 1. Crear un NUEVO Hábitat para pruebas
        print("\n--- Crear NUEVO Hábitat ---")
        unique_habitat_name = f"Hábitat Prueba {uuid.uuid4().hex[:6]}"
        new_habitat_data = {
            "nombre": unique_habitat_name,
            "id_tipo_habitat": tipo_habitat_existente.id_tipo_habitat,
            "ubicacion": {"latitud": 10.1234, "longitud": 20.5678, "altitud": 100},
            "capacidad_maxima": 2,
            "area_metros_cuadrados": 150.0,
            "fecha_construccion": date(2023, 1, 1),
            "estado": "activo",
            "costo_mantenimiento_mensual": 300.00
        }
        new_test_habitat = crud.create_habitat(db, new_habitat_data)
        print(f"Nuevo hábitat de prueba creado: {new_test_habitat}")

        # 2. Crear un NUEVO Animal para pruebas
        print("\n--- Crear NUEVO Animal ---")
        new_animal_id = f"TEST-ANI-{uuid.uuid4().hex[:6]}"
        new_animal_data = {
            "nombre": "Prueba Animal",
            "id_especie": especie_existente.id_especie,
            "id_habitat": new_test_habitat.id_habitat, # Usamos el hábitat recién creado
            "fecha_nacimiento": date(2024, 2, 1),
            "sexo": "M",
            "peso_actual": 50.0,
            "altura": 0.8,
            "numero_identificacion": new_animal_id,
            "origen": "rescate",
            "estado_salud": "bueno"
        }
        new_test_animal = crud.create_animal(db, new_animal_data)
        print(f"Nuevo animal de prueba creado: {new_test_animal}")

        # 3. Crear un NUEVO Evento para pruebas
        print("\n--- Crear NUEVO Evento ---")
        new_event_name = f"Evento de Prueba {uuid.uuid4().hex[:6]}"
        new_event_data = {
            "nombre": new_event_name,
            "descripcion": "Evento de prueba para verificar CRUD.",
            "fecha_inicio": date(2026, 1, 1),
            "fecha_fin": date(2026, 1, 1),
            "horario_inicio": time(15, 0),
            "horario_fin": time(16, 0),
            "capacidad_maxima": 10,
            "precio_entrada": 1.00,
            "tipo_evento": "especial",
            "estado": "programado",
            "horario_complejo": {
                "dias_semana": [1], 
                "hora_inicio": "15:00:00", 
                "hora_fin": "16:00:00",
                "duracion_minutos": 60,
                "frecuencia": "una_vez"
            }
        }
        new_test_evento = crud.create_evento(db, new_event_data)
        print(f"Nuevo evento de prueba creado: {new_test_evento}")


        # --- PRUEBAS DE LECTURA (READ) ---
        print("\n--- Pruebas de Lectura (READ) ---")

        print("\n--- Leyendo Hábitats ---")
        all_habitats = crud.get_habitats(db)
        print(f"Total de hábitats: {len(all_habitats)}")
        for i, h in enumerate(all_habitats[:5]): # Muestra los primeros 5 para no saturar
            print(f"  [{i+1}] - {h.nombre}, Estado: {h.estado}")
        if len(all_habitats) > 5:
            print(f"  ... y {len(all_habitats) - 5} más.")

        print("\n--- Leyendo Animales ---")
        all_animals = crud.get_animals(db)
        print(f"Total de animales: {len(all_animals)}")
        for i, a in enumerate(all_animals[:5]): # Muestra los primeros 5
            print(f"  [{i+1}] - {a.nombre} ({a.numero_identificacion}), Salud: {a.estado_salud}")
        if len(all_animals) > 5:
            print(f"  ... y {len(all_animals) - 5} más.")

        print("\n--- Leyendo Eventos ---")
        all_eventos = crud.get_eventos(db)
        print(f"Total de eventos: {len(all_eventos)}")
        for i, e in enumerate(all_eventos[:5]): # Muestra los primeros 5
            print(f"  [{i+1}] - {e.nombre}, Fecha: {e.fecha_inicio}, Estado: {e.estado}")
        if len(all_eventos) > 5:
            print(f"  ... y {len(all_eventos) - 5} más.")


        # --- PRUEBAS DE ACTUALIZACIÓN (UPDATE) ---
        print("\n--- Pruebas de Actualización (UPDATE) ---")

        print("\n--- Actualizando el Hábitat de Prueba ---")
        update_data_habitat = {"estado": "mantenimiento", "costo_mantenimiento_mensual": 350.00}
        updated_test_habitat = crud.update_habitat(db, new_test_habitat.id_habitat, update_data_habitat)
        print(f"Hábitat de prueba actualizado: {updated_test_habitat}")

        print("\n--- Actualizando el Animal de Prueba ---")
        update_data_animal = {"peso_actual": 52.5, "estado_salud": "excelente"}
        updated_test_animal = crud.update_animal(db, new_test_animal.id_animal, update_data_animal)
        print(f"Animal de prueba actualizado: {updated_test_animal}")

        print("\n--- Actualizando el Evento de Prueba ---")
        update_data_evento = {"precio_entrada": 1.50, "estado": "finalizado"}
        updated_test_evento = crud.update_evento(db, new_test_evento.id_evento, update_data_evento)
        print(f"Evento de prueba actualizado: {updated_test_evento}")


        # --- PRUEBAS DE LECTURA DE VISTAS (USANDO crudvista) ---
        print("\n--- Pruebas de Lectura de Vistas ---")

        print("\n--- Vista Financiera Mensual ---")
        finanzas = crudvista.get_vista_financiera_mensual(db)
        if finanzas:
            for f in finanzas:
                print(f"  - {f}")
        else:
            print("No hay datos en VistaFinancieraMensual. Asegúrate de tener registros en tablas de ingresos/gastos.")

        print("\n--- Vista de Conservación (Especies Amenazadas) ---")
        conservacion_data = crudvista.get_vista_conservacion(db)
        if conservacion_data:
            for c in conservacion_data:
                print(f"  - {c}")
        else:
            print("No hay datos en VistaConservacion.")

        print("\n--- Vista de Control Animal ---")
        control_animal_data = crudvista.get_vista_control_animal(db)
        if control_animal_data:
            for ca in control_animal_data:
                print(f"  - {ca}")
        else:
            print("No hay datos en VistaControlAnimal.")


        # --- PRUEBAS DE ELIMINACIÓN (DELETE) ---
        # Siempre es buena práctica eliminar los registros creados por la prueba al final
        # para mantener la base de datos limpia de "basura" de pruebas si no usas volúmenes desechables.
        print("\n--- Pruebas de Eliminación (DELETE) ---")
        
        # Eliminar Animal de Prueba
        deleted_animal = crud.delete_animal(db, new_test_animal.id_animal)
        if deleted_animal:
            print(f"Animal de prueba eliminado: {deleted_animal}")
        else:
            print(f"No se pudo eliminar el animal de prueba con ID: {new_test_animal.id_animal}")

        # Eliminar Evento de Prueba
        deleted_evento = crud.delete_evento(db, new_test_evento.id_evento)
        if deleted_evento:
            print(f"Evento de prueba eliminado: {deleted_evento}")
        else:
            print(f"No se pudo eliminar el evento de prueba con ID: {new_test_evento.id_evento}")

        # Eliminar Hábitat de Prueba
        # Asegúrate de que no haya animales referenciando este hábitat antes de eliminarlo
        # (ya eliminamos el animal de prueba, así que no debería haber problemas con ese).
        deleted_habitat = crud.delete_habitat(db, new_test_habitat.id_habitat)
        if deleted_habitat:
            print(f"Hábitat de prueba eliminado: {deleted_habitat}")
        else:
            print(f"No se pudo eliminar el hábitat de prueba con ID: {new_test_habitat.id_habitat}")


    except Exception as e:
        print(f"Ocurrió un error durante las pruebas: {e}")
        db.rollback() 
    finally:
        db.close()
        print("\nPruebas CRUD y de Vistas finalizadas.")

if __name__ == "__main__":
    main()