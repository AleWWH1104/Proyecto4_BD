# app/reports_tests.py
from database import SessionLocal, get_db
from reports.reports import (
    get_reporte_animales_por_habitat,
    get_reporte_eventos_y_asistencia,
    get_reporte_alimentos_y_proveedores
)
from datetime import date, time

def main():
    print("Iniciando pruebas de reportes...")

    db = next(get_db()) # Obtener una sesión de base de datos

    try:
        print("\n--- Generando Reporte de Animales por Hábitat ---")
        # Caso 1: Reporte general sin filtros
        print("\n--- Reporte 1.1: Todos los animales en sus hábitats ---")
        df_animales_all = get_reporte_animales_por_habitat(
            db=db,
            export_csv=True,
            filename="reporte_animales_habitat_todos.csv"
        )
        print(f"Filas generadas: {len(df_animales_all)}")
        if not df_animales_all.empty:
            print(df_animales_all.head())

        # Caso 2: Reporte filtrado de animales por hábitat
        print("\n--- Reporte 1.2: Animales Macho con salud excelente en Bosque Tropical ---")
        df_animales_filtrado = get_reporte_animales_por_habitat(
            db=db,
            nombre_habitat="Jungla de Asia",
            tipo_habitat="Bosque Tropical",
            estado_habitat="activo",
            especie_nombre_comun="Tigre", # Buscar 'Tigre de Bengala'
            sexo_animal="M",
            estado_salud_animal="excelente",
            min_peso=150.0,
            max_peso=250.0,
            export_csv=True,
            filename="reporte_animales_habitat_filtrado.csv"
        )
        print(f"Filas generadas: {len(df_animales_filtrado)}")
        if not df_animales_filtrado.empty:
            print(df_animales_filtrado.head())
        else:
            print("No se encontraron animales con los filtros especificados para el reporte 1.2.")


        print("\n--- Generando Reporte de Eventos y Asistencia ---")
        # Caso 1: Reporte general de eventos
        print("\n--- Reporte 2.1: Todos los eventos y su asistencia ---")
        df_eventos_all = get_reporte_eventos_y_asistencia(
            db=db,
            export_csv=True,
            filename="reporte_eventos_asistencia_todos.csv"
        )
        print(f"Filas generadas: {len(df_eventos_all)}")
        if not df_eventos_all.empty:
            print(df_eventos_all.head())

        # Caso 2: Reporte filtrado de eventos con asistencia
        print("\n--- Reporte 2.2: Eventos educativos programados con asistencia de adultos guatemaltecos ---")
        df_eventos_filtrado = get_reporte_eventos_y_asistencia(
            db=db,
            fecha_inicio_desde=date(2025, 7, 1),
            fecha_inicio_hasta=date(2025, 8, 31),
            tipo_evento="educativo",
            estado_evento="programado",
            min_precio_entrada=0.0,
            max_precio_entrada=10.0,
            tipo_visitante="adulto",
            nacionalidad_visitante="Guatemalteca",
            evento_con_asistencia=True,
            export_csv=True,
            filename="reporte_eventos_asistencia_filtrado.csv"
        )
        print(f"Filas generadas: {len(df_eventos_filtrado)}")
        if not df_eventos_filtrado.empty:
            print(df_eventos_filtrado.head())
        else:
            print("No se encontraron eventos con los filtros especificados para el reporte 2.2.")


        print("\n--- Generando Reporte de Alimentos y Proveedores ---")
        # Caso 1: Reporte general de alimentos y proveedores
        print("\n--- Reporte 3.1: Todos los alimentos y sus proveedores ---")
        df_alimentos_all = get_reporte_alimentos_y_proveedores(
            db=db,
            export_csv=True,
            filename="reporte_alimentos_proveedores_todos.csv"
        )
        print(f"Filas generadas: {len(df_alimentos_all)}")
        if not df_alimentos_all.empty:
            print(df_alimentos_all.head())

        # Caso 2: Reporte filtrado de alimentos
        print("\n--- Reporte 3.2: Alimentos carnívoros de ZooFood S.A. con calificación 5, stock > 100, y con fecha de vencimiento en o antes de 2025-07-15 o costo hasta 12.00 ---")
        df_alimentos_filtrado = get_reporte_alimentos_y_proveedores(
            db=db,
            nombre_alimento="Carne",
            tipo_alimento="carnivoro",
            nombre_proveedor="ZooFood S.A.",
            tipo_proveedor="alimentos",
            calificacion_proveedor_min=5,
            stock_actual_min=100,
            fecha_vencimiento_antes=date(2025, 12, 31), # Esto debería incluir 'Carne de Res Magra' e 'Insectos Vivo'
            costo_por_kg_max=12.00, # Esto debería incluir 'Insectos Vivo'
            export_csv=True,
            filename="reporte_alimentos_proveedores_filtrado.csv"
        )
        print(f"Filas generadas: {len(df_alimentos_filtrado)}")
        if not df_alimentos_filtrado.empty:
            print(df_alimentos_filtrado.head())
        else:
            print("No se encontraron alimentos con los filtros especificados para el reporte 3.2.")

    except Exception as e:
        print(f"Ocurrió un error durante las pruebas de reportes: {e}")
        db.rollback()
    finally:
        db.close()
        print("\nPruebas de reportes finalizadas.")

if __name__ == "__main__":
    main()