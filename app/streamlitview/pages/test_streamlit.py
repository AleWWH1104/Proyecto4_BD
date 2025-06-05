# app/streamlitview/home.py
import sys
import os

# Añade el root del proyecto al path (sube 2 niveles desde este archivo)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from database import get_db
from export_to_dataframe import export_all_to_dataframes, eventos_to_dataframe, habitats_to_dataframe, animals_to_dataframe
from crud.crud import get_animals, get_eventos, get_habitats

import streamlit as st

def app():
    st.title("DataFrames de Animales, Eventos y Hábitats")

    db = next(get_db())
    try:
        a1 = animals_to_dataframe(db, get_animals(db))
        a2 = eventos_to_dataframe(db, get_eventos(db))
        a3 = habitats_to_dataframe(db, get_habitats(db))

        st.subheader("DataFrame de Animales (a1)")
        st.write(a1)

        st.subheader("DataFrame de Eventos (a2)")
        st.write(a2)

        st.subheader("DataFrame de Hábitats (a3)")
        st.write(a3)

    except Exception as e:
        st.error(f"Error durante la exportación de datos: {str(e)}")
        db.rollback()
    finally:
        db.close() # Ensure the database connection is closed

if __name__ == "__main__":
    app()