import streamlit as st
from streamlit import session_state
from authentication.login import authenticate
from models.database import SessionLocal, Base
from models import Niño
from modules import home_page, data_management, new_diagnosis, diagnosis_history, resources_tools, settings
from constants.config import get_text, LANGUAGES
from datetime import date

##comprobar si se usa esta funcion si no eliminar
def new_child_form(db, professional_dni, session_state):
    new_child = Niño()

    # Aquí reutilizamos la función child_form con el nuevo objeto Niño
    child_form(db, new_child, session_state, True)


def child_form(db, child, session_state, new_child=False):
    language = session_state.language

    form_key = f"form_{child.id_niño}" if not new_child else "new_child_form"
    with st.form(form_key):
        color, nombre, apellidos = st.columns([1, 2, 3])
        color = color.color_picker(get_text("DATA_MANAGEMENT_VARIABLES", language)["color"],
                                   value=child.color or "#b4cffa" if not new_child else "#b4cffa")
        nombre = nombre.text_input(get_text("DATA_MANAGEMENT_VARIABLES", language)["child_name"], value=child.nombre if not new_child else "")
        apellidos = apellidos.text_input(get_text("DATA_MANAGEMENT_VARIABLES", language)["child_surname"],
                                         value=child.apellidos if not new_child else "")

        left, right = st.columns(2)
        fecha_nacimiento = left.date_input(get_text("DATA_MANAGEMENT_VARIABLES", language)["date_of_birth"],
                                           value=child.fecha_nacimiento if not new_child else date.today())
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
                                     value=child.observaciones if not new_child else "")

        if st.form_submit_button("Añadir nuevo niño" if new_child else get_text("DATA_MANAGEMENT_VARIABLES", language)["update_child_data"]):
            child.nombre = nombre
            child.apellidos = apellidos
            child.fecha_nacimiento = fecha_nacimiento
            child.genero = genero
            child.antecedentes_familiares = 'Sí' if antecedentes_familiares == 'Sí' else 'No'
            child.diagnostico_previo = 'Sí' if diagnostico_previo == 'Sí' else 'No'
            child.observaciones = observaciones
            child.color = color

            if new_child:
                child.dni_profesional = session_state.professional_dni
                db.add(child)
            else:
                db.merge(child)

            session_state.expander_states[child.id_niño] = False

            if new_child:
                session_state.expander_states["new_child_form"] = False
            
            try:
                db.commit()
                st.success(get_text("DATA_MANAGEMENT_VARIABLES", language)["child_data_added_success"] if new_child else get_text("DATA_MANAGEMENT_VARIABLES", language)["child_data_updated_success"])
            except Exception as e:
                st.error(get_text("DATA_MANAGEMENT_VARIABLES", language)["child_data_add_error"].format(e) if new_child else get_text("DATA_MANAGEMENT_VARIABLES", language)["child_data_update_error"].format(e))

            st.experimental_rerun()



def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def toggle_expander_state(child_id, session_state):
    session_state.expander_states[child_id] = not session_state.expander_states[child_id]

## no funciona el expander state, revisar el app.py cambiar el metodo para cerrarlo si no se ve nada

def render_dashboard(session_state):
    db = SessionLocal()
    professional_dni = session_state.professional_dni
    children = db.query(Niño).filter(Niño.dni_profesional == professional_dni).all()

    st.sidebar.markdown("___")
    st.sidebar.subheader(get_text("MENU_ITEMS", session_state.language)["display_data_management"])

    with st.sidebar.expander(get_text("DATA_MANAGEMENT_VARIABLES", session_state.language)["child_form_expander"]):
        new_child = Niño()
        child_form(db, new_child, session_state, new_child=True)

    for child in children:
        if child.id_niño not in session_state.expander_states:
            session_state.expander_states[child.id_niño] = False

        query_params = st.experimental_get_query_params()
        expander_closed_str = query_params.get("expander_closed", [None])[0]

        try:
            expander_closed = int(expander_closed_str)
        except (ValueError, TypeError):
            expander_closed = 0

        if expander_closed == child.id_niño:
            session_state.expander_states[child.id_niño] = False
            st.experimental_set_query_params(expander_closed=None)  # Limpia el parámetro de consulta

        expander_state = session_state.expander_states[child.id_niño]
        
        col1, col2 = st.columns([3, 1])
        with col1:
            with st.expander(f"{child.nombre} {child.apellidos}", expanded=expander_state):
                child_form(db, child, session_state)
        with col2:
            with st.expander("", expanded=False):  
                st.write("Diagnóstico del niño")
                #llamada a una funcion para traer el ultimo diagnostico del niño y un numero que infdique cuantos diagnosticos lleva hechos
                #prepara el try 



def display_data_management(session_state):
    language = session_state.language
    st.subheader(get_text("MENU_ITEMS", language)["display_data_management"])

    render_dashboard(session_state)

if __name__ == "__main__":
    display_data_management(session_state)

