
import sys
import os

# Añade el root del proyecto al path (sube 2 niveles desde este archivo)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from database import get_db
from export_to_dataframe import *
from crud.crud import *

import streamlit as st

def app():
    st.title("DataFrames de Animales, Eventos y Hábitats")

    db = next(get_db())
    try:
        a1 = vista_financiera_to_dataframe(db, get_vista_financiera_mensual(db))
        a2 = vista_conservacion_to_dataframe(db, get_vista_conservacion(db))
        a3 = vista_control_animal_to_dataframe(db, get_vista_control_animal(db))

        st.subheader("Vista Financiera (a1)")
        st.write(a1)

        st.subheader("Vista Conservacion (a2)")
        st.write(a2)

        st.subheader("Vista Control Animal (a3)")
        st.write(a3)

    except Exception as e:
        st.error(f"Error durante la exportación de datos: {str(e)}")
        db.rollback()
    finally:
        db.close() # Ensure the database connection is closed

if __name__ == "__main__":
    app()