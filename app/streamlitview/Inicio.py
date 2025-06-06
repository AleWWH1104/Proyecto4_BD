import streamlit as st

st.set_page_config(layout="centered", page_title="Página Principal Peluzoo")

st.title("Página Principal Peluzoo")
st.write("Bienvenido/a a la aplicación de gestión integral del zoológico **Peluzoo**!")
st.write("Aquí podrás interactuar con los datos de nuestro sistema, desde la información de animales y hábitats hasta el seguimiento de eventos y la generación de reportes detallados.")

st.markdown("---")

st.header("Sobre el Proyecto")
st.write(
    "Este proyecto es una implementación del **Proyecto 4 - Bases de Datos**, que consiste en diseñar y desarrollar un **sistema de gestión universitaria integral utilizando un ORM (Object-Relational Mapper)**. "
    "El sistema incluye diversos módulos, estructurados con **más de 20 tablas normalizadas**, lo que garantiza la eficiencia y la integridad de los datos. "
    "Además, incorpora **validaciones complejas** para asegurar la calidad de la información y ofrece **funcionalidades de reportes** que permiten un análisis profundo de los datos."
)
st.write(
    "En el contexto de Peluzoo, este sistema se ha adaptado para gestionar de manera efectiva todos los aspectos de un zoológico moderno, "
    "permitiendo un control exhaustivo sobre animales, hábitats, eventos y recursos."
)

st.markdown("---")

st.header("Desarrollado por:")
st.markdown("""
* **Iris Ayala** - 23965
* **Gabriel Bran** - 23590
* **David Dominguez** - 23712
* **Jonathan Díaz** - 23837
* **Anggie Quezada** - 23643
""")