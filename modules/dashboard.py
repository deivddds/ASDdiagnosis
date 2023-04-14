import streamlit as st
from models.child import Niño
from models.diagnosis import Diagnosis
from datetime import date
from sqlalchemy.orm import Session
from models.database import SessionLocal, Base

def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def child_form(child: Niño):
    db = SessionLocal()

    with st.form(f"form_{child.id_niño}"):
        color, nombre, apellidos = st.columns([0.5,2.5,3])
        color = color.color_picker("Color", value=child.color or "#b4cffa")
        nombre = nombre.text_input("Nombre", value=child.nombre)
        apellidos = apellidos.text_input("Apellidos", value=child.apellidos)

        left, right = st.columns(2)
        fecha_nacimiento = left.date_input("Fecha de nacimiento", value=child.fecha_nacimiento)
        genero = right.selectbox("Género", ["Masculino", "Femenino"], index=0 if child.genero is None else ["Masculino", "Femenino"].index(child.genero))

        antecedentes_familiares = left.selectbox("Antecedentes familiares", ["Sí", "No"], index=0 if child.antecedentes_familiares is None else ["Sí", "No"].index(child.antecedentes_familiares))
        diagnostico_previo = right.selectbox("Diagnóstico previo", ["Sí", "No"], index=0 if child.diagnostico_previo is None else ["Sí", "No"].index(child.diagnostico_previo))

        observaciones = st.text_area("Observaciones", value=child.observaciones)

        if st.form_submit_button("Actualizar datos del niño"):
            child.nombre = nombre
            child.apellidos = apellidos
            child.fecha_nacimiento = fecha_nacimiento
            child.genero = genero
            child.antecedentes_familiares = 'Sí' if antecedentes_familiares == 'Sí' else 'No'
            child.diagnostico_previo = 'Sí' if diagnostico_previo == 'Sí' else 'No'
            child.observaciones = observaciones
            child.color = color
            db.merge(child)
            db.commit()
            st.success("Datos del niño actualizados con éxito")
            st.experimental_rerun()

def render_dashboard():
    st.title("Dashboard")
    st.subheader("Niños asociados al profesional")

    db = SessionLocal()

    # Lista de niños asociados al profesional
    children = db.query(Niño).filter(Niño.dni_profesional == st.session_state.dni).all()

    # Tarjetas de niños
    for child in children:
        # Datos del niño
        nombre = child.nombre
        edad = calculate_age(child.fecha_nacimiento)

        # Mostrar tarjeta
        with st.expander(f"{nombre} ({edad} años) - Último diagnóstico: 'N/A'"):
            # Aquí puede agregar más información sobre el niño y sus diagnósticos, si es necesario
            child_form(child)

    # Botones en la esquina superior derecha
    col1, col2 = st.columns(2)
    with col1:
        st.button("Añadir niño")

    # Barra de navegación
    st.sidebar.title("Navegación")
    st.sidebar.markdown("**[Inicio (Dashboard)](javascript:void(0);)**", unsafe_allow_html=True)
    st.sidebar.markdown("**[Perfil del profesional](javascript:void(0);)**", unsafe_allow_html=True)
    st.sidebar.markdown("**[Cerrar sesión](javascript:void(0);)**", unsafe_allow_html=True)
