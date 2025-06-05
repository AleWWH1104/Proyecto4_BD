# app/main.py
from database import engine, Base, SessionLocal, get_db
from models import Animal, Evento, Habitat, Especie, TipoHabitat
from crud import crud
from datetime import date, time
from export_to_dataframe import export_all_to_dataframes, export_vistas_to_dataframes  # Modificado para incluir export_vistas_to_dataframes

def create_tables():
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente.")

def main():
    print("Iniciando pruebas CRUD...")

    # create_tables() # Comenta esta línea si ya tienes el esquema cargado por Docker

    db = next(get_db())

    try:
    

        print("\n=== INICIANDO EXPORTACIÓN A DATAFRAMES ===")
        try:
            dataframes = export_all_to_dataframes(db)
            
            print("\n=== RESUMEN DE DATOS EXPORTADOS ===")
            print(f"• Animales: {len(dataframes['animals'])} registros")
            print(f"• Eventos: {len(dataframes['eventos'])} registros")
            print(f"• Hábitats: {len(dataframes['habitats'])} registros")
            print("\nExportación completada exitosamente.")
            
        except Exception as e:
            print(f"\nError durante la exportación: {str(e)}")
            db.rollback()

        # --- Exportación de Vistas a DataFrames ---
        print("\n=== INICIANDO EXPORTACIÓN DE VISTAS A DATAFRAMES ===")
        try:
            vistas_df = export_vistas_to_dataframes(db)
            
            print("\n=== RESUMEN DE VISTAS EXPORTADAS ===")
            print(f"• Vista Financiera: {len(vistas_df['vista_financiera'])} registros")
            print(f"• Vista Conservación: {len(vistas_df['vista_conservacion'])} registros")
            print(f"• Vista Control Animal: {len(vistas_df['vista_control_animal'])} registros")
            print("\nExportación de vistas completada exitosamente.")
            
        except Exception as e:
            print(f"\nError durante la exportación de vistas: {str(e)}")
            db.rollback()

    except Exception as e:
        print(f"\nSe produjo un error general: {str(e)}")
        db.rollback()

if __name__ == "__main__":
    main()
