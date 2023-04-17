import streamlit as st
import concurrent.futures
import time
from streamlit import session_state
from models.database import SessionLocal, Base
from models import Niño
from constants.config import get_text, LANGUAGES
from datetime import date
from sqlalchemy import Insert
import urllib.parse

if "submit_attempt" not in st.session_state:
    st.session_state.submit_attempt = 0

def store_errors(errors):
    return errors
    
def form_fields(child, language, is_new_child):
    color, nombre, apellidos = st.columns([1, 2, 3])
    color = color.color_picker(get_text("DATA_MANAGEMENT_VARIABLES", language)["color"],
                               value=child.color or "#b4cffa" if not is_new_child else "#b4cffa")
    nombre = nombre.text_input(get_text("DATA_MANAGEMENT_VARIABLES", language)["child_name"], value=child.nombre if not is_new_child else "")
    apellidos = apellidos.text_input(get_text("DATA_MANAGEMENT_VARIABLES", language)["child_surname"],
                                     value=child.apellidos if not is_new_child else "")

    left, right = st.columns(2)
    fecha_nacimiento = left.date_input(get_text("DATA_MANAGEMENT_VARIABLES", language)["date_of_birth"],
                                       value=child.fecha_nacimiento if not is_new_child else date.today())
    genero = right.selectbox(get_text("DATA_MANAGEMENT_VARIABLES", language)["gender"],
                             ["Masculino", "Femenino"],
                             index=0 if child.genero is None else ["Masculino", "Femenino"].index(child.genero),
                             key=f"gender_{child.id_niño if not is_new_child else 'new_child'}")

    antecedentes_familiares = left.selectbox(get_text("DATA_MANAGEMENT_VARIABLES", language)["family_history"],
                                             ["Sí", "No"],
                                             index=0 if child.antecedentes_familiares is None else ["Sí", "No"].index(
                                                 child.antecedentes_familiares), key=f"family_history_{child.id_niño if not is_new_child else 'new_child'}")
    diagnostico_previo = right.selectbox(get_text("DATA_MANAGEMENT_VARIABLES", language)["previous_diagnosis"],
                                         ["Sí", "No"],
                                         index=0 if child.diagnostico_previo is None else ["Sí", "No"].index(
                                             child.diagnostico_previo), key=f"previous_diagnosis_{child.id_niño if not is_new_child else 'new_child'}")

    observaciones = st.text_area(get_text("DATA_MANAGEMENT_VARIABLES", language)["observations"],
                                 value=child.observaciones if not is_new_child else "")
    return color, nombre, apellidos, fecha_nacimiento, genero, antecedentes_familiares, diagnostico_previo, observaciones

def show_form_message(session_state, message_key, message_type, message):
    if message_key not in session_state.form_messages:
        session_state.form_messages[message_key] = (message_type, message, time.time())
        return True
    else:
        _, _, timestamp = session_state.form_messages[message_key]
        if time.time() - timestamp > 2:
            del session_state.form_messages[message_key]
            return False
        return True


def is_form_valid(nombre, apellidos, fecha_nacimiento, genero):
    errors = []
    if not (nombre and apellidos and fecha_nacimiento and genero):
        errors.append("Por favor, complete todos los campos obligatorios.")

    if fecha_nacimiento >= date.today():
        errors.append("La fecha de nacimiento debe ser anterior al día de hoy.")

    return store_errors(errors)

def show_temporary_message(session, message_type, message, duration=3):
    session.write(f"<div id='temporary-message' style='color: {message_type};'>{message}</div>", unsafe_allow_html=True)
    time.sleep(duration)
    session.write("<script>document.getElementById('temporary-message').remove()</script>", unsafe_allow_html=True)


def show_spinner(wait_time):
    with st.spinner("Creando niño..."):
        time.sleep(wait_time)

def child_form_create(db, session_state):
    language = session_state.language
    new_child = Niño()

    with st.form("new_child_form"):
        color, nombre, apellidos, fecha_nacimiento, genero, antecedentes_familiares, diagnostico_previo, observaciones = form_fields(new_child, language, True)

        submit_button = st.form_submit_button("Añadir nuevo niño")

        if submit_button:
            errors = is_form_valid(nombre, apellidos, fecha_nacimiento, genero)
            if not errors:
                new_child.nombre = nombre
                new_child.apellidos = apellidos
                new_child.fecha_nacimiento = fecha_nacimiento
                new_child.genero = genero
                new_child.antecedentes_familiares = antecedentes_familiares
                new_child.diagnostico_previo = diagnostico_previo
                new_child.observaciones = observaciones
                new_child.color = color
                new_child.dni_profesional = session_state.professional_dni
                db.add(new_child)

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    try:
                        db.commit()
                        st.success(get_text("DATA_MANAGEMENT_VARIABLES", session_state.language)["child_data_created_success"])
                        st.experimental_rerun()
                    except Exception as e:
                        db.rollback()
                        if not session_state.first_time:
                            st.error(get_text("DATA_MANAGEMENT_VARIABLES", session_state.language)["child_data_create_error"].format(e))
                        else:
                            try:
                                db.commit()
                                st.success(get_text("DATA_MANAGEMENT_VARIABLES", session_state.language)["child_data_created_success"])
                            except Exception as e:
                                db.rollback()
                                st.error(get_text("DATA_MANAGEMENT_VARIABLES", session_state.language)["child_data_create_error"].format(e))
                                st.experimental_rerun()

            else:
                for error in errors:
                    st.error(error)
        # elif any([nombre, apellidos, fecha_nacimiento, genero, antecedentes_familiares, diagnostico_previo, observaciones]):
        #     st.warning("Por favor, complete todos los campos obligatorios.")



def child_form_update(db, child, session_state):
    language = session_state.language

    with st.form(f"form_{child.id_niño}"):
        color, nombre, apellidos, fecha_nacimiento, genero, antecedentes_familiares, diagnostico_previo, observaciones = form_fields(child, language, False)

        submit_button = st.form_submit_button("Actualizar niño")

        if submit_button:
            if is_form_valid(nombre, apellidos, fecha_nacimiento, genero):
                child.nombre = nombre
                child.apellidos = apellidos
                child.fecha_nacimiento = fecha_nacimiento
                child.genero = genero
                child.antecedentes_familiares = antecedentes_familiares
                child.diagnostico_previo = diagnostico_previo
                child.observaciones = observaciones
                child.color = color

                try:
                    db.commit()
                    st.success(get_text("DATA_MANAGEMENT_VARIABLES", session_state.language)["child_data_updated_success"])
                    st.experimental_rerun()
                except Exception as e:
                    db.rollback()
                    st.error(get_text("DATA_MANAGEMENT_VARIABLES", session_state.language)["child_data_update_error"].format(e))
            else:
                st.error("Por favor, complete todos los campos obligatorios.")


def render_dashboard(session_state):
    if session_state.operation_result:
        st.success(session_state.operation_result)
        session_state.operation_result = ""

    db = SessionLocal()
    professional_dni = session_state.professional_dni
    children = db.query(Niño).filter(Niño.dni_profesional == professional_dni).all()

    st.sidebar.markdown("___")
    st.sidebar.subheader(get_text("MENU_ITEMS", session_state.language)["display_data_management"])

    with st.sidebar.expander(get_text("DATA_MANAGEMENT_VARIABLES", session_state.language)["child_form_expander"]):
        child_form_create(db, session_state)

    for child in children:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            with st.expander(f"{child.nombre} {child.apellidos}"):
                child_form_update(db, child, session_state)
        with col2:
            with st.expander("", expanded=False):
                st.write("Diagnóstico del niño")
        with col3:
            if st.button(get_text("DATA_MANAGEMENT_VARIABLES", session_state.language)["delete_child"], key=f"delete_child_{child.id_niño}"):
                delete_child(db, child.id_niño, session_state)

def display_data_management(session_state):
    language = session_state.language
    st.subheader(get_text("MENU_ITEMS", language)["display_data_management"])

    render_dashboard(session_state)

def delete_child(db, child_id, session_state):
    pass

if __name__ == "__main__":
    display_data_management(session_state)