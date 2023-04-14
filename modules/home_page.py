import streamlit as st
from streamlit import session_state
from authentication.login import authenticate
from models.database import SessionLocal, Base
from modules import home_page, data_management, new_diagnosis, diagnosis_history, resources_tools, settings
from constants.config import get_text, LANGUAGES

def display_home_page(session_state):
    language = session_state.language

    st.subheader(get_text("MENU_ITEMS", language)["display_home_page"])
    st.markdown(get_text("HOME_DESCRIPTION", language))

    st.markdown(get_text("USAGE_INSTRUCTIONS", language).strip())
    st.markdown("---")

    st.markdown(get_text("AUTHORS_LICENSE", language)["authors"])
    st.markdown(get_text("AUTHORS_LICENSE", language)["email"])
    st.markdown(get_text("AUTHORS_LICENSE", language)["profiles"])
    st.markdown(get_text("AUTHORS_LICENSE", language)["license"])

if __name__ == "__main__":
    display_home_page(session_state)
