import streamlit as st
from streamlit import session_state
from authentication.login import authenticate
from models.database import SessionLocal, Base
from modules import home_page, data_management, new_diagnosis, diagnosis_history, resources_tools, settings
from constants.config import get_text, LANGUAGES

def display_settings(session_state):
    language = session_state.language
    theme = session_state.theme

    st.subheader(get_text("PAGE_TITLES", language)["display_settings"])

    # Configuración del idioma
    st.markdown("##### " + get_text("SETTINGS_SECTIONS", language)["language"], unsafe_allow_html=True)

    languages_options = LANGUAGES[language]
    current_language_index = next((index for index, lang in enumerate(languages_options) if lang["code"] == session_state.language), 0)

    selected_language = st.selectbox(get_text("SETTINGS_PROMPTS", language)["select_language"],
                                     [lang["label"] for lang in languages_options],
                                     index=current_language_index)

    # Encuentra el código de idioma seleccionado y actualiza el estado de la sesión
    selected_language_code = next((lang["code"] for lang in languages_options if lang["label"] == selected_language), None)
    session_state.language = selected_language_code
        
    # # Configuración del tema
    # st.markdown("##### " + get_text("SETTINGS_SECTIONS", language)["theme"], unsafe_allow_html=True)

    # theme_col, font_col = st.columns(2)

    # with theme_col:
    #     theme_options = ["Light", "Dark"]
    #     selected_theme = st.selectbox(get_text("SETTINGS_PROMPTS", language)["select_theme"], theme_options, index=theme_options.index(theme))

    # with font_col:
    #     font_options = ["sans serif", "serif", "monospace"]
    #     current_font = st.config.get_option("theme.font") or "sans serif"
    #     selected_font = st.selectbox("Selecciona la fuente:", font_options, index=font_options.index(current_font))

    # session_state.theme = selected_theme

    # if selected_font != current_font:
    #     st.config.set_option("theme.font", selected_font)


    if st.button("Guardar cambios"):
        # apply_theme(session_state.theme)
        apply_language(selected_language_code)
        st.experimental_rerun()


def apply_theme(theme):
    if theme == "Dark":
        st.config.set_option("theme.base", "dark")
    else:
        st.config.set_option("theme.base", "light")

def apply_language(language):
    st.session_state.language = language

if __name__ == "__main__":
    display_settings(session_state)
