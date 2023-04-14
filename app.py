import streamlit as st
from streamlit import session_state
from authentication.login import authenticate
from models.database import SessionLocal, Base
from modules import home_page, data_management, new_diagnosis, diagnosis_history, resources_tools, settings
from constants.config import get_text, LANGUAGES

# Funciones de Streamlit y el resto de la aplicación
st.set_page_config(
    page_title='Evaluación TEA',
    layout="wide",
    initial_sidebar_state="expanded"
)

# app.py
@st.cache_resource
class SessionState:
    def __init__(self):
        self.language = "es"
        self.logged_in = False
        self.selected_menu_item = home_page.display_home_page

def main():
    session_state = SessionState()

    if not session_state.logged_in:
        # Crear un espacio vacío en la parte superior de la página
        st.empty()

        # Centrar el título y el subheader
        _, title_col, _ = st.columns([1, 1.5, 1])
        with title_col:
            st.title("Plataforma para Diagnostico de TEA")
            st.subheader("Iniciar sesión")
            db = SessionLocal()
            session_state.logged_in = authenticate(db)

        if session_state.logged_in:
            st.experimental_rerun()
    else:
        
        session_state.language = st.session_state.get("language", "es")

    menu_items = [
        home_page.display_home_page,
        data_management.display_data_management,
        new_diagnosis.display_new_diagnosis,
        diagnosis_history.display_diagnosis_history,
        resources_tools.display_resources_tools,
        settings.display_settings,
    ]

    if session_state.logged_in:
        if session_state.language is None:
            session_state.language = "es"

        if session_state.selected_menu_item is None:
            session_state.selected_menu_item = menu_items[0]

        choice = st.sidebar.selectbox(
            get_text("HOME_TITLE", session_state.language),
            [get_text("MENU_ITEMS", session_state.language)[func.__name__] for func in menu_items]
        )

        # Encuentra el índice del elemento seleccionado y actualiza el estado de la sesión
        choice_index = [get_text("MENU_ITEMS", session_state.language)[func.__name__] for func in menu_items].index(choice)
        session_state.selected_menu_item = menu_items[choice_index]

        st.sidebar.markdown("## " + get_text("SIDEBAR_LINKS", session_state.language)["research"])
        st.sidebar.button(get_text("SIDEBAR_LINKS", session_state.language)["research"], on_click=None, args=None, kwargs=None, key=None, help=None)
        st.sidebar.button(get_text("SIDEBAR_LINKS", session_state.language)["communities"], on_click=None, args=None, kwargs=None, key=None, help=None)
        st.sidebar.button(get_text("SIDEBAR_LINKS", session_state.language)["tools_apps"], on_click=None, args=None, kwargs=None, key=None, help=None)

        session_state.selected_menu_item(session_state)

if __name__ == "__main__":
    main()
