import streamlit as st
from streamlit import session_state
from authentication.login import authenticate
from models.database import SessionLocal, Base
from modules import home_page, data_management, new_diagnosis, diagnosis_history, resources_tools, settings
from constants.config import get_text, LANGUAGES

def display_settings(session_state):
    language = session_state.language

    st.title(get_text("MENU_ITEMS", language)["display_settings"])

    languages_options = LANGUAGES[language]
    current_language_index = next((index for index, lang in enumerate(languages_options) if lang["code"] == session_state.language), 0)

    selected_language = st.selectbox("Selecciona el idioma / Select Language",
                                     [lang["label"] for lang in languages_options],
                                     index=current_language_index)

    # Encuentra el código de idioma seleccionado y actualiza el estado de la sesión
    selected_language_code = next((lang["code"] for lang in languages_options if lang["label"] == selected_language), None)
    session_state.language = selected_language_code

    # Aquí puedes agregar más configuraciones si lo deseas

if __name__ == "__main__":
    display_settings(session_state)
