import streamlit as st
from streamlit import session_state
from authentication.login import authenticate
from models.database import SessionLocal, Base
from models import Niño
from modules import home_page, data_management, new_diagnosis, diagnosis_history, resources_tools, settings
from constants.config import get_text, LANGUAGES
from datetime import date


def new_child_form(db, professional_dni, session_state):
    new_child = Niño()

    # Aquí reutilizamos la función child_form con el nuevo objeto Niño
    child_form(db, new_child, session_state, True)


def child_form(db, child, session_state, new_child=False):
    language = session_state.language

    form_key = f"form_{child.id_niño}" if not new_child else "new_child_form"
    with st.form(form_key):
        color, nombre, apellidos = st.columns([0.5, 2.5, 3])
        color = color.color_picker(get_text("DATA_MANAGEMENT_VARIABLES", language)["color"],
                                   value=child.color or "#b4cffa")
        nombre = nombre.text_input(get_text("DATA_MANAGEMENT_VARIABLES", language)["child_name"], value=child.nombre)
        apellidos = apellidos.text_input(get_text("DATA_MANAGEMENT_VARIABLES", language)["child_surname"],
                                         value=child.apellidos)

        left, right = st.columns(2)
        fecha_nacimiento = left.date_input(get_text("DATA_MANAGEMENT_VARIABLES", language)["date_of_birth"],
                                           value=child.fecha_nacimiento)
        genero = right.selectbox(get_text("DATA_MANAGEMENT_VARIABLES", language)["gender"],
                                 ["Masculino", "Femenino"],
                                 index=0 if child.genero is None else ["Masculino", "Femenino"].index(child.genero),
                                 key=f"gender_{child.id_niño}")

        antecedentes_familiares = left.selectbox(get_text("DATA_MANAGEMENT_VARIABLES", language)["family_history"],
                                                 ["Sí", "No"],
                                                 index=0 if child.antecedentes_familiares is None else ["Sí", "No"].index(
                                                     child.antecedentes_familiares), key=f"family_history_{child.id_niño}")
        diagnostico_previo = right.selectbox(get_text("DATA_MANAGEMENT_VARIABLES", language)["previous_diagnosis"],
                                             ["Sí", "No"],
                                             index=0 if child.diagnostico_previo is None else ["Sí", "No"].index(
                                                 child.diagnostico_previo), key=f"previous_diagnosis_{child.id_niño}")

        observaciones = st.text_area(get_text("DATA_MANAGEMENT_VARIABLES", language)["observations"],
                                     value=child.observaciones)

        if new_child:
            if st.form_submit_button("Añadir nuevo niño"):
                child.dni_profesional = session_state.professional_dni
                db.add(child)
                db.commit()
                st.success("Nuevo niño añadido con éxito")
                st.experimental_rerun()
        else:
            if st.form_submit_button(get_text("DATA_MANAGEMENT_VARIABLES", language)["update_child_data"]):
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
                st.success(get_text("DATA_MANAGEMENT_VARIABLES", language)["child_data_updated_success"])
                st.experimental_rerun()

def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def render_dashboard(session_state):
    db = SessionLocal()
    professional_dni = session_state.professional_dni
    children = db.query(Niño).filter(Niño.dni_profesional == professional_dni).all()

    for child in children:
        if child.id_niño not in session_state.expander_states:
            session_state.expander_states[child.id_niño] = False

        expander_state = session_state.expander_states[child.id_niño]
        with st.expander(f"{child.nombre} {child.apellidos}", expanded=expander_state):
            child_form(db, child, session_state)

def display_data_management(session_state):
    language = session_state.language
    st.subheader(get_text("MENU_ITEMS", language)["display_data_management"])

    add_new_child_button = st.button("Añadir nuevo niño", key="add_new_child_button")
    if add_new_child_button:
        st.modal(new_child_form, SessionLocal(), session_state.professional_dni, session_state)

    render_dashboard(session_state)

if __name__ == "__main__":
    display_data_management(session_state)

