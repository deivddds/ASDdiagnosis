import streamlit as st
from streamlit import session_state
from authentication.login import authenticate
from models.database import SessionLocal, Base
from modules import home_page, data_management, new_diagnosis, diagnosis_history, resources_tools, settings
from constants.config import get_text, LANGUAGES

def display_diagnosis_history(session_state):
    language = session_state.language
    st.subheader(get_text("MENU_ITEMS", language)["display_diagnosis_history"])

if __name__ == "__main__":
    display_diagnosis_history(session_state)