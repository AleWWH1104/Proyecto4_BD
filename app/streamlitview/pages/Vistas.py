
import sys
import os

# Añade el root del proyecto al path (sube 2 niveles desde este archivo)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from database import get_db
from export_to_dataframe import *
from crud.crud import *

import streamlit as st

st.set_page_config(layout="wide", page_title="Gestión de Zoológico - Vistas")


def app():
    st.title("Gestión de Zoológico - Vistas")
    
    db = next(get_db())
    try:
        a1 = vista_financiera_to_dataframe(db, get_vista_financiera_mensual(db))
        a2 = vista_conservacion_to_dataframe(db, get_vista_conservacion(db))
        a3 = vista_control_animal_to_dataframe(db, get_vista_control_animal(db))

        st.subheader("Vista Financiera")
        st.write(a1)

        st.subheader("Vista Conservacion")
        st.write(a2)

        st.subheader("Vista Control Animal")
        st.write(a3)

    except Exception as e:
        st.error(f"Error durante la exportación de datos: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    app()